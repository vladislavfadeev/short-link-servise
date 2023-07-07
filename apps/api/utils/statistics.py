from asgiref.sync import sync_to_async

from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from fastapi import HTTPException

from apps.db_model.models import GroupLinkModel, LinkModel, StatisticsModel


User = get_user_model()


class Statistics():
    
    @staticmethod
    def _from_queryset(queryset: QuerySet) -> dict:
        
        clicks = len(queryset)
        if not clicks:
            raise HTTPException(status_code=404, detail='Item not found, or statistics is empty')
        
        device = list(queryset.values('device').annotate(entries=Count('device')).distinct())
        source = list(queryset.values('ref_link').annotate(entries=Count('ref_link')).distinct())
        browser = list(queryset.values('browser').annotate(entries=Count('browser')).distinct())
        date = list(queryset.values('date').annotate(entries=Count('date')).distinct())

        data = {
            'clicks': clicks,
            'device': device,
            'source': source,
            'browser': browser,
            'date': date,
        }
        return data
    
    @staticmethod
    @sync_to_async
    def link_count(user: User, **kwargs) -> int:
        return len(LinkModel.objects.filter(user=user, **kwargs))

    @classmethod
    @sync_to_async
    def link_info(cls, user: User, slug: str) -> dict:
        queryset = StatisticsModel.objects.filter(
            link__user = user,
            link__slug = slug
        )
        data: dict = cls._from_queryset(queryset)
        return data

    @classmethod
    @sync_to_async
    def group_info(cls, user: User, group_id: int) -> dict:
        queryset = StatisticsModel.objects.filter(
            link__user=user,
            link__group__id=group_id,
        )
        links = cls.link_count(user=user, group=group_id)
        data: dict = cls._from_queryset(queryset)
        data.update({'links': links})
        return data

    @classmethod
    @sync_to_async
    def account_info(cls, user: User) -> dict:
        queryset = StatisticsModel.objects.filter(link__user=user)
        data: dict = cls._from_queryset(queryset)
        links = cls.link_count(user=user)
        groups = len(GroupLinkModel.objects.filter(user=user))
        data.update({'links': links, 'groups': groups})
        return data
