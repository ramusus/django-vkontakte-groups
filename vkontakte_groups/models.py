# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _
from django.core.exceptions import MultipleObjectsReturned, ImproperlyConfigured
from django.conf import settings
from vkontakte_api import fields
from vkontakte_api.models import VkontakteManager, VkontakteModel, VkontaktePKModel, VkontakteDeniedAccessError, VkontakteContentError
from datetime import datetime
from urllib import unquote
import logging
import re
import simplejson as json

log = logging.getLogger('vkontakte_groups')

GROUP_TYPE_CHOICES = (
    ('group',  u'Группа'),
    ('page',  u'Страница'),
    ('event',  u'Событие'),
)

class ParseGroupsMixin(object):
    '''
    Manager mixin for parsing response with extra cache 'groups'. Used in vkontakte_wall applications
    '''
    def parse_response_groups(self, response_list):
        users = Group.remote.parse_response_list(response_list.get('groups', []), {'fetched': datetime.now()})
        instances = []
        for instance in users:
            instances += [Group.remote.get_or_create_from_instance(instance)]
        return instances

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

class Group(VkontaktePKModel):
    class Meta:
        verbose_name = _('Vkontakte group')
        verbose_name_plural = _('Vkontakte groups')

    resolve_screen_name_type = 'group'
    methods_namespace = 'groups'
    remote_pk_field = 'gid'
    slug_prefix = 'club'

    name = models.CharField(max_length=800)
    screen_name = models.CharField(u'Короткое имя группы', max_length=50, db_index=True)
    is_closed = models.NullBooleanField(u'Флаг закрытой группы')
    is_admin = models.NullBooleanField(u'Пользователь является администратором')
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
    def refresh_kwargs(self):
        return {'ids': [self.remote_id]}

    @property
    def wall_comments(self):
        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

        from vkontakte_wall.models import Comment
        # TODO: improve schema and queries with using owner_id field
        return Comment.objects.filter(remote_id__startswith='-%s_' % self.remote_id)

    @property
    def topics_comments(self):
        if 'vkontakte_board' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_board' not in INSTALLED_APPS")

        from vkontakte_board.models import Comment
        # TODO: improve schema and queries with using owner_id field
        return Comment.objects.filter(remote_id__startswith='-%s_' % self.remote_id)

    @property
    def photos(self):
        if 'vkontakte_photos' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_photos' not in INSTALLED_APPS")

        from vkontakte_photos.models import Photo
        # TODO: improve schema and queries with using owner_id field
        return Photo.objects.filter(remote_id__startswith='-%s_' % self.remote_id)

    def fetch_posts(self, *args, **kwargs):
        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

        from vkontakte_wall.models import Post
        return Post.remote.fetch_wall(owner=self, *args, **kwargs)

    def fetch_albums(self, *args, **kwargs):
        if 'vkontakte_photos' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_photos' not in INSTALLED_APPS")

        from vkontakte_photos.models import Album
        return Album.remote.fetch(group=self, *args, **kwargs)

    def fetch_topics(self, *args, **kwargs):
        if 'vkontakte_board' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_board' not in INSTALLED_APPS")

        from vkontakte_board.models import Topic
        return Topic.remote.fetch(group=self, *args, **kwargs)

    def fetch_statistic(self, *args, **kwargs):
        if 'vkontakte_groups_statistic' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_groups_statistic' not in INSTALLED_APPS")

        from vkontakte_groups_statistic.models import fetch_statistic_for_group
        return fetch_statistic_for_group(group=self, *args, **kwargs)

    def update_users(self, *args, **kwargs):
        if 'vkontakte_groups_migration' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_groups_migration' not in INSTALLED_APPS")

        from vkontakte_groups_migration.models import GroupMigration
        return GroupMigration.objects.update_for_group(group=self, *args, **kwargs)

if 'vkontakte_users' in settings.INSTALLED_APPS:
    from vkontakte_users.models import User
    Group.add_to_class('users', models.ManyToManyField(User))
else:
    @property
    def users(self):
        raise ImproperlyConfigured("Application 'vkontakte_users' not in INSTALLED_APPS")
    Group.add_to_class('users', users)