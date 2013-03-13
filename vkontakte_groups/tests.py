# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Group
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

    def test_search_groups(self):

        self.assertEqual(Group.objects.count(), 0)
        groups = Group.remote.search(q=GROUP_NAME)

        self.assertTrue(len(groups) > 1)