from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl



class LinkModel(BaseModel):
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

    class Config:
        orm_mode = True







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