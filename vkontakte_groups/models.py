# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _
from django.core.exceptions import MultipleObjectsReturned, ImproperlyConfigured
from django.conf import settings
from vkontakte_api import fields
from vkontakte_api.utils import api_call
from vkontakte_api.models import VkontakteManager, VkontakteModel, VkontakteIDModel, VkontakteDeniedAccessError, VkontakteContentError
from datetime import datetime
from urllib import unquote
import logging
import re
import simplejson as json

log = logging.getLogger('vkontakte_groups')

GROUP_TYPE_CHOICES = (
    ('group', u'Группа'),
    ('page', u'Страница'),
    ('event', u'Событие'),
)

class GroupRemoteManager(VkontakteManager):

    def api_call(self, *args, **kwargs):
        if 'ids' in kwargs:
            kwargs['gids'] = ','.join(map(lambda i: str(i), kwargs.pop('ids')))
        return super(GroupRemoteManager, self).api_call(*args, **kwargs)

    def search(self, q, offset=None, count=None):

        kwargs = {'q': q}
        if offset:
            kwargs.update(offset=offset)
        if count:
            kwargs.update(count=count)

        return self.get(method='search', **kwargs)

class Group(VkontakteIDModel):
    class Meta:
        db_table = 'vkontakte_groups_group'
        verbose_name = _('Vkontakte group')
        verbose_name_plural = _('Vkontakte groups')
        ordering = ['name']

    methods_namespace = 'groups'
    remote_pk_field = 'gid'
    slug_prefix = 'club'

    name = models.CharField(max_length=800)
    screen_name = models.CharField(u'Короткое имя группы', max_length=50, db_index=True)
    is_closed = models.BooleanField(u'Флаг закрытой группы')
    is_admin = models.BooleanField(u'Пользователь является администратором')
    type = models.CharField(u'Тип объекта', max_length=10, choices=GROUP_TYPE_CHOICES)

    photo = models.URLField()
    photo_big = models.URLField()
    photo_medium = models.URLField()

    remote = GroupRemoteManager(remote_pk=('remote_id',), methods={
        'get': 'getById',
        'search': 'search',
    })

    def __unicode__(self):
        return self.name

    def remote_link(self):
        return 'http://vk.com/club%d' % self.remote_id

    @property
    def wall_comments(self):
        if 'vkontakte_wall' in settings.INSTALLED_APPS:
            from vkontakte_wall.models import Comment
            return Comment.objects.filter(remote_id__startswith='-%s_' % self.remote_id)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

    @property
    def topics_comments(self):
        if 'vkontakte_board' in settings.INSTALLED_APPS:
            from vkontakte_board.models import Comment
            return Comment.objects.filter(remote_id__startswith='-%s_' % self.remote_id)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_board' not in INSTALLED_APPS")

    @property
    def photos(self):
        if 'vkontakte_photos' in settings.INSTALLED_APPS:
            from vkontakte_photos.models import Photo
            return Photo.objects.filter(remote_id__startswith='-%s_' % self.remote_id)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_photos' not in INSTALLED_APPS")

    def fetch_posts(self, *args, **kwargs):
        if 'vkontakte_wall' in settings.INSTALLED_APPS:
            from vkontakte_wall.models import Post
            return Post.remote.fetch_group_wall(self, *args, **kwargs)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

    def fetch_albums(self, *args, **kwargs):
        if 'vkontakte_photos' in settings.INSTALLED_APPS:
            from vkontakte_photos.models import Album
            return Album.remote.fetch(group=self, *args, **kwargs)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_photos' not in INSTALLED_APPS")

    def fetch_topics(self, *args, **kwargs):
        if 'vkontakte_board' in settings.INSTALLED_APPS:
            from vkontakte_board.models import Topic
            return Topic.remote.fetch(group=self, *args, **kwargs)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_board' not in INSTALLED_APPS")

    def update_statistic(self, *args, **kwargs):
        if 'vkontakte_groups_statistic' in settings.INSTALLED_APPS:
            from vkontakte_groups_statistic.models import update_statistic_for_group
            return update_statistic_for_group(group=self, *args, **kwargs)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_groups_statistic' not in INSTALLED_APPS")

    def update_users(self, *args, **kwargs):
        if 'vkontakte_groups_migration' in settings.INSTALLED_APPS:
            from vkontakte_groups_migration.models import GroupMigration
            return GroupMigration.objects.update_for_group(group=self, *args, **kwargs)
        else:
            raise ImproperlyConfigured("Application 'vkontakte_groups_migration' not in INSTALLED_APPS")

if 'vkontakte_users' in settings.INSTALLED_APPS:
    from vkontakte_users.models import User
    Group.add_to_class('users', models.ManyToManyField(User))
else:
    @property
    def users(self):
        raise ImproperlyConfigured("Application 'vkontakte_users' not in INSTALLED_APPS")
    Group.add_to_class('users', users)