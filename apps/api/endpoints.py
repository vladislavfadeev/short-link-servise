from typing import List

from fastapi import APIRouter

from django.contrib.auth import get_user_model

from apps.api import schemas
from apps.db_model import models

User = get_user_model()
api_router = APIRouter()


@api_router.post("/items", response_model=schemas.LinkModel)
def create_item(item: schemas.LinkModel):
    user_id = item.user_id
    user = User.objects.get(id = user_id)
    item = models.LinkModel.objects.create(user=user, **item.dict())

    return item


@api_router.get("/items", response_model=List[schemas.LinkModel])
def read_items():
    items = list(models.LinkModel.objects.all())

    return items