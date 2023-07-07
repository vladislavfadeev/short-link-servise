from typing import Union
from django.contrib.auth import get_user_model
from fastapi import APIRouter, Request, HTTPException, Response, status
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics
from apps.api.utils.validators import ItemChecker
from apps.api.utils.exceptions import IValidationError



router = APIRouter()
User = get_user_model()


@router.get("/", response_model=list[schemas.ViewLinkModel])
async def links_list(request: Request):
    user = request.user
    data = await sync_to_async(list)(models.LinkModel.objects.filter(user=user))
    if not len(data):
        raise HTTPException(
            status_code=404,
            detail='You do not have any created links'
        )
    return data


@router.get("/{slug}", response_model=schemas.ViewLinkModel)
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
    data = await Statistics.link_info(request.user, slug)
    return data


@router.post("/", response_model=schemas.ViewLinkModel)
async def create_item(item: schemas.CreateLinkModel, request: Request):
    item = await ItemChecker.validate(item, request.user)
    if isinstance(item, schemas.FailValidationModel):
        raise IValidationError(
            msg=item.msg,
            loc=('body', *tuple(item.loc)),
            model=schemas.CreateLinkModel
        )
    resp = await models.LinkModel.objects.acreate(user=request.user, **item.dict())
    return resp


@router.post("/multiple", response_model=schemas.MultipleResponseModel)
async def multiple_create_item(
    items: list[schemas.CreateLinkModel],
    request: Request,
    response: Response
):
    user = request.user
    fail_items = []
    success_items = []
    for item in items:
        item = await ItemChecker.validate(item, user)
        if isinstance(item, schemas.FailValidationModel):
            fail_items.append(item)
            continue
        success_items.append(models.LinkModel(user=user,**item.dict()))
    if not success_items:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    links = await models.LinkModel.objects.abulk_create(success_items)

    return {'fails': fail_items, 'created': links}
