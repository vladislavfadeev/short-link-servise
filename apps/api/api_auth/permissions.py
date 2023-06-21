from typing import Any, Optional
from django.contrib.auth import get_user_model
from fastapi import Request, HTTPException


class AuthPermissions:
    def __init__(
            self,
            role: str | None = None,
            user_model: Optional[Any] = None,
            redirect_to: str = None    
        ):
        self.role = role
        self._user_model = user_model
        self._redirect_to = redirect_to

    @property
    def redirect_to(self):
        pass
        # not completed

    @property
    def user_model(self):
        if self._user_model:
            return self._user_model
        return get_user_model()

    def check_role(self):
        if self.role is None:
            return True
        pass
        # it's not completed

    def check_auth(self, request: Request):
        user = request.user
        if isinstance(user, self.user_model):
            return True
        raise HTTPException(
            status_code=401,
            detail='Not authorized.'
        )

    async def __call__(self, request: Request):
        self.check_auth(request)
        self.check_role()