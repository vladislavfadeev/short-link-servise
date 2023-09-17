from datetime import datetime

from django_filters import (
    FilterSet,
    BooleanFilter,
    ChoiceFilter,
    DateFilter,
    ModelChoiceFilter,
)
from django_filters.widgets import CSVWidget
from django.db.models import Count
from django import forms

from apps.db_model.models import GroupLinkModel, LinkModel


def out_of_date_filter(queryset, name, value):
    if isinstance(value, bool) and value:
        lookup = "__".join([name, "lte"])
        return queryset.filter(**{lookup: datetime.now()})
    return queryset


def boolean_filter(queryset, name, value):
    if isinstance(value, bool) and value:
        return queryset.filter(**{name: value})
    return queryset


class LinksFilter(FilterSet):
    ORDER_CHOICE = (
        ("discending_date", "Сначала старые"),
        ("ascending_clicks", "По убыванию кликов [10 --> 0]"),
        ("discending_clicks", "По возрастанию кликов [0 --> 10]"),
    )
    ORDER_PARAMS = {
        "discending_date": "date_created",
        "ascending_clicks": "-clicks",
        "discending_clicks": "clicks",
    }

    def group_choice(request):
        if request is None:
            return GroupLinkModel.objects.none()
        return request.user.link_groups.all()

    def filter_by_order(self, queryset, name, value):
        expr = self.ORDER_PARAMS.get(value)
        if expr is not None and "date" in expr:
            return queryset.order_by(expr)
        elif expr is not None and "clicks" in expr:
            return queryset.annotate(clicks=Count("statistics")).order_by(
                expr, "-date_created"
            )
        return queryset.order_by("-date_created")

    disabled = BooleanFilter(
        field_name="disabled",
        method=boolean_filter,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    out_of_date = BooleanFilter(
        field_name="date_expire",
        method=out_of_date_filter,
        lookup_expr="lte",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    sort = ChoiceFilter(
        choices=ORDER_CHOICE,
        empty_label="Сначала новые",
        method="filter_by_order",
        widget=forms.Select(attrs={"class": "form-control mt-1"}),
    )
    date_from = DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        widget=CSVWidget(attrs={"class": "form-control mt-1", "type": "date"}),
    )
    date_to = DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        widget=CSVWidget(attrs={"class": "form-control mt-1", "type": "date"}),
    )
    group = ModelChoiceFilter(
        queryset=group_choice,
        empty_label="Выберите группу..",
        widget=forms.Select(attrs={"class": "form-control mt-1"}),
    )

    class Meta:
        model = LinkModel
        fields = ["disabled", "group"]


class GroupFilter(FilterSet):
    ORDER_CHOICE = (
        ("discending_date", "Сначала старые"),
        ("ascending_clicks", "По убыванию кликов [10 --> 0]"),
        ("discending_clicks", "По возрастанию кликов [0 --> 10]"),
        ("ascending_links", "По объему ссылок [10 --> 0]"),
        ("discending_links", "По объему ссылок [0 --> 10]"),
    )
    ORDER_PARAMS = {
        "discending_date": "date_created",
        "ascending_clicks": "-clicks",
        "discending_clicks": "clicks",
        "ascending_links": "-links",
        "discending_links": "links",
    }

    def is_private_filter(self, queryset, name, value):
        if isinstance(value, bool) and value:
            lookup = "__".join([name, "isnull"])
            return queryset.filter(**{lookup: False})
        return queryset

    def filter_by_order(self, queryset, name, value):
        expr = self.ORDER_PARAMS.get(value)
        if "date" in expr:
            return queryset.order_by(expr)
        elif "clicks" in expr:
            return queryset.annotate(clicks=Count("linkmodel__statistics")).order_by(
                expr, "-date_created"
            )
        elif "links" in expr:
            return queryset.annotate(links=Count("linkmodel")).order_by(
                expr, "-date_created"
            )
        return queryset.order_by("-date_created")

    disabled = BooleanFilter(
        field_name="disabled",
        method=boolean_filter,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    out_of_date = BooleanFilter(
        field_name="date_expire",
        method=out_of_date_filter,
        lookup_expr="lte",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    date_from = DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        widget=CSVWidget(attrs={"class": "form-control mt-1", "type": "date"}),
    )
    date_to = DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        widget=CSVWidget(attrs={"class": "form-control mt-1", "type": "date"}),
    )
    sort = ChoiceFilter(
        choices=ORDER_CHOICE,
        empty_label="Сначала новые",
        method="filter_by_order",
        widget=forms.Select(attrs={"class": "form-control mt-1"}),
    )
    private = BooleanFilter(
        field_name="password",
        method="is_private_filter",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    rotation = BooleanFilter(
        field_name="rotation",
        method=boolean_filter,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = GroupLinkModel
        fields = ["rotation", "disabled"]
