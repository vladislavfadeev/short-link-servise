from typing import Annotated

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Request, Response, HTTPException, Query
from django.db.models import Count

from apps.api import schemas
from apps.db_model import models
from apps.db_model.statistics import Statistics
from apps.api.utils.validators import ItemChecker
from apps.api.utils.exceptions import IValidationError

router = APIRouter()


@router.get(
    "/",
    response_model=schemas.GroupList,
    responses={**schemas.code_401},
)
async def group_list(
    request: Request,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 10,
):
    """
    # Retrieves a list of all groups created by the user.

    ## Parameters:
    - `skip` : Count of skipped items (default is 0).
    - `limit` : Count of item to show (default is 10).

    ## Exceptions:
    - `401`: If the user is not authorized.
    """
    user = request.user
    limit = skip + limit
    obj_list = await sync_to_async(list)(
        models.GroupLinkModel.objects.filter(user=user).annotate(
            links_entry=Count("linkmodel")
        )[skip:limit]
    )
    total = Statistics._group_count(user)
    shown = len(obj_list)
    return {"groups_total": total, "groups_shown": shown, "groups_list": obj_list}


@router.get(
    "/{pk}",
    response_model=schemas.ViewGroupDetail,
    responses={**schemas.code_401, **schemas.code_404},
)
async def group_detail(
    request: Request,
    pk: int,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 10,
):
    """
    # Retrieves detailed information about a specific group created by the user.

    ## Parameters:
    - `pk` : The primary key of the group to retrieve.
    - `skip` : Count of skipped records of links (default is 0).
    - `limit` : Count of records of links to show (default is 20).

    ## Exceptions:
    - `401`: The user is not authorized.
    - `404`: The group does not exist.
    """
    user = request.user
    limit = skip + limit
    try:
        obj = await models.GroupLinkModel.objects.aget(user=user, id=pk)
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="You do not have any created groups with such a primary key",
        )
    links = obj.linkmodel_set.all()[skip:limit]
    setattr(obj, "links_total", Statistics._link_count(user=user, group=obj))
    setattr(obj, "links_shown", len(links))
    setattr(obj, "links", [i for i in links])
    resp_model = schemas.ViewGroupDetail.from_orm(obj)
    return resp_model


@router.put(
    "/{pk}",
    response_model=schemas.ViewCreatedGroup,
    responses={**schemas.code_401, **schemas.code_404},
)
async def partial_update(
    item: schemas.PartialUpdateGroupModel, pk: int, request: Request
):
    """
    # Partial update details of a group.

    ## Parameters:
    - `pk` : The primary key of the group.

    ## Exceptions:
    - `400` : If the update fails.
    - `401` : If the user is not authorized.
    - `404` : If the specified group doesn't exist.
    - `422` : If you have validation error.
    """
    user = request.user
    obj_exist = await models.GroupLinkModel.objects.filter(user=user, id=pk).aexists()
    if not obj_exist:
        raise HTTPException(
            status_code=404,
            detail="You do not have created group with such a primary key",
        )
    update_data = item.dict(exclude_unset=True)
    title = update_data.get("title", "unset")
    if title != "unset":
        if title is None:
            raise IValidationError(
                "Title can not be empty.", ("body", "title"), model=schemas.CreateGroup
            )
        title_exist = await models.GroupLinkModel.objects.filter(
            user=user, title=title
        ).aexists()
        if title_exist:
            raise IValidationError(
                "Current title is exists.", ("body", "title"), model=schemas.CreateGroup
            )
    res = await models.GroupLinkModel.objects.filter(user=user, id=pk).aupdate(
        **update_data
    )
    if res:
        return await models.GroupLinkModel.objects.aget(user=user, id=pk)
    else:
        raise HTTPException(status_code=400, detail="Not updated")


@router.delete(
    "/{pk}",
    status_code=204,
    responses={**schemas.code_401, **schemas.code_404},
)
async def delete_group(request: Request, pk: int, cascade: bool = False):
    """
    # Delete a specific group.

    ## Parameters:
    - `pk` : The primary key of the group to be deleted.
    - `cascade` : If True, delete all links associated with the group as well.
            Default is False.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the specified group doesn't exist.
    """
    user = request.user
    if cascade:
        await models.LinkModel.objects.filter(user=user, group_id=pk).adelete()
    try:
        await models.GroupLinkModel.objects.get(user=user, id=pk).adelete()
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Group does not exist")
    else:
        return Response(status_code=204)


@router.get(
    "/{pk}/info",
    response_model=schemas.GroupInfo,
    responses={**schemas.code_401, **schemas.code_404},
)
async def group_info(request: Request, pk: int):
    """
    # Retrieve detailed information about a specific group.

    ## Parameters:
    - `pk` : The primary key of the group.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the group does not exist.
    """
    user = request.user
    try:
        data = await Statistics.async_group_info(user, pk)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return data


@router.post(
    "/",
    status_code=201,
    response_model=schemas.ViewCreatedGroup,
    responses={**schemas.code_401},
)
async def group_create(item: schemas.CreateGroup, request: Request):
    """
    # Create a new group.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `422` : If the provided input data is invalid or fails validation.
    """
    item = await ItemChecker.validate_group(item, request.user)
    if isinstance(item, schemas.FailValidationModel):
        raise IValidationError(
            item.msg, ("body", *tuple(item.loc)), model=schemas.CreateGroup
        )
    resp = await models.GroupLinkModel.objects.acreate(user=request.user, **item.dict())
    return resp
