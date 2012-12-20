# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import GroupStat, Group, GroupStatPersentage, VkontakteDeniedAccessError
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

def import_statistic(request, redirect_url_name=None, form_class=GroupImportStatisticForm):

    context = {
        'message': '',
    }

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                group = form.save()
                if redirect_url_name:
                    try:
                        return HttpResponseRedirect(reverse(redirect_url_name, args=('vk', group.id)))
                    except:
                        context['message'] = u'Статистика группы импортирована успешно'
            except VkontakteDeniedAccessError:
                context['message'] = u'Вы не имеете доступа к статистике группы'
    else:
        form = form_class()

    context['form'] = form

    return render_to_response('vkontakte_groups/import_group_statistic.html', context, context_instance=RequestContext(request))

@csrf_exempt
def import_statistic_via_bookmarklet(request, redirect_url_name=None):

    try:
        m = re.findall(r'http://vk.com/stats\?gid=(\d+)/?', request.POST['url'])
        if not len(m):
            logging.error("Url of vkontakte group statistic should be started with http://vk.com/stats?gid=")
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

    group_id = m[0]
    group = Group.remote.fetch(ids=[group_id])[0]
    GroupStat.objects.parse_statistic_page(group, request.POST['body'])
    GroupStatPersentage.objects.parse_statistic_page(group, request.POST['body'])
    try:
        return HttpResponseRedirect(reverse(redirect_url_name, args=(group.id,)))
    except:
        return HttpResponseRedirect('/')