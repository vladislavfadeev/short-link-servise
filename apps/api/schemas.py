from datetime import date, datetime
from typing import Optional, TypeVar
from pydantic import BaseModel, AnyHttpUrl

T = TypeVar('T')


class Base(BaseModel):
    id: int

    class Config:
        orm_mode = True


class LinkModel(Base):
    user_id: Optional[int | None]
    group: Optional[int | None]
    slug: str
    long_link: AnyHttpUrl
    statistics: bool = False
    is_private: bool = False
    password: Optional[str]
    svg_image: Optional[str | None]
    png_image: Optional[str | None]
    date_created: Optional[date]
    last_changed: Optional[datetime]
    date_expire: Optional[datetime | None]
    use_alias: bool = False
    is_active: bool = True


class GroupLinkModel(Base):
    user_id: int
    title: str
    description: str
    is_active: bool
    is_private: bool
    password: str


class LinkInfo(BaseModel):
    clicks: int
    device: list[dict]
    source: list[dict]
    browser: list[dict]
    date: list[dict]

    class Config:
        orm_mode = True


class GroupInfo(LinkInfo):
    links: int


class AccountInfo(GroupInfo):
    groups: int


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