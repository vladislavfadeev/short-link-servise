from os import sync
import string
import random
from typing import Union

from fastapi import HTTPException
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from apps.db_model.models import GroupLinkModel, LinkModel
from apps.api.schemas import CreateGroup, CreateLinkModel, FailValidationModel

User = get_user_model()


@sync_to_async
def make_slug():
    data = string.ascii_letters + string.digits
    while True:
        slug = ''.join(random.choice(data) for _ in range(8))
        if not LinkModel.objects.filter(slug=slug).exists():
            break
    return slug


@sync_to_async
def uniq_check(slug):
    if slug is not None:
        if LinkModel.objects.filter(slug=slug).exists():
            raise HTTPException(
                status_code=422,
                detail='Object with such a slug already exists'
            )


class ItemChecker():

    @staticmethod
    def _group_filter(**kwargs) -> bool:
        return GroupLinkModel.objects.filter(**kwargs).exists()

    @staticmethod
    def _link_filter(**kwargs) -> bool:
        return LinkModel.objects.filter(**kwargs).exists()
    
    @staticmethod
    def _make_group_alias(item: CreateGroup) -> Union[type[CreateGroup], None]:
        if item.alias is None:
            item.alias = GroupLinkModel.make_alias()
        return item

    @staticmethod
    def _make_link_slug(item: CreateLinkModel) -> Union[type[CreateLinkModel], None]:
        if item.group and item.slug is None:
            item.slug = LinkModel.make_slug(group=item.group)
            return item

        elif item.group is None and item.slug is None:
            item.slug = LinkModel.make_slug()
            return item

    @classmethod
    def _check_link(cls, item: CreateLinkModel, user: User) -> Union[type[CreateLinkModel], type[FailValidationModel]]:
        if item.group:
            if not cls._group_filter(user=user, id=item.group):
                return FailValidationModel(
                    loc={'group': item.group},
                    msg=(
                        'Group with the specified id does not exist. '
                        'If you want to specify a new group, you need to create it first'
                    )
                )
        if item.group and item.slug:
            if cls._link_filter(group=item.group, slug=item.slug):
                return FailValidationModel(
                    loc={'slug': item.slug}, msg='Current slug is not unique in the specified group'
                )
        elif item.slug:
            if cls._link_filter(slug=item.slug):
                return FailValidationModel(
                    loc={'slug': item.slug}, msg='Current slug is not unique'
                )
        return item

    @classmethod
    def _check_group(cls, item:CreateGroup, user: User):
        if cls._group_filter(user=user, title=item.title):
            return FailValidationModel(
                loc={'title': item.title},
                msg='Current title is not unique in yor account'
            )
        if item.alias:
            if cls._group_filter(alias=item.alias):
                return FailValidationModel(
                    loc={'alias': item.alias},
                    msg='Current alias is not unique'
                )
        return item

    @classmethod
    @sync_to_async
    def validate(cls, item: CreateLinkModel, user: User) -> Union[type[CreateLinkModel], type[FailValidationModel]]:
        return cls._make_link_slug(item) or cls._check_link(item, user)
    
    @classmethod
    @sync_to_async
    def validate_group(cls, item: CreateGroup, user: User):
        item = cls._check_group(item, user)
        if isinstance(item, FailValidationModel):
            return item
        return cls._make_group_alias(item)
        