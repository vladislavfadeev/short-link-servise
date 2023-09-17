from fastapi import APIRouter, Depends

from apps.api.api_auth.permissions import AuthPermissions
from apps.api.endpoints.v1 import (
    qr,
    links,
    groups,
    account,
)


api_router = APIRouter(dependencies=[Depends(AuthPermissions())])

api_router.include_router(links.router, prefix="/links", tags=["Link endpoints"])
api_router.include_router(groups.router, prefix="/groups", tags=["Group endpoints"])
api_router.include_router(
    account.router, prefix="/users", tags=["User account endpoints"]
)
api_router.include_router(qr.router, prefix="/qr", tags=["QR endpoints"])
