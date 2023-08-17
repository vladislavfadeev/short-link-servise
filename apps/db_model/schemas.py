from typing import Any
from pydantic import BaseModel


class DetailBase(BaseModel):
    clicks: int
    device: list
    os: list
    source: list
    browser: list
    date: list

    class Config:
        from_attributes = True


class LinkDetailStatistics(DetailBase):
    pass


class GroupDetailStatistics(DetailBase):
    links: int


class AccountDetailStatistics(DetailBase):
    links: int
    groups: int
