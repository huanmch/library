# coding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf

from tushuguan.queryset import *
from tushuguan.mix import *
from tushuguan.models import *
import datetime, hashlib

'''自动跳转到登陆页
arguments:request
'''
def auto_index(request):
    return HttpResponseRedirect('entry/')

'''登录页
arguments:request,
'''
def index_page(request):
    c={}
    return render_to_response('tushuguan/entry.html',c)

@csrf_exempt
def ajax_index_page(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    result = local_password_enter(username, password)
    if result == 'T':
        request.session['stuid']=username
        return HttpResponse('0')
    else:
        outer_result = outer_password_enter(username, password)
        #0正确
        if outer_result==0:
            request.session['stuid']=username
            return HttpResponse('0')
        #1用户未认证或密码错误
        elif outer_result==1:
            return HttpResponse('1')
        #2用户名不存在
        elif outer_result==2:
            return HttpResponse('2')
        #3内部错误
        elif outer_result==3:
            return HttpResponse('3')
        else:
            return HttpResponse('XXX')

'''
注册页
arguments:request
'''
def register_page(request):
    c = {}
    return render_to_response('tushuguan/registration.html', c)

'''
导航页
arguments:request
'''
def nav_page(request):
    c = {}
    result=judge_islogin(request,c)
    if result=='T':
        return render_to_response('tushuguan/nav.html', c)
    else:
        return HttpResponseRedirect('../index/')

'''
借书页
arguments:request
'''
def borrow_page(request):
    c ={}
    result=judge_islogin(request,c)
    if result=='T':
        return render_to_response('tushuguan/borrow.html', c)
    else:
        return HttpResponseRedirect('../index/')
