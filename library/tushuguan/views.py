# coding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf

from tushuguan.models import *
import datetime, hashlib

'''自动跳转到登陆页
arguments:request
'''
def auto_index(request):
    return HttpResponseRedirect('index/')

'''登录页
arguments:request,
'''
def index_page(request):
    c={}
    return render_to_response('tushuguan/entry.html',c)
