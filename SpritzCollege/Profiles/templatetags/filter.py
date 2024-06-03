from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    
    if user.is_superuser:
        return True
    
    if user.groups.filter(name="administration").exists():
        return True
    
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False