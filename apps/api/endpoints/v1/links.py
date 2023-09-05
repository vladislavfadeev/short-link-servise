from typing import Annotated

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from fastapi import APIRouter, Request, HTTPException, Response, status, Query
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model import models
from apps.db_model.statistics import Statistics
from apps.api.utils.validators import ItemChecker
from apps.api.utils.exceptions import IValidationError

router = APIRouter()
User = get_user_model()


@router.get(
    "/",
    response_model=schemas.LinksList,
    responses={**schemas.code_401},
)
async def links_list(
    request: Request,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 15,
):
    """
    # Get a list of links created by the user.

    ## Parameters:
    - `skip` : The count of links to skip from the beginning. Defaults to 0.
    - `limit` : The maximum count of links to show. Defaults to 15.

    ## Exceptions:
    - `401` : If the user is not authorized.

    """
    user = request.user
    limit = skip + limit
    obj_list = await sync_to_async(list)(
        models.LinkModel.objects.filter(user=user).select_related("group")[skip:limit]
    )
    total = Statistics._link_count(user)
    shown = len(obj_list)
    return {"links_total": total, "links_skipped": skip, "links_shown": shown, "links_list": obj_list}


@router.get(
    "/{slug}",
    response_model=schemas.ViewLinkModel,
    responses={**schemas.code_401, **schemas.code_404},
)
async def link_detail(request: Request, slug: str):
    """
    # Get detailed information about link.

    ## Parameters:
    - `slug` : The unique slug identifier of the link.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the link does not exist.
    """
    user = request.user
    try:
        data = await models.LinkModel.objects.select_related("group").aget(
            user=user, slug=slug
        )
    except models.LinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="You do not have created link with such a slug"
        )
    return data


@router.put(
    "/{slug}",
    response_model=schemas.ViewLinkModel,
    responses={**schemas.code_401, **schemas.code_404},
)
async def partial_update(
    item: schemas.PartialUpdateLinkModel, slug: str, request: Request
):
    """
    # Partially update a link's information.

    ## Parameters:
    - `slug` : The unique slug identifier of the link.

    ## Exceptions:
    - `400` : If the update fails.
    - `401` : If the user is not authorized.
    - `404` : If the link does not exist.
    - `422` : If you have validation error.
    """
    user = request.user
    is_exist = await models.LinkModel.objects.filter(user=user, slug=slug).aexists()
    if is_exist:
        update_data = item.dict(exclude_unset=True)
        res = await models.LinkModel.objects.filter(user=user, slug=slug).aupdate(
            **update_data
        )
        if res:
            link = await models.LinkModel.objects.select_related("group").aget(
                user=user, slug=slug
            )
            return link
        else:
            raise HTTPException(status_code=400, detail="Not updated")
    raise HTTPException(
        status_code=404, detail="You do not have created link with such a slug"
    )


@router.delete(
    "/{slug}", status_code=204, responses={**schemas.code_401, **schemas.code_404}
)
async def delete_link(request: Request, slug: str):
    """
    # Delete a link by its slug.

    ## Parameters:
    - `slug` : The unique slug identifier of the link.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the specified group doesn't exist.
    """
    user = request.user
    try:
        await models.LinkModel.objects.get(user=user, slug=slug).adelete()
    except models.LinkModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Link does not exist")
    else:
        return Response(status_code=204)


@router.get(
    "/{slug}/info",
    response_model=schemas.LinkInfo,
    responses={**schemas.code_401, **schemas.code_404},
)
async def link_info(request: Request, slug: str):
    """
    # Retrieve detailed information about a link.

    ## Parameters:
    - `slug` : The unique slug identifier of the link.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If link does not exist.
    """
    try:
        data = await Statistics.async_link_info(request.user, slug)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return data


@router.post(
    "/",
    response_model=schemas.ViewLinkModel, #schemas.CreateViewLinkModel, 
    status_code=201,
    responses={**schemas.code_401},
)
async def create_item(item: schemas.CreateLinkModel, request: Request):
    """
    # Create a new link.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `422` : If you have validation error.
    """
    item = await ItemChecker.validate_link(item, request.user)
    if isinstance(item, schemas.FailValidationModel):
        raise IValidationError(
            msg=item.msg, loc=("body", *tuple(item.loc)), model=schemas.CreateLinkModel
        )
    obj = await models.LinkModel.objects.acreate(user=request.user, **item.dict())
    return obj


@router.post(
    "/multiple",
    status_code=201,
    response_model=schemas.MultipleResponseModel,
    responses={**schemas.code_401, **schemas.code_413},
)
async def multiple_create_item(
    items: list[schemas.CreateLinkModel], request: Request, response: Response
):
    """
    # Multiple create links.
    
    ## Items quantity must be less or equal 70.
    ## For free use, requests quantity cannot exceed 5 per minute and 50 per day. If you need more email us.
    
    ## Exceptions:
    - `413` : If you send too much items.
    - `422` : If you have validation error.
    """
    if len(items) > 70:
        return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
    user = request.user
    fail_items = []
    success_items = []
    for item in items:
        item = await ItemChecker.validate_link(item, user)
        if isinstance(item, schemas.FailValidationModel):
            fail_items.append(item)
            continue
        success_items.append(models.LinkModel(user=user, **item.dict()))
    if not success_items:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    links = await models.LinkModel.objects.abulk_create(success_items)
    return {"fails": fail_items, "created": [model_to_dict(i) for i in links]}
