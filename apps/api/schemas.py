from datetime import date, datetime
from typing import Any, Optional, TypeVar
from pydantic import BaseModel, Field, HttpUrl, root_validator, validator
from django.contrib.auth.hashers import make_password
import string

from apps.cutter.utils import qr


T = TypeVar('T')
literals = string.ascii_letters + string.digits + '_-'


class Base(BaseModel):

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
    date_expire: Optional[date]

    @validator('date_expire', pre=True)
    def group_date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError('Date cannot be less or equal than today')
        return date 


class ViewGroupInList(GroupBase):
    id: int
    password: bool
    short_url: str
    links_entry: Optional[int]
    date_expire: Optional[date]
    qr: str

    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False
    
class GroupList(Base):
    groups_total: int
    groups_shown: int
    groups_list: list[ViewGroupInList] | None


class BaseLinkModel(Base):
    slug: Optional[str | None]
    long_link: HttpUrl
    date_expire: Optional[date | None]
    is_active: Optional[bool] = True


class CreateLinkModel(BaseLinkModel):
    password: Optional[str | None]
    group_id: Optional[int]

    @validator('slug')
    def slug(cls, v):
        for i in list(v):
            if i not in literals:
                raise ValueError(
                    'Slug must contain English letters and digits only'
                )
        return v
    
    @validator('date_expire', pre=True)
    def date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError('Date cannot be less or equal than today')
        return date        

    @validator('password')
    def pwd_setter(cls, v):
        return make_password(v)
    

class ViewLinkInGroup(BaseLinkModel):
    date_created: Optional[date]
    last_changed: Optional[datetime]
    password: Optional[bool | None]
    short_url: Optional[str]
    qr: str

    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False


class ViewLinkModel(ViewLinkInGroup):
    group: Optional[GroupBase | None]


class LinksList(Base):
    links_total: int
    links_shown: int
    links_list: list[ViewLinkModel] | None


class CreateViewLinkModel(BaseLinkModel):
    date_created: Optional[date]
    last_changed: Optional[datetime]
    password: Optional[bool] 
    group: Optional[GroupBase | None]
    short_url: Optional[str]
    qr: Optional[str]

    # @root_validator(pre=True)
    # def sss(cls, values):
    #     q = qr.make_base64(values.get('long_link'))
    #     values.update({'qr': q})
    #     return values
    
    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False
    

class PartialUpdateLinkModel(Base):
    title: Optional[str]
    group_id: Optional[int]
    password: Optional[str]
    date_expire: Optional[date]
    is_active: Optional[bool]

    @validator('password')
    def pwd_setter(cls, v):
        return make_password(v)

    @validator('date_expire', pre=True)
    def link_date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError('Date cannot be less or equal than today')
        return date 


class PartialUpdateGroupModel(Base):
    title: Optional[str]
    description: Optional[str]
    rotation: Optional[bool]
    password: Optional[str]
    is_active: Optional[bool]
    date_expire: Optional[date]

    @validator('password')
    def pwd_setter(cls, v):
        return make_password(v)
    
    @validator('date_expire', pre=True)
    def date_expire1(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError('Date cannot be less or equal than today')
        return date 


class ViewGroupDetail(GroupBase):
    id: int
    date_expire: Optional[date]
    short_url: str
    qr: str
    links_total: int
    links_shown: int
    links: Optional[Any]
    
  
class ViewCreatedGroup(GroupBase):
    id: int
    password: bool
    short_url: str
    date_expire: Optional[date]
    qr: str

    @validator('password', pre=True)
    def pwd(cls, v):
        return True if v else False


class BaseInfo(BaseModel):
    clicks: int
    device: list[dict | None]
    source: list[dict | None]
    browser: list[dict | None]
    date: list[dict | None]

    class Config:
        orm_mode = True


class LinkInfo(BaseInfo):
    pass


class GroupInfo(BaseInfo):
    links: int | None


class AccountInfo(GroupInfo):
    groups: Optional[int | None]


class FailValidationModel(BaseModel):
    loc: dict
    msg: str


class MultipleResponseModel(BaseModel):
    fails: Optional[list[FailValidationModel]]
    created: Optional[list[CreateViewLinkModel]]



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
