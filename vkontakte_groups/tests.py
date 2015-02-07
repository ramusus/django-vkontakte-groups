# -*- coding: utf-8 -*-
import mock
import simplejson as json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from vkontakte_users.tests import user_fetch_mock

from .factories import GroupFactory
from .models import Group

GROUP_ID = 30221121
GROUP_SCREEN_NAME = 'volkswagen_jm'
GROUP_NAME = 'Volkswagen'


class VkontakteGroupsTest(TestCase):

    def test_refresh_group(self):

        instance = Group.remote.fetch(ids=[GROUP_ID])[0]
        self.assertEqual(instance.screen_name, GROUP_SCREEN_NAME)

        instance.screen_name = 'temp'
        instance.save()
        self.assertEqual(instance.screen_name, 'temp')

        instance.refresh()
        self.assertEqual(instance.screen_name, GROUP_SCREEN_NAME)

    def test_fetch_groups(self):

        self.assertEqual(Group.objects.count(), 0)
        instance = Group.remote.fetch(ids=[GROUP_ID])[0]

        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(instance.remote_id, GROUP_ID)
        self.assertEqual(instance.screen_name, GROUP_SCREEN_NAME)
        self.assertGreater(instance.members_count, 0)

    def test_parse_group(self):

        response = '''
            {"response":[{"gid":1,"name":"ВКонтакте API","screen_name":"apiclub","is_closed":0,
                "is_admin":1,"type":"group","photo":"http://cs400.vkontakte.ru/g00001/e_5ba03323.jpg",
                "photo_medium":"http://cs400.vkontakte.ru/g00001/d_7bfe2183.jpg",
                "photo_big":"http://cs400.vkontakte.ru/g00001/a_9a5cd502.jpg",
                "members_count":3168},
                {"gid":45,"name":"›››› ФМЛ 239 ››››","screen_name":"fml239","is_closed":1,"is_admin":0,"type":"group",
                "photo":"http://cs39.vkontakte.ru/g00045/c_5a38eec.jpg",
                "photo_medium":"http://cs39.vkontakte.ru/g00045/b_5a38eec.jpg",
                "photo_big":"http://cs39.vkontakte.ru/g00045/a_5a38eec.jpg"}]}
            '''
        instance = Group()
        instance.parse(json.loads(response)['response'][0])
        instance.save()

        self.assertEqual(instance.remote_id, 1)
        self.assertEqual(instance.name, u'ВКонтакте API')
        self.assertEqual(instance.screen_name, 'apiclub')
        self.assertEqual(instance.is_closed, False)
        self.assertEqual(instance.is_admin, True)
        self.assertEqual(instance.members_count, 3168)
        self.assertEqual(instance.type, 'group')
        self.assertEqual(instance.photo, 'http://cs400.vkontakte.ru/g00001/e_5ba03323.jpg')
        self.assertEqual(instance.photo_medium, 'http://cs400.vkontakte.ru/g00001/d_7bfe2183.jpg')
        self.assertEqual(instance.photo_big, 'http://cs400.vkontakte.ru/g00001/a_9a5cd502.jpg')

    def test_search_groups(self):

        self.assertEqual(Group.objects.count(), 0)
        groups = Group.remote.search(q=GROUP_NAME)

        self.assertTrue(len(groups) > 1)

    def test_raise_users_exception(self):

        group = GroupFactory(remote_id=GROUP_ID)
        try:
            group.users
            assert False
        except ImproperlyConfigured, e:
            pass

    if 'vkontakte_users' in settings.INSTALLED_APPS:

        @mock.patch('vkontakte_users.models.User.remote._fetch', side_effect=user_fetch_mock)
        def test_fetch_group_members(self, fetch):
            from vkontakte_users.models import User

            group = GroupFactory(remote_id=GROUP_ID)

            self.assertEqual(User.objects.count(), 0)
            self.assertEqual(group.members.versions.count(), 0)

            users = group.update_members()

            self.assertTrue(group.members_count > 3100)
            self.assertEqual(group.members_count, User.objects.count())
            self.assertEqual(group.members_count, users.count())
            self.assertEqual(group.members_count, group.members.count())

            self.assertEqual(group.members.versions.count(), 1)

            version = group.members.versions.all()[0]

            self.assertEqual(version.added_count, 0)
            self.assertEqual(version.removed_count, 0)
