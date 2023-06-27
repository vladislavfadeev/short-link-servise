from fastapi import APIRouter, Depends

from apps.api.api_auth.permissions import AuthPermissions
from apps.api.endpoints.v1 import (
    links,
    groups,
    account,
)


api_router = APIRouter(dependencies=[Depends(AuthPermissions())])

api_router.include_router(links.router, prefix="/link", tags=["link"])
api_router.include_router(groups.router, prefix="/group", tags=["group"])
api_router.include_router(account.router, prefix="/user", tags=["user"])
