# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Group, GroupStat, GroupStatistic, GroupStatMembers
from vkontakte_users.factories import UserFactory
import simplejson as json

GROUP_ID = 30221121
GROUP_NAME = 'Volkswagen'

class VkontakteGroupsTest(TestCase):

    def test_fetch_groups(self):

        self.assertEqual(Group.objects.count(), 0)
        Group.remote.fetch(ids=[GROUP_ID])

        self.assertEqual(Group.objects.count(), 1)

    def test_parse_group(self):

        response = '''
            {"response":[{"gid":1,"name":"ВКонтакте API","screen_name":"apiclub","is_closed":0,
                "is_admin":1,"type":"group","photo":"http://cs400.vkontakte.ru/g00001/e_5ba03323.jpg",
                "photo_medium":"http://cs400.vkontakte.ru/g00001/d_7bfe2183.jpg",
                "photo_big":"http://cs400.vkontakte.ru/g00001/a_9a5cd502.jpg"},
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
        self.assertEqual(instance.type, 'group')
        self.assertEqual(instance.photo, 'http://cs400.vkontakte.ru/g00001/e_5ba03323.jpg')
        self.assertEqual(instance.photo_medium, 'http://cs400.vkontakte.ru/g00001/d_7bfe2183.jpg')
        self.assertEqual(instance.photo_big, 'http://cs400.vkontakte.ru/g00001/a_9a5cd502.jpg')

    def test_fetch_statistic(self):

        group = Group.objects.create(remote_id=GROUP_ID)
        self.assertEqual(GroupStat.objects.count(), 0)

        group.update_statistic()
        self.assertNotEqual(GroupStat.objects.count(), 0)

        stat = GroupStat.objects.all()[0]
        self.assertTrue(stat.members > 0)
        self.assertTrue(stat.views > 0)
        self.assertTrue(stat.visitors > 0)
        self.assertTrue(stat.males > 0)
        self.assertTrue(stat.females > 0)
        self.assertNotEqual(stat.date, None)

    def test_fetch_statistic_via_api(self):

        group = Group.objects.create(remote_id=GROUP_ID)
        self.assertEqual(GroupStatistic.objects.count(), 0)

        group.update_statistic(api=True)
        self.assertNotEqual(GroupStatistic.objects.count(), 0)

        stat = GroupStatistic.objects.all()[0]
        self.assertTrue(stat.views > 0)
        self.assertTrue(stat.visitors > 0)
        self.assertTrue(stat.males > 0)
        self.assertTrue(stat.females > 0)
        self.assertNotEqual(stat.date, None)

    def test_search_groups(self):

        self.assertEqual(Group.objects.count(), 0)
        groups = Group.remote.search(q=GROUP_NAME)

        self.assertTrue(len(groups) > 1)

    def test_group_migration(self):

        for i in range(1,7):
            UserFactory.create(remote_id=i)
        group = Group.objects.create(remote_id=GROUP_ID)
        stat1 = GroupStatMembers.objects.create(group=group, members=',1,2,3,4,5,')
        stat1.save_final()
        stat2 = GroupStatMembers.objects.create(group=group, members='1,2,3,4,6')
        stat2.save_final()
        stat3 = GroupStatMembers.objects.create(group=group, members='1,2,3,5,7')
        stat3.save_final()

        self.assertEqual(stat1.members, '1,3,2,5,4')
        self.assertEqual(sorted(stat1.members_ids), sorted([int(i) for i in '1,2,3,4,5'.split(',')]))
        self.assertEqual(sorted(stat2.members_ids), sorted([int(i) for i in '1,2,3,4,6'.split(',')]))
        self.assertEqual(sorted(stat3.members_ids), sorted([int(i) for i in '1,2,3,5,7'.split(',')]))
        self.assertEqual(stat2.members_entered_ids, [6])
        self.assertEqual(stat2.members_left_ids, [5])
        self.assertEqual(stat3.members_entered_ids, [5,7])
        self.assertEqual(stat3.members_left_ids, [4,6])

        stat2.delete()
        stat3 = GroupStatMembers.objects.get(id=stat3.id)

        self.assertEqual(stat3.members_entered_ids, [7])
        self.assertEqual(stat3.members_left_ids, [4])