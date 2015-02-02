from django.conf import settings
from django.db import models
from vkontakte_api.utils import get_improperly_configured_field


class UserableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_users' in settings.INSTALLED_APPS:
        from vkontakte_users.models import User
        users = models.ManyToManyField(User)
    else:
        users = get_improperly_configured_field('vkontakte_users', True)


class PhotableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_photos' in settings.INSTALLED_APPS:
#           photoalbums = generic.GenericRelation(
#             Album, content_type_field='author_content_type',
#             object_id_field='author_id', verbose_name=u'Photoalbums')
        photoalbums = get_improperly_configured_field('vkontakte_photos', True)

        def photos(self):
            from vkontakte_photos.models import Photo
            return Photo.objects.filter(remote_id__startswith='-%s_' % self.remote_id)

        def fetch_photoalbums(self, *args, **kwargs):
            from vkontakte_photos.models import Album
            return Album.remote.fetch(group=self, *args, **kwargs)

    else:

        photoalbums = get_improperly_configured_field('vkontakte_photos', True)
        photos = get_improperly_configured_field('vkontakte_photos', True)
        fetch_photoalbums = get_improperly_configured_field('vkontakte_photos')


class VideoableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_video' in settings.INSTALLED_APPS:

        videoalbums = get_improperly_configured_field('vkontakte_video', True)
        videos = get_improperly_configured_field('vkontakte_video', True)
        # becouse of this line command
        # ./manage.py sqlflush | grep facebook_photos
        # outputs wrong column
        # SELECT setval(pg_get_serial_sequence('"facebook_photos_album"','id'), 1, false);
    #     videoalbums = generic.GenericRelation(
    #         Album, content_type_field='owner_content_type', object_id_field='owner_id', verbose_name=u'Videoalbums')
    #     videos = generic.GenericRelation(
    #         Video, content_type_field='owner_content_type', object_id_field='owner_id', verbose_name=u'Videos')

        def fetch_videoalbums(self, *args, **kwargs):
            from vkontakte_video.models import Album
            return Album.remote.fetch(owner=self, *args, **kwargs)

        def fetch_videos(self, *args, **kwargs):
            from vkontakte_video.models import Video
            return Video.remote.fetch(owner=self, *args, **kwargs)
    else:

        videoalbums = get_improperly_configured_field('vkontakte_video', True)
        videos = get_improperly_configured_field('vkontakte_video', True)
        fetch_videoalbums = get_improperly_configured_field('vkontakte_video')


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
