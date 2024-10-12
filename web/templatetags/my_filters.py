# templatetags/my_filters.py

from django import template
from web.models import District

register = template.Library()

# Custom filter to get district by primary key
@register.filter(name='get_obj_by_pk')
def get_obj_by_pk(queryset, pk):
    try:
        return queryset.get(pk=int(pk))
    except (ValueError, queryset.model.DoesNotExist):
        return None

