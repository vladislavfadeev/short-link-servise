from typing import List, Union
import json

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Request, HTTPException

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics
from apps.api.utils.validators import ItemChecker
from apps.api.utils.exceptions import IValidationError

from django.db.models import Count


router = APIRouter()


@router.get("/", response_model=List[schemas.ViewGroupList])
async def group_list(request: Request):
    user = request.user
    data = await sync_to_async(list)(models.GroupLinkModel.objects.filter(user=user).annotate(links_entry=Count('links')))
    if not len(data):
        raise HTTPException(
            status_code=404,
            detail='You do not have any created groups'
        )
    return data


@router.get("/{pk}", response_model=schemas.ViewGroupDetail)
async def group_detail(request: Request, pk: int):
    user = request.user
    try:
        obj = await models.GroupLinkModel.objects.aget(user=user, id=pk)
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail='You do not have any created groups with such a primary key'
        )
    model = schemas.ViewGroupDetail.from_orm(obj)
    links = await sync_to_async(list)(models.LinkModel.objects.filter(user=user, group=pk))
    model.links = [schemas.ViewLinkInGroup.from_orm(i) for i in links]
    return model


@router.get("/{pk}/info", response_model=schemas.GroupInfo)
async def group_info(request: Request, pk: int):
    user = request.user
    data = await Statistics.group_info(user, pk)
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