from datetime import datetime

from asgiref.sync import sync_to_async

from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.db.models.functions import TruncDate

from apps.db_model.models import GroupLinkModel, LinkModel, StatisticsModel
from apps.db_model.schemas import (
    LinkDetailStatistics,
    GroupDetailStatistics,
    AccountDetailStatistics,
)


User = get_user_model()


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.strftime("%Y-%m-%d")


class Statistics:
    @staticmethod
    def _from_queryset(queryset: QuerySet) -> dict:
        clicks = len(queryset)
        device = list(
            queryset.values("device").annotate(entries=Count("device")).distinct()
        )
        source = list(
            queryset.values("ref_link").annotate(entries=Count("ref_link")).distinct()
        )
        browser = list(
            queryset.values("browser").annotate(entries=Count("browser")).distinct()
        )
        os = list(queryset.values("os").annotate(entries=Count("os")).distinct())
        date = list(
            queryset.annotate(tr_date=TruncDate("date"))
            .values("tr_date")
            .annotate(entries=Count("tr_date"))
            .distinct()
        )
        data = {
            "clicks": clicks,
            "device": device,
            "os": os,
            "source": source,
            "browser": browser,
            "date": date,
        }
        return data

    @staticmethod
    def _is_exists(model, **kwargs) -> bool:
        return model.objects.filter(**kwargs).exists()

    @staticmethod
    def _link_count(user: User, **kwargs) -> int:
        return len(LinkModel.objects.filter(user=user, **kwargs))

    @staticmethod
    def _group_count(user: User, **kwargs) -> int:
        return len(GroupLinkModel.objects.filter(user=user, **kwargs))

    @classmethod
    def link_info(cls, user: User, slug: str) -> type[LinkDetailStatistics]:
        if not cls._is_exists(LinkModel, user=user, slug=slug):
            raise ValueError("Link not found")
        queryset = StatisticsModel.objects.filter(link__user=user, link__slug=slug)
        data: dict = cls._from_queryset(queryset)
        return LinkDetailStatistics(**data)

    @classmethod
    def group_info(cls, user: User, group_id: int) -> type[GroupDetailStatistics]:
        if not cls._is_exists(GroupLinkModel, user=user, id=group_id):
            raise ValueError("Group not found")
        queryset = StatisticsModel.objects.filter(
            link__user=user,
            link__group__id=group_id,
        )
        links = cls._link_count(user=user, group=group_id)
        data: dict = cls._from_queryset(queryset)
        data.update({"links": links})
        return GroupDetailStatistics(**data)

    @classmethod
    def account_info(cls, user: User) -> type[AccountDetailStatistics]:
        queryset = StatisticsModel.objects.filter(link__user=user)
        data: dict = cls._from_queryset(queryset)
        links = cls._link_count(user=user)
        groups = cls._group_count(user=user)
        data.update({"links": links, "groups": groups})
        return AccountDetailStatistics(**data)

    @classmethod
    @sync_to_async
    def async_link_info(cls, *args):
        return cls.link_info(*args)

    @classmethod
    @sync_to_async
    def async_group_info(cls, *args):
        return cls.group_info(*args)

    @classmethod
    @sync_to_async
    def async_account_info(cls, *args):
        return cls.account_info(*args)
