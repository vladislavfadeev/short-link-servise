import typing
import json

from starlette.authentication import (
    AuthCredentials,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from apps.api.api_auth.auth import SimpleAuthBackend
from apps.api.api_auth.exceptions import AuthenticationFailed


class AuthMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        backend: SimpleAuthBackend,
        on_error: typing.Optional[
            typing.Callable[[HTTPConnection, AuthenticationFailed], Response]
        ] = None,
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationFailed], Response
        ] = (on_error if on_error is not None else self.default_on_error)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        print(conn.headers)
        try:
            auth_result = await self.backend.get_auth(conn)
        except AuthenticationFailed as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return
        print(auth_result)
        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()
        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=400)
