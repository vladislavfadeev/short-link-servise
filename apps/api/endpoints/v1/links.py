from typing import List

from django.contrib.auth import get_user_model
from fastapi import APIRouter, Depends, Request, HTTPException
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics

router = APIRouter()
User = get_user_model()


@router.get("/", response_model=List[schemas.LinkModel])
async def links_list(request: Request):
    user = request.user
    data = await sync_to_async(list)(models.LinkModel.objects.filter(user=user))
    if not len(data):
        raise HTTPException(
            status_code=404,
            detail='You do not have any created links'
        )
    return data


@router.get("/{slug}", response_model=schemas.LinkModel)
async def link_detail(request: Request, slug: str):
    user = request.user
    try:
        data = await models.LinkModel.objects.aget(user=user, slug=slug)
    except models.LinkModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="You do not have any created links with such a slug"
        )
    return data


@router.get("/{slug}/info", response_model=schemas.LinkInfo)
async def link_info(request: Request, slug: str):
    user = request.user
    data = await Statistics.link_info(user, slug)
    return data


@router.post("/", response_model=schemas.LinkModel)
async def create_item(item: schemas.LinkModel):
    user_id = item.user_id
    user = User.objects.get(id = user_id)
    item = await models.LinkModel.objects.acreate(user=user, **item.dict())
    return item
