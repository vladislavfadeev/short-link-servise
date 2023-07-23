from typing import Annotated

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from fastapi import APIRouter, Request, HTTPException, Response, status, Query
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics
from apps.api.utils.validators import ItemChecker
from apps.api.utils.exceptions import IValidationError

router = APIRouter()
User = get_user_model()



@router.get("/", response_model=schemas.LinksList)
async def links_list(request: Request, skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 20):
    user = request.user
    limit = skip + limit
    obj_list = await sync_to_async(list)(models.LinkModel.objects.filter(user=user).select_related('group')[skip:limit])
    total = Statistics._link_count(user)
    shown = len(obj_list)
    return {'links_total': total, 'links_shown': shown, 'links_list': obj_list}


@router.get("/{slug}", response_model=schemas.ViewLinkModel)
async def link_detail(request: Request, slug: str):
    user = request.user
    try:
        data = await models.LinkModel.objects.select_related('group').aget(user=user, slug=slug)
    except models.LinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="You do not have created link with such a slug"
        )
    return data


@router.put("/{slug}", response_model=schemas.ViewLinkModel)
async def partial_update(item: schemas.PartialUpdateLinkModel, slug: str, request: Request):
    user = request.user
    is_exist = await models.LinkModel.objects.filter(user=user, slug=slug).aexists()
    if is_exist:
        update_data = item.dict(exclude_unset=True)
        res = await models.LinkModel.objects.filter(user=user, slug=slug).aupdate(**update_data)
        if res:
            link=await models.LinkModel.objects.select_related('group').aget(user=user, slug=slug)
            return link
        else:
            raise HTTPException(status_code=400, detail='Not updated')
    raise HTTPException(status_code=400, detail='You do not have created link with such a slug')    


@router.delete("/{slug}")
async def delete_link(request: Request, slug: str):
    user = request.user
    try:
        await models.GroupLinkModel.objects.get(user=user, slug=slug).adelete()
    except models.LinkModel.DoesNotExist:
        raise HTTPException(status_code=404, detail='Link does not exist')
    else:
        return Response(status_code=205)
    

@router.get("/{slug}/info", response_model=schemas.LinkInfo)
async def link_info(request: Request, slug: str):
    data = await Statistics.link_info(request.user, slug)
    return data


@router.post("/", response_model=schemas.CreateViewLinkModel)
async def create_item(item: schemas.CreateLinkModel, request: Request):
    item = await ItemChecker.validate_link(item, request.user)
    if isinstance(item, schemas.FailValidationModel):
        raise IValidationError(msg=item.msg, loc=('body', *tuple(item.loc)), model=schemas.CreateLinkModel)
    obj = await models.LinkModel.objects.acreate(user=request.user, **item.dict())
    return obj


@router.post("/multiple", response_model=schemas.MultipleResponseModel)
async def multiple_create_item(items: list[schemas.CreateLinkModel], request: Request, response: Response):
    user = request.user
    fail_items = []
    success_items = []
    for item in items:
        item = await ItemChecker.validate_link(item, user)
        if isinstance(item, schemas.FailValidationModel):
            fail_items.append(item)
            continue
        success_items.append(models.LinkModel(user=user,**item.dict()))
    if not success_items:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    links = await models.LinkModel.objects.abulk_create(success_items)
    return {'fails': fail_items, 'created': [model_to_dict(i) for i in links]}
