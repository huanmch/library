# coding:utf-8

from tushuguan.models import *

'''通过验证cookie判断是否已经登陆
参数:request
返回:'T'成功,'F'失败
'''
def judge_islogin(request,c):
    username = request.session.get('stuid','')
    if username:
        tuser = users.objects.filter(stuid=username)
        if tuser:
            tuser = tuser[0]
            c.update({'realname':tuser.realname})
            return 'T'
        else:
            return 'F'
    else:
        return 'F'

'''用户登陆时检查使用的设备
参数:request
返回值:'pc':电脑,'pe'手机
'''
def check_page(request):
    user = request.META['HTTP_USER_AGENT']
    if 'Windows Phone' in user:
        return 'pe'
    elif 'Windows' in user and 'Windows Phone' not in user:
        return 'pc'
    elif 'Mac' in user:
        if not 'iPhone' in user:
            return 'pc'
        else:
            return 'pe'
    elif 'Linux' in user:
        if not 'Android' in user:
            return 'pc'
        else:
            return 'pe'
    else:
        return 'pe'        