from typing import List

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Request, HTTPException

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics

router = APIRouter()


@router.get("/", response_model=List[schemas.GroupLinkModel])
async def group_list(request: Request):
    user = request.user
    data = await sync_to_async(list)(models.GroupLinkModel.objects.filter(user=user))
    if not len(data):
        raise HTTPException(
            status_code=404,
            detail='You do not have any created groups'
        )
    return data


@router.get("/{pk}", response_model=schemas.LinkModel)
async def group_detail(request: Request, pk: int):
    user = request.user
    try:
        data = await models.GroupLinkModel.objects.aget(user=user, id=pk)
    except models.GroupLinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail='You do not have any created groups with such a primary key'
        )
    return data


@router.get("/{pk}/info", response_model=schemas.GroupInfo)
async def group_info(request: Request, pk: int):
    user = request.user
    data = await Statistics.group_info(user, pk)
    return data