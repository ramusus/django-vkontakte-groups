# -*- coding: utf-8 -*-
import mock
import simplejson as json
from django.conf import settings
from django.test import TestCase
from vkontakte_users.tests import user_fetch_mock

from .factories import GroupFactory
from .models import Group, CheckMembersCountFailed

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
            {"response":[{"id":1,"name":"ВКонтакте API","screen_name":"apiclub","is_closed":0,
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

    # def test_raise_users_exception(self):
    #
    # group = GroupFactory(remote_id=GROUP_ID)
    #     try:
    #         group.members
    #         assert False
    #     except ImproperlyConfigured, e:
    #         pass

    if 'vkontakte_users' in settings.INSTALLED_APPS:

        @mock.patch('vkontakte_users.models.User.remote._fetch', side_effect=user_fetch_mock)
        def test_group_add_members_ids_not_users(self, fetch):
            '''
            Without vkontakte_users in apps fetching group members doesn't trigger fetching users
            :param fetch:
            :return:
            '''
            apps = list(settings.INSTALLED_APPS)
            del apps[apps.index('vkontakte_users')]

            from vkontakte_users.models import User

            User.remote.fetch(ids=range(0, 500))

            group = GroupFactory(remote_id=GROUP_ID)
            with self.settings(**dict(INSTALLED_APPS=apps)):
                group.members = range(0, 1000)

            self.assertEqual(group.members.count(), 500)
            self.assertEqual(group.members.get_queryset().count(), 500)
            self.assertEqual(group.members.get_queryset_through().count(), 1000)
            self.assertItemsEqual(group.members.all(), User.objects.all())
            self.assertItemsEqual(group.members.get_queryset(only_pk=True), range(0, 1000))

        @mock.patch('vkontakte_users.models.User.remote._fetch', side_effect=user_fetch_mock)
        def test_fetch_group_members(self, fetch):
            from vkontakte_users.models import User

            group = Group.remote.fetch(ids=[GROUP_ID])[0]

            self.assertEqual(User.objects.count(), 0)
            self.assertEqual(group.members.versions.count(), 0)
            self.assertGreater(group.members_count, 3100)

            with self.settings(**dict(VKONTAKTE_USERS_FETCH_USERS_ASYNC=False)):
                group.update_members()

            self.assertEqual(group.members_count, User.objects.count())
            self.assertEqual(group.members_count, group.members.count())

            self.assertEqual(group.members.versions.count(), 1)

            version = group.members.versions.all()[0]

            self.assertEqual(version.added_count, 0)
            self.assertEqual(version.removed_count, 0)

            group.members_count = 3200
            group.save()
            with self.assertRaises(CheckMembersCountFailed):
                group.update_members()

            group.members_count = 3000
            group.save()
            with self.assertRaises(CheckMembersCountFailed):
                group.update_members()

        @mock.patch('vkontakte_groups.models.GroupRemoteManager.get_members_ids')
        def test_group_members_changes(self, get_members_ids):

            apps = list(settings.INSTALLED_APPS)
            del apps[apps.index('vkontakte_users')]
            with self.settings(**dict(INSTALLED_APPS=apps)):

                group = GroupFactory(remote_id=GROUP_ID)

                def membership(id):
                    return group.members.get_queryset_through().get(user_id=id)

                def memberships(id):
                    return group.members.get_queryset_through().filter(user_id=id).order_by('id')

                def id90_state1():
                    self.assertEqual(membership(90).time_from, None)
                    self.assertEqual(membership(90).time_to, None)

                def id90_state2():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(90).time_from, None)
                    self.assertEqual(membership(90).time_to, versions[1].time)

                def id90_state3():
                    versions = group.members.versions.all()
                    self.assertEqual(memberships(90)[0].time_from, None)
                    self.assertEqual(memberships(90)[0].time_to, versions[1].time)
                    self.assertEqual(memberships(90)[1].time_from, versions[2].time)
                    self.assertEqual(memberships(90)[1].time_to, None)

                def id90_state4():
                    versions = group.members.versions.all()
                    self.assertEqual(memberships(90)[0].time_from, None)
                    self.assertEqual(memberships(90)[0].time_to, versions[1].time)
                    self.assertEqual(memberships(90)[1].time_from, versions[2].time)
                    self.assertEqual(memberships(90)[1].time_to, None)

                def id0_state1():
                    self.assertEqual(memberships(0).count(), 0)

                def id0_state2():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(0).time_from, versions[1].time)
                    self.assertEqual(membership(0).time_to, None)

                def id0_state3():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(0).time_from, versions[1].time)
                    self.assertEqual(membership(0).time_to, versions[2].time)

                id0_state4 = id0_state3

                def id20_state1():
                    self.assertEqual(memberships(20).count(), 0)

                def id20_state2():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(20).time_from, versions[1].time)
                    self.assertEqual(membership(20).time_to, None)

                def id20_state3():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(20).time_from, versions[1].time)
                    self.assertEqual(membership(20).time_to, versions[2].time)

                def id20_state4():
                    versions = group.members.versions.all()
                    self.assertEqual(memberships(20)[0].time_from, versions[1].time)
                    self.assertEqual(memberships(20)[0].time_to, versions[2].time)
                    self.assertEqual(memberships(20)[1].time_from, versions[3].time)
                    self.assertEqual(memberships(20)[1].time_to, None)

                def id40_state1():
                    self.assertEqual(membership(40).time_from, None)
                    self.assertEqual(membership(40).time_to, None)

                id40_state2 = id40_state1

                def id40_state3():
                    self.assertEqual(membership(40).time_from, None)
                    self.assertEqual(membership(40).time_to, None)

                id40_state4 = id40_state3

                def id105_state1():
                    self.assertEqual(memberships(105).count(), 0)

                id105_state2 = id105_state1

                def id105_state3():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(105).time_from, versions[2].time)
                    self.assertEqual(membership(105).time_to, None)

                def id105_state4():
                    versions = group.members.versions.all()
                    self.assertEqual(membership(105).time_from, versions[2].time)
                    self.assertEqual(membership(105).time_to, versions[3].time)

                get_members_ids.side_effect = lambda group, *a, **kw: range(30, 100)
                group.update_members(check_count=False)
                self.assertEqual(group.members.get_queryset_through().count(), 70)
                id0_state1()
                id20_state1()
                id40_state1()
                id90_state1()
                id105_state1()

                get_members_ids.side_effect = lambda group, *a, **kw: range(0, 50)
                group.update_members(check_count=False)
                state_time2 = group.members.last_update_time()
                self.assertEqual(group.members.get_queryset_through().count(), 100)
                id0_state2()
                id20_state2()
                id40_state2()
                id90_state2()
                id105_state2()

                get_members_ids.side_effect = lambda group, *a, **kw: range(30, 110)
                group.update_members(check_count=False)
                state_time3 = group.members.last_update_time()
                self.assertEqual(group.members.get_queryset_through().count(), 160)
                id0_state3()
                id20_state3()
                id40_state3()
                id90_state3()
                id105_state3()

                get_members_ids.side_effect = lambda group, *a, **kw: range(15, 100)
                group.update_members(check_count=False)
                state_time4 = group.members.last_update_time()
                self.assertEqual(group.members.get_queryset_through().count(), 175)
                id0_state4()
                id20_state4()
                id40_state4()
                id90_state4()
                id105_state4()

                # delete middle version
                group.members.versions.get(time=state_time3).delete()
                self.assertEqual(group.members.get_queryset_through().count(), 150)
                id0_state4()
                id20_state2()
                id40_state2()
                id90_state4()
                id105_state2()

                # hide migration4 -> back to state2
                group.members.versions.get(time=state_time4).delete()
                self.assertEqual(group.members.get_queryset_through().count(), 100)
                id0_state2()
                id20_state2()
                id40_state2()
                id90_state2()
                id105_state2()

                # hide migration2 -> back to state1
                group.members.versions.get(time=state_time2).delete()
                self.assertEqual(group.members.get_queryset_through().count(), 70)
                id0_state1()
                id20_state1()
                id40_state1()
                id90_state1()
                id105_state1()
