from django import template
from ..models import CATEGORY_CHOICES

register = template.Library()

@register.filter
def filter_by_category(queryset, category):
    return queryset.filter(category=category)

@register.simple_tag
def get_categories():
    return [choice[0] for choice in CATEGORY_CHOICES]
