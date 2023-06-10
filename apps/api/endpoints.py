from typing import List

from django.contrib.auth import get_user_model
from fastapi import APIRouter, Request
import time 

from apps.api import schemas
from apps.db_model import models
# from apps.api.api_auth.auth import CookieAuthentication, TokenAuthentication

api_router = APIRouter()
# auth = CookieAuthentication()
User = get_user_model()



@api_router.post("/items", response_model=schemas.LinkModel)
def create_item(item: schemas.LinkModel):
    user_id = item.user_id
    user = User.objects.get(id = user_id)
    item = models.LinkModel.objects.create(user=user, **item.dict())

    return item


@api_router.get("/items", response_model=List[schemas.LinkModel])
def read_items(request: Request):
    items = list(models.LinkModel.objects.all())
    print(request.user, request.auth)

    return items


# async def add_process_time_header(request: Request, call_next):
#     if '/api/' in str(request.url):
#         user = await auth.cookie_auth(request.cookies)
#         print(user)
#         if not user:
#             raise Exception
#     response = await call_next(request)
#     return response
    # response = await call_next(request)  request: Request, call_next
    # process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    # return response