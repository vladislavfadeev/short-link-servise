import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clkr_core.settings")
apps.populate(settings.INSTALLED_APPS)

from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.simple import MemoryBackend

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from apps.api.utils.exceptions import IValidationError

from apps.api.endpoints.router import api_router
from apps.api.api_auth.auth import SimpleAuthBackend
from apps.api.middleware import NotAuthDocsRedirectMiddleware
from apps.api.utils.exc_handlers import ivalidation_error_handler
from apps.api.utils import openapi_schemas, api_rate_limit


def get_application() -> FastAPI:
    app = FastAPI(
        title=os.environ["PROJECT_NAME"],
        # debug=os.environ["DEBUG"],
        debug=False,
        docs_url=os.environ["SWAGGER_URL"],
        redoc_url=os.environ["REDOC_URL"],
        openapi_url=os.environ["OPENAPI_URL"],
    )
    app.add_middleware(
        RateLimitMiddleware,
        authenticate=api_rate_limit.rate_limit_auth_func,
        backend=MemoryBackend(),
        config={
            r"^/api/v1/links": [Rule(second=2)],
            r"^/api/v1/groups": [Rule(second=2)],
            r"^/api/v1/users": [Rule(second=2)],
            r"^/api/v1/qr": [Rule(second=2)],
            r"^/api/v1/links/multiple": [Rule(minute=5, day=50)],
            r"^/api/v1/qr/multiple": [Rule(minute=5, day=50)],
        },
    )
    app.add_middleware(NotAuthDocsRedirectMiddleware)
    app.add_middleware(AuthenticationMiddleware, backend=SimpleAuthBackend())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=(
            "DELETE",
            "GET",
            "POST",
            "PUT",
        ),
        allow_headers=["*"],
    )
    app.add_exception_handler(IValidationError, ivalidation_error_handler)
    app.include_router(api_router, prefix="/api/v1")
    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app


def custom_openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=openapi_schemas.title,
        version=openapi_schemas.version,
        description=openapi_schemas.description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://clkr.su/static/img/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = get_application()
app.openapi = custom_openapi_schema
