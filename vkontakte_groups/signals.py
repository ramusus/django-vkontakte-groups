from django.conf import settings
from django.dispatch import receiver
from m2m_history.signals import m2m_history_changed

from .models import Group

if 'vkontakte_users' in settings.INSTALLED_APPS:
    from vkontakte_users.signals import users_to_fetch

    @receiver(m2m_history_changed, sender=Group.members.through)
    def fetch_new_users_members(sender, action, instance, reverse, pk_set, field_name, time, **kwargs):

        if action == 'post_add':
            versions = getattr(instance, field_name).versions
            initial = versions.count() == 1
            version = versions.get(time=time)
            new_ids = version.items(only_pk=True) if initial else version.added(only_pk=True)
            new_ids = list(new_ids)

            users_to_fetch.send(sender=sender, ids=new_ids)
