from datetime import datetime
from starlette.requests import HTTPConnection
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)


User = get_user_model()


HTTP_HEADER_ENCODING = "iso-8859-1"


# based on DRF Token authentication
class TokenCheck:
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
    {Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a}
    """

    def get_token_model(self):
        if self.token_model is not None:
            return self.token_model

        from apps.authuser.models import Token

        return Token

    def token_auth(self, token: str):
        token: list = token.split()

        if not token or token[0].lower() != self.token_keyword.lower():
            return None

        if len(token) == 1:
            msg = "Invalid token header. No credentials provided."
            raise AuthenticationError(msg)
        elif len(token) > 2:
            msg = "Invalid token header. Token string should not contain spaces."
            raise AuthenticationError(msg)

        return self.authenticate_credentials(token[1])

    def authenticate_credentials(self, token: str):
        model = self.get_token_model()

        try:
            token_obj = model.objects.select_related("user").get(key=token)
        except model.DoesNotExist:
            raise AuthenticationError("Invalid token.")

        if not token_obj.user.is_active:
            raise AuthenticationError("User inactive or deleted.")

        return token_obj.user


class CookieCheck:
    """
    Simple cookie based authentication.
    Get django cookies, decode it and get user.
    """

    def get_cookie_model(self):
        if self.cookie_model is not None:
            return self.cookie_model
        from django.contrib.sessions.models import Session

        return Session

    def cookie_auth(self, cookie: dict):
        session_id = cookie.get("sessionid")

        if session_id is None:
            return

        return self.authenticate_cookies(session_id)

    def authenticate_cookies(self, session_id):
        model = self.get_cookie_model()

        try:
            raw_data = model.objects.get(session_key=session_id)
        except model.DoesNotExist:
            return

        data = raw_data.get_decoded()
        time_now = datetime.now()

        if raw_data.expire_date.timestamp() < time_now.timestamp():
            return
        user_id = data.get("_auth_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return
        if not user.is_active:
            return

        return user


class SimpleAuthBackend(AuthenticationBackend, CookieCheck, TokenCheck):
    def __init__(
        self,
        use_cookie: bool = True,
        use_token: bool = True,
        token_keyword: str = "Token",
        token_model=None,
        cookie_model=None,
    ):
        self.use_cookie = use_cookie
        self.use_token = use_token
        self.token_keyword = token_keyword
        self.token_model = token_model
        self.cookie_model = cookie_model

    @sync_to_async
    def authenticate(self, conn: HTTPConnection):
        user = None
        auth_token = conn.headers.get("Authorization")
        cookies = conn.cookies

        if self.use_cookie and cookies:
            user = self.cookie_auth(cookies)
        if not user and self.use_token and auth_token:
            user = self.token_auth(auth_token)
        if user is None:
            return
        auth = AuthCredentials()

        return (auth, user)
