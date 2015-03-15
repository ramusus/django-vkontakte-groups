from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from m2m_history.models import ManyToManyHistoryVersion

from .models import Group

if 'vkontakte_users' in settings.INSTALLED_APPS:
    from vkontakte_users.signals import users_to_fetch

    @receiver(post_save, sender=ManyToManyHistoryVersion)
    def fetch_new_users_members(sender, instance, created, **kwargs):

        if instance.content_type.pk == ContentType.objects.get_for_model(Group).pk \
                and instance.field_name == 'members' and created:
            versions = getattr(instance.object, instance.field_name).versions
            new_ids = instance.items(only_pk=True) if versions.count() == 1 else instance.added(only_pk=True)
            new_ids = list(new_ids)

            users_to_fetch.send(sender=sender, ids=new_ids)
