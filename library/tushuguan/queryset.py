# coding:utf-8

from django.http import HttpResponse

import urllib2
import urllib
import re
import json
import cookielib
import base64
import hashlib
import datetime

from tushuguan.models import *
from django.db.models import Q

#资源服务器地址前缀
resource_server_urlpre='https://online.sdu.edu.cn/ol_passport/api'
#全局变量
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

'''通行证登陆，使用密码授权模式
参数:username:用户名,password:密码
返回值:0正确,1用户未认证或密码错误,2用户名不存在,3内部错误
'''
def outer_password_enter(username,password):
    scope='realname stuid tel email pwd'
    appname='center_lib'
    appkey='zyh'
    global opener
    #密码认证
    password_postdata = urllib.urlencode({'username':username,
            'password':password,
            'scope':scope,
            'grant_type':'password'})
    pass_req = urllib2.Request(
        url = resource_server_urlpre + '/Access_token.html',
        data = password_postdata
    )
    base64string = base64.encodestring(
        '%s:%s' % (appname, appkey))[:-1]
    authheader =  "Basic %s" % base64string
    pass_req.add_header("Authorization", authheader)
    opener = urllib2.build_opener()
#分析返回数据
    try:
        pass_con=opener.open(pass_req).read()
#400错误
    except urllib2.HTTPError,e:
        error_res=e.read()
        error_res=json.loads(error_res)
        if error_res.has_key('error'):
            error=error_res.get('error','')
            error_description=error_res.get('error_description','')
            #1用户未认证或密码错误
            if error_description=='password error':
                return 1
            #2用户名不存在
            elif error_description=='username error':
                return 2
            #3内部错误
            else:
                return 3
        #3内部错误
        else:
            return 3
#200成功返回
    pass_res=json.loads(pass_con)
    access_token=pass_res.get('access_token','')
    token_type=pass_res.get('token_type','')
    expires_in=pass_res.get('expires_in','')
    refresh_token=pass_res.get('refresh_token','')
#使用令牌(access_token)取资源
    token_postdata = urllib.urlencode({'access_token':access_token,
        'scope':'realname stuid tel email pwd'})
    token_req = urllib2.Request(
        url = resource_server_urlpre + '/Resource.html',
        data = token_postdata
    )
#分析返回数据
    try:
        token_con=opener.open(token_req).read()
#如果400错误
    except urllib2.HTTPError,e:
        #内部错误
        return 3
#200成功返回
    token_res=json.loads(token_con)
    data=token_res.get('data','')
    users(stuid=data.get('stuid',''),code=data.get('pwd',''),
        realname=data.get('realname',''),tel=data.get('tel',''),
        email=data.get('email',''),borrowstate='00',extrainfo='',
        usergroupid=1,state=0).save()
    return 0

'''本地登陆
参数:username用户名，password密码
返回值:T成功,F失败
'''
def local_password_enter(username,password):
    tuser=users.objects.filter(stuid=username)
    #(tuple((tuser[0].code).split('$'))[1]==hashlib.sha1(tuple((tuser[0].code).split('$'))[0] + password).hexdigest())
    if tuser:
        md5 = hashlib.md5()
        md5.update(password+username)
        if tuser[0].code==md5.hexdigest():
            return 'T'
        else:
            return 'F'
    else:
        'F'

'''寻找已借阅的书籍
参数:用户学号
返回:((< books object >,< record object >),……)
'''
def find_borrowed_books(stuid):
    trecord=record.objects.filter(username=stuid,state=0)
    bookids=[]
    for onerecord in trecord:
        bookids.append(onerecord.bid)
    tbook=books.objects.filter(id__in=bookids)
    return zip(tbook,trecord)

'''寻找需要归还的书籍
参数:用户学号
返回:((< books object >,< record object >),……)
'''
def find_needreturn_books(stuid):
    trecord=record.objects.filter(username=stuid,state=1)
    bookids=[]
    for onerecord in trecord:
        bookids.append(onerecord.bid)
    tbook=books.objects.filter(id__in=bookids)
    return zip(tbook,trecord)

'''寻找已经归还的书籍
参数:用户学号
返回:[(< books object >,< record object >),……]
'''
def find_returned_books(stuid):
    trecord=record.objects.filter(username=stuid,state=2)
    data=[]
    for onerecord,forloop in zip(trecord,range(0,len(trecord))):
        temp = books.objects.filter(id=onerecord.bid)
        if temp:
            data.append((temp[0],trecord[forloop]))
        else:
            pass
    #raise Exception(data)
    return data

'''搜索书籍
参数:书id,书名
返回:(< books object >,……)
'''
def search_books(bid,bname):
    tbook=books.objects.filter(
        Q(id__contains=bid) & Q(bookname__contains=bname)
    )
    return tbook

'''书库书籍
参数:bgn书id开始,gnd书id结束,stype:NOTALL不全部搜索,ALL全部搜索,默认不全部搜索
返回:(< books object >,……)
'''
def stack_books(bgn,end,stype='NOTALL'):
    if stype=='NOTALL':
        tbook=books.objects.filter(
            Q(id__gte=bgn) & Q(id__lte=end)
        ).order_by('-hits')
    else:
        tbook=books.objects.all().order_by('-hits')

    return tbook

'''返还书籍
参数:记录id
返回:T成功,F失败
'''
def returning_book(bookid,username):
    tuser = users.objects.filter(stuid=username)
    if tuser:
        tuser=tuser[0]
    else:
        return 'F'

    trecord=record.objects.filter(bid=bookid,username=username,state__in=(0,1))
    if trecord:
        trecord[0].state=2
        trecord[0].save()

        tuser.borrowstate=tuser.borrowstate[0]+str(int(tuser.borrowstate[1])-1)
        tuser.save()
        return 'T'
    else:
        return 'F'

'''借阅书籍
参数:记录id
返回:T成功,F0借书超过上限,F1超期而失败,F2用户已冻结,F3这本书已经被借走,F9别的失败
'''
def borrowing_book(bookid,username):
    tuser = users.objects.filter(stuid=username)
    if tuser:
        tuser=tuser[0]
    else:
        return 'F2'
    tbook = books.objects.filter(id=bookid)
    if tbook:
        tbook=tbook[0]
    else:
        return 'F2'
    #判断是不是借书状态前两位都是数字
    try:
        int(tuser.borrowstate[0])
        int(tuser.borrowstate[1])
    except:
        return 'F9'
    #如果用户有借的书超期
    if int(tuser.borrowstate[0])==1:
        return 'F1'
    #借书达到上限
    if int(tuser.borrowstate[1])>=3:
        return 'F0'
    #用户已被冻结
    if tuser.state==1:
        return 'F2'
    #书已被借走
    oldrecord = record.objects.filter(bid=bookid,state__in=(0,1))
    if oldrecord:
        return 'F3'
    #都没问题则创建新的纪录
    nrecord = record(username=tuser.stuid,uid=tuser.id,bookname=tbook.bookname,
        bid=tbook.id,time=datetime.datetime.now(),state=0)
    #raise Exception(record(username=tuser.stuid,uid=tuser.id,bookname=tbook.bookname,
        #bid=tbook.id,time=datetime.datetime.now(,state=0).save())
    nrecord.save()
    tuser.borrowstate=tuser.borrowstate[0]+str(int(tuser.borrowstate[1])+1)
    tuser.save()
    return 'T'
