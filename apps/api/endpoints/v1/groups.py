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


@router.get("/", response_model=schemas.GroupList)
async def group_list(request: Request, skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 10):
    user = request.user
    limit = skip + limit
    obj_list = await sync_to_async(list)(models.GroupLinkModel.objects.filter(user=user).annotate(links_entry=Count('links'))[skip:limit])
    total = Statistics._group_count(user)
    shown = len(obj_list)
    return {'groups_total': total, 'groups_shown': shown, 'groups_list': obj_list}


@router.get("/{pk}", response_model=schemas.ViewGroupDetail)
async def group_detail(request: Request, pk: int, skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 20):
    user = request.user
    limit = skip + limit
    try:
        obj = await models.GroupLinkModel.objects.aget(user=user, id=pk)
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail='You do not have any created groups with such a primary key'
        )
    links = await sync_to_async(list)(models.LinkModel.objects.filter(user=user, group=obj)[skip:limit])
    setattr(obj, 'links_total', Statistics._link_count(user=user, group=obj))
    setattr(obj, 'links_shown', len(links))
    resp_model = schemas.ViewGroupDetail.from_orm(obj)
    resp_model.links = [schemas.ViewLinkInGroup.from_orm(i) for i in links]
    return resp_model
    


@router.put("/{pk}", response_model=schemas.ViewCreatedGroup)
async def partial_update(item: schemas.PartialUpdateGroupModel, pk: int, request: Request):
    user = request.user
    obj_exist = await models.GroupLinkModel.objects.filter(user=user, id=pk).aexists()
    if not obj_exist:
        raise HTTPException(status_code=400, detail='You do not have created group with such a primary key')
    if item.title:
        title_exist = await models.GroupLinkModel.objects.filter(user=user, title=item.title).aexists()
        if title_exist:
            raise IValidationError('Current title is exists.', ('body', 'title'), model=schemas.CreateGroup)
    update_data = item.dict(exclude_unset=True)
    res = await models.GroupLinkModel.objects.filter(user=user, id=pk).aupdate(**update_data)
    if res:
        group=await models.GroupLinkModel.objects.aget(user=user, id=pk)
        return group
    else:
        raise HTTPException(status_code=400, detail='Not updated')
    

@router.delete("/{pk}")
async def delete_group(request: Request, pk: int, cascade: bool = False):
    user = request.user
    if cascade:
        await models.LinkModel.objects.filter(user=user, group_id=pk).adelete()
    try:
        await models.GroupLinkModel.objects.get(user=user, id=pk).adelete()
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(status_code=404, detail='Group does not exist')
    else:
        return Response(status_code=205)


@router.get("/{pk}/info", response_model=schemas.GroupInfo)
async def group_info(request: Request, pk: int):
    user = request.user
    try:
        data = await Statistics.async_group_info(user, pk)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return data


@router.post("/", response_model=schemas.ViewCreatedGroup)
async def group_create(item: schemas.CreateGroup, request: Request):
    item = await ItemChecker.validate_group(item, request.user)
    if isinstance(item, schemas.FailValidationModel):
        raise IValidationError(
            item.msg,
            ('body', *tuple(item.loc)),
            model=schemas.CreateGroup
        )
    resp = await models.GroupLinkModel.objects.acreate(user=request.user, **item.dict())
    return resp