from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, UUID4, validator, Field
from django.contrib.auth.hashers import make_password
import string


literals = string.ascii_letters + string.digits + "_-"


class Base(BaseModel):
    class Config:
        orm_mode = True


class GroupBase(Base):
    title: str = Field(
        max_length=256, description="Name of your group. Must be unique."
    )
    slug: Optional[str] = Field(
        default=None, max_length=30, description="Group url element. Alias"
    )
    description: Optional[str | None] = None
    disabled: Optional[bool] = False
    rotation: Optional[bool] = Field(default=False, description="Random link choice")


class CreateGroup(GroupBase):
    password: Optional[str | None] = Field(default=None, max_length=32)
    date_expire: Optional[date | None] = None

    @validator("date_expire")  # , pre=True
    def group_date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError("Date cannot be less or equal than today")
        return date


class ViewGroupInList(GroupBase):
    id: int
    password: bool
    short_url: str
    links_entry: Optional[int] = Field(
        description="The count of links that the group contains."
    )
    date_expire: Optional[date]
    qr: str

    @validator("password", pre=True)
    def pwd(cls, v):
        return True if v else False


class ViewGroupInLink(GroupBase):
    id: int
    password: bool
    short_url: str
    date_expire: Optional[date]

    @validator("password", pre=True)
    def pwd(cls, v):
        return True if v else False


class GroupList(Base):
    groups_total: int = Field(description="The count of groups in the account.")
    groups_shown: int = Field(description="The count of shown groups.")
    groups_list: list[ViewGroupInList | None]


class BaseLinkModel(Base):
    slug: Optional[str | None] = Field(default=None, max_length=30)
    title: Optional[str | None] = Field(
        default=None,
        max_length=512,
        description="The name of the link. It show to the customer, be careful.",
    )
    long_link: HttpUrl
    date_expire: Optional[date | None] = None
    disabled: Optional[bool] = False


class CreateLinkModel(BaseLinkModel):
    password: Optional[str | None] = Field(default=None, max_length=32)
    group_id: Optional[int | None] = None

    @validator("slug")
    def slug(cls, v):
        for i in list(v):
            if i not in literals:
                raise ValueError("Slug must contain English letters and digits only")
        return v

    @validator("date_expire", pre=True)
    def date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError("Date cannot be less or equal than today")
        return date

    @validator("password")
    def pwd_setter(cls, v):
        return make_password(v)


class ViewLinkInGroup(BaseLinkModel):
    date_created: Optional[datetime]
    last_changed: Optional[datetime]
    password: Optional[bool | None]
    short_url: str
    qr: str

    @validator("password", pre=True)
    def pwd(cls, v):
        return True if v else False


class ViewLinkModel(ViewLinkInGroup):
    group: Optional[ViewGroupInLink | None]


class LinksList(Base):
    links_total: int = Field(description="Count of all links in the account")
    links_skipped: int = Field(description="Count of skipped links")
    links_shown: int = Field(description="Count of current shown links")
    links_list: list[ViewLinkModel] | None


class PartialUpdateLinkModel(Base):
    title: Optional[str | None] = Field(
        default=None,
        max_length=512,
        description="The name of the link. It show to the customer, be careful.",
    )
    group_id: Optional[int | None] = None
    password: Optional[str | None] = Field(default=None, max_length=32)
    date_expire: Optional[date | None] = None
    disabled: Optional[bool] = False

    @validator("password")
    def pwd_setter(cls, v):
        return make_password(v)

    @validator("date_expire", pre=True)
    def link_date_expire(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError("Date cannot be less or equal than today")
        return date


class PartialUpdateGroupModel(Base):
    title: Optional[str | None] = Field(
        default=None, max_length=256, description="Name of your group. Must be unique."
    )
    description: Optional[str | None] = None
    rotation: Optional[bool | None] = None
    password: Optional[str | None] = None
    disabled: Optional[bool | None] = None
    date_expire: Optional[date | None] = None

    @validator("password")
    def pwd_setter(cls, v):
        return make_password(v)

    @validator("date_expire", pre=True)
    def date_expire1(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date <= datetime.now():
            raise ValueError("Date cannot be less or equal than today")
        return date


class ViewCreatedGroup(GroupBase):
    id: int
    password: bool
    short_url: str
    date_expire: Optional[date]
    qr: str

    @validator("password", pre=True)
    def pwd(cls, v):
        return True if v else False


class ViewGroupDetail(ViewCreatedGroup):
    links_total: int
    links_shown: int
    links: list[ViewLinkInGroup] | None


class BaseInfo(Base):
    clicks: int
    device: list[dict | None]
    source: list[dict | None]
    browser: list[dict | None]
    date: list[dict | None]


class LinkInfo(BaseInfo):
    pass


class GroupInfo(BaseInfo):
    links: int | None


class AccountInfo(GroupInfo):
    groups: Optional[int | None]


class FailValidationModel(Base):
    loc: dict
    msg: str


class MultipleResponseModel(Base):
    fails: Optional[list[FailValidationModel | None]]
    created: Optional[list[ViewLinkModel | None]]  # CreateViewLinkModel


class QRCodeRetrieve(Base):
    slug: UUID4
    text: str
    qr: str
    date_created: datetime


class QRCodeCreate(Base):
    text: str = Field(max_length=550)


code_401 = {
    401: {
        "description": "User is not authorized",
        "content": {"application/json": {"example": {"detail": "Not authorized."}}},
    }
}

code_404 = {
    404: {
        "description": "Item not found",
        "content": {"application/json": {"example": {"detail": "Does not exist."}}},
    }
}

code_413 = {
    413: {
        "description": "Payload too large",
        "content": {
            "application/json": {"example": {"detail": "Request entity too large."}}
        },
    }
}
