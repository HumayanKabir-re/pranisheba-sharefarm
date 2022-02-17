import django_filters
from rest_framework import request
from django.contrib.admin import SimpleListFilter
from .models import *
from django.utils.translation import gettext_lazy as _


class HelpfulFilterSet(django_filters.FilterSet):
    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        filter = super(HelpfulFilterSet, cls).filter_for_field(f, name, lookup_expr)
        filter.extra['help_text'] = f.help_text
        return filter


class FaqItemListFilter(HelpfulFilterSet):
    # director = django_filters.CharFilter(name='relationship__name', lookup_expr='contains')
    # before_release = django_filters.NumberFilter(field_name='publishing_year', lookup_expr=('lte'),
    #                                              help_text='Before what year? to get all the movies')
    # after_release = django_filters.NumberFilter(field_name='publishing_year', lookup_expr=('gte'),
    #                                             help_text='After what year? to get all the movies')

    class Meta:
        model = FaqItem
        fields = ['category', ]
