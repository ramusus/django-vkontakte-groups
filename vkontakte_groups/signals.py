# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.conf import settings
from annoying.decorators import signals
from models import Group
from tasks import VkontakteGroupUpdateUsersM2M

group_users_updated = Signal(providing_args=['instance', 'ids'])

@signals(group_users_updated, sender=Group)
def group_users_update_m2m(sender, instance, **kwargs):
    if 'djcelery' in settings.INSTALLED_APPS:
        return VkontakteGroupUpdateUsersM2M.delay(instance)
    else:
        instance.update_users_m2m()