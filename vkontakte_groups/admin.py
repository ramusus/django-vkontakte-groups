# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from vkontakte_api.admin import VkontakteModelAdmin
from django import forms
from models import Group

class GroupAdmin(VkontakteModelAdmin):

    def image_preview(self, obj):
        return u'<a href="%s"><img src="%s" height="30" /></a>' % (obj.photo_big, obj.photo)
    image_preview.short_description = u'Картинка'
    image_preview.allow_tags = True

    search_fields = ('name',)
    list_display = ('image_preview','name','screen_name','type')
    list_display_links = ('name','screen_name')
    list_filter = ('type','is_closed','is_admin')

    exclude = ('users',)

admin.site.register(Group, GroupAdmin)