from datetime import date, datetime
from typing import Any, Optional, TypeVar
from pydantic import BaseModel, HttpUrl, validator
from django.contrib.auth.hashers import make_password
from asgiref.sync import sync_to_async
import string

from apps.db_model.models import LinkModel


T = TypeVar('T')
literals = string.ascii_letters + string.digits


class Base(BaseModel):
    id: Optional[int | None]

    class Config:
        orm_mode = True


class GroupBase(Base):
    title: str                      # добавить проверку на кол-во символов
    alias: Optional[str]
    description: Optional[str]
    is_active: Optional[bool] = True
    rotation: Optional[bool] = False
    

class CreateGroup(GroupBase):
    password: Optional[str]


class ViewGroupList(GroupBase):
    password: bool
    links_entry: Optional[int]
    links: Any

    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False


class BaseLinkModel(Base):
    slug: Optional[str | None]
    long_link: HttpUrl
    date_expire: Optional[datetime | None]
    is_active: Optional[bool] = True


class CreateLinkModel(BaseLinkModel):
    password: Optional[str | None]
    group: Optional[int]

    @validator('slug')
    def slug(cls, v):
        for i in list(v):
            if i not in literals:
                raise ValueError(
                    'Slug must only contain English letters and digits'
                )
        return v
    
    @validator('password')
    def pwd_setter(cls, v):
        return make_password(v)



class ViewLinkModel(BaseLinkModel):
    date_created: Optional[date]
    last_changed: Optional[datetime]
    password: Optional[bool]
    group: ViewGroupList | None
    qr: str

    
    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False


class ViewLinkInGroup(BaseLinkModel):
    date_created: Optional[date]
    last_changed: Optional[datetime]
    password: Optional[bool | None]
    qr: str

    @validator('password')
    def pwd(cls, v):
        return True if v else False


class ViewGroupDetail(GroupBase):
    links: Optional[Any]

  
class ViewCreatedGroup(GroupBase):
    password: bool

    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False


class BaseInfo(BaseModel):
    clicks: int
    device: list[dict]
    source: list[dict]
    browser: list[dict]
    date: list[dict]

    class Config:
        orm_mode = True


class LinkInfo(BaseInfo):
    pass


class GroupInfo(BaseInfo):
    links: int


class AccountInfo(GroupInfo):
    groups: int


class FailValidationModel(BaseModel):
    loc: dict
    msg: str


class MultipleResponseModel(BaseModel):
    fails: Optional[list[FailValidationModel]]
    created: Optional[list[ViewLinkModel]]


{
  "detail": [
    {
      "loc": [
        "body",
        0,
        "slug"
      ],
      "msg": "Slug can only contain English letters and digits",
      "type": "value_error"
    }
  ]
},
{
  "fails": [
    {
      "loc": {
        "slug": "kjbwnw"
      },
      "msg": "Current slug is not unique"
    },
    {
      "loc": {
        "slug": "kjbwn"
      },
      "msg": "Current slug is not unique"
    }
  ],
  "success": []
}


# class ResponseBase(BaseModel):
#     message: str = ""
#     meta: dict = {}
#     data: T | None


# def create_response(
#     data: DataType | None,
#     message: str | None = None,
#     meta: dict | Any | None = {},
# ) -> dict[str, DataType] | DataType:
#     if isinstance(data, IResponsePage):
#         data.message = "Data paginated correctly" if message is None else message
#         data.meta = meta
#         return data
#     if message is None:
#         return {"data": data, "meta": meta}
#     return {"data": data, "message": message, "meta": meta}




# class ItemBase(BaseModel):
#     title: str
#     description: str = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True