from fastapi import APIRouter, Request, HTTPException
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model import models
from apps.api.utils.statistics import Statistics

router = APIRouter()


@router.get("/me", response_model=schemas.AccountInfo)
async def account_info(request: Request):
    user = request.user
    data = await Statistics.account_info(user)
    return data