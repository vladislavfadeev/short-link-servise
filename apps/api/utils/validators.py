from typing import Union

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from apps.db_model.models import GroupLinkModel, LinkModel
from apps.api.schemas import CreateGroup, CreateLinkModel, FailValidationModel

User = get_user_model()


class ItemChecker():

    @staticmethod
    def _group_filter(**kwargs) -> bool:
        return GroupLinkModel.objects.filter(**kwargs).exists()

    @staticmethod
    def _link_filter(**kwargs) -> bool:
        return LinkModel.objects.filter(**kwargs).exists()

    @classmethod
    def _check_link(cls, item: CreateLinkModel, user: User) -> Union[type[CreateLinkModel], type[FailValidationModel]]:
        # if user enter group id for current link we check group exists
        if item.group_id:
            if not cls._group_filter(user=user, id=item.group_id):
                return FailValidationModel(
                    loc={'group': item.group_id},
                    msg=(
                        'Group with the specified id does not exist. '
                        'If you want to create a new group, you need make it first'
                    )
                )
        # check slug unique if it has been entered
        if item.slug:
            if cls._link_filter(slug=item.slug):
                return FailValidationModel(
                    loc={'slug': item.slug}, msg='Current slug is not unique'
                )        
        return item

    @classmethod
    def _check_group(cls, item:CreateGroup, user: User):
        # check title unique in current user account
        if cls._group_filter(user=user, title=item.title):
            return FailValidationModel(
                loc={'title': item.title},
                msg='Current title is not unique in yor account'
            )
        # if user enter group slug we check unique of it
        if item.slug:
            if cls._group_filter(slug=item.slug):
                return FailValidationModel(
                    loc={'slug': item.slug},
                    msg='Current group slug is not unique'
                )
        return item

    @classmethod
    @sync_to_async
    def validate_link(cls, item: CreateLinkModel, user: User) -> Union[type[CreateLinkModel], type[FailValidationModel]]:
        return cls._check_link(item, user)
    
    @classmethod
    @sync_to_async
    def validate_group(cls, item: CreateGroup, user: User):
        return cls._check_group(item, user)
        