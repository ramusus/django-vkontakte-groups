# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime
from urllib import unquote

import simplejson as json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from vkontakte_api import fields
from vkontakte_api.decorators import fetch_all
from vkontakte_api.models import (VkontakteContentError,
                                  VkontakteDeniedAccessError, VkontakteManager,
                                  VkontakteModel, VkontaktePKModel)

from .mixins import (ParseGroupsMixin, PhotableModelMixin, UserableModelMixin,
                     VideoableModelMixin)

log = logging.getLogger('vkontakte_groups')

GROUP_TYPE_CHOICES = (
    ('group',  u'Группа'),
    ('page',  u'Страница'),
    ('event',  u'Событие'),
)


class GroupRemoteManager(VkontakteManager):

    def api_call(self, *args, **kwargs):
        if 'ids' in kwargs:
            kwargs['group_ids'] = ','.join(map(lambda i: str(i), kwargs.pop('ids')))
        return super(GroupRemoteManager, self).api_call(*args, **kwargs)

    def search(self, q, offset=None, count=None):

        kwargs = {'q': q}
        if offset:
            kwargs.update(offset=offset)
        if count:
            kwargs.update(count=count)

        return self.get(method='search', **kwargs)

    def fetch(self, *args, **kwargs):
        '''
        Add additional fields to parent fetch request
        '''
        if 'fields' not in kwargs:
            kwargs['fields'] = 'members_count'
        return super(GroupRemoteManager, self).fetch(*args, **kwargs)

    @fetch_all(always_all=True)
    def get_members_ids(self, group, **kwargs):
        kwargs['group_id'] = group.remote_id
        return self.api_call('get_members', **kwargs)


@python_2_unicode_compatible
class Group(PhotableModelMixin, VideoableModelMixin, UserableModelMixin, VkontaktePKModel):

    resolve_screen_name_types = ['group', 'page', 'event']
    slug_prefix = 'club'

    name = models.CharField(max_length=800)
    screen_name = models.CharField(u'Короткое имя группы', max_length=50, db_index=True)
    is_closed = models.NullBooleanField(u'Флаг закрытой группы')
    is_admin = models.NullBooleanField(u'Пользователь является администратором')
    members_count = models.IntegerField(u'Всего участников', null=True)
    verified = models.NullBooleanField(u'Флаг официальной группы')
    type = models.CharField(u'Тип объекта', max_length=10, choices=GROUP_TYPE_CHOICES)

    photo = models.URLField()
    photo_big = models.URLField()
    photo_medium = models.URLField()

    remote = GroupRemoteManager(remote_pk=('remote_id',), methods_namespace='groups', version=5.28, methods={
        'get': 'getById',
        'search': 'search',
        'get_members': 'getMembers',
    })

    class Meta:
        verbose_name = _('Vkontakte group')
        verbose_name_plural = _('Vkontakte groups')

    def __str__(self):
        return self.name

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

    def fetch_posts(self, *args, **kwargs):
        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

        from vkontakte_wall.models import Post
        return Post.remote.fetch_wall(owner=self, *args, **kwargs)

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
