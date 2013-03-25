# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Group
from datetime import datetime, timedelta

class GroupImportForm(forms.Form):
    group_url = forms.CharField(label=_(u'URL группы Вконтакте'))

    def clean_group_url(self):
        try:
            return Group.remote.get_by_url(self.cleaned_data['group_url'])
        except ValueError, e:
            raise forms.ValidationError(e)

    def save(self):
        group = self.cleaned_data['group_url']
        group = Group.remote.fetch(ids=[group.remote_id])[0]
        return group

class GroupImportStatisticForm(GroupImportForm):
    def save(self, *args, **kwargs):
        group = super(GroupImportStatisticForm, self).save(*args, **kwargs)
        group.fetch_statistic()
        return group

class GroupImportPostsForm(GroupImportForm):
    def save(self, *args, **kwargs):
        group = super(GroupImportPostsForm, self).save(*args, **kwargs)
        for post in group.fetch_posts(after=datetime.now()-timedelta(days=30)):
            post.fetch_comments()
            post.update_reposts()
            post.update_likes()
        return group