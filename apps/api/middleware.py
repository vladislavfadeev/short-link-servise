from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# def is_ok(value):
#     return 200 <= value <= 299


# class MyMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app):
#         super().__init__(app)

#     async def dispatch(self, request: Request, call_next: Callable):      
#         response = await call_next(request)
#         if is_ok(response.status_code):
#             response_body = b""
#             async for chunk in response.content:
#                 response_body += chunk
#             print(response_body)
#         return response
