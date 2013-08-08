# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from vkontakte_groups_statistic.models import GroupStat, GroupStatPercentage, VkontakteDeniedAccessError
from models import Group
from forms import GroupImportStatisticForm, GroupImportPostsForm
import re
import logging

def import_posts(request, redirect_url_name=None, form_class=GroupImportPostsForm):

    context = {
        'message': '',
    }

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            group = form.save()
            if redirect_url_name:
                try:
                    return HttpResponseRedirect(reverse(redirect_url_name, args=('vk', group.id)))
                except:
                    context['message'] = u'Сообщения группы импортированы успешно'
    else:
        form = form_class()

    context['form'] = form

    return render_to_response('vkontakte_groups/import_group_posts.html', context, context_instance=RequestContext(request))