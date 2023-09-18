import os
from typing import Callable

from fastapi import Request
from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import UnauthenticatedUser

REDOC_URL=os.environ["REDOC_URL"]
SWAGGER_URL=os.environ["SWAGGER_URL"]


class NotAuthDocsRedirectMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path in (REDOC_URL, SWAGGER_URL):
            if isinstance(request.user, UnauthenticatedUser):
                return RedirectResponse(
                    f"/login?next={request.url.path}", status_code=301
                )
        response = await call_next(request)
        return response
