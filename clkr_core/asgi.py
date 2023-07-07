import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clkr_core.settings')
apps.populate(settings.INSTALLED_APPS)


from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from apps.api.utils.exceptions import IValidationError

from apps.api.endpoints.router import api_router
from apps.api.api_auth.auth import SimpleAuthBackend
from apps.api.utils.exc_handlers import ivalidation_error_handler



def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    # app.add_middleware(
    #     BaseHTTPMiddleware,
    #     dispatch=add_process_time_header
    # )
    app.add_middleware(
        AuthenticationMiddleware,
        backend=SimpleAuthBackend()
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(IValidationError, ivalidation_error_handler)
    app.include_router(api_router, prefix="/api/v1")
    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()
