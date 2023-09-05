from starlette.types import Scope


async def rate_limit_auth_func(scope: Scope):
    return scope['user'], 'default'