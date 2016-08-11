# coding: utf-8

from django.db import models

class usergroup(models.Model):
    id = models.AutoField(primary_key=True)          #编号
    introduction = models.CharField(max_length=32)   #介绍
    extrainfo = models.CharField(max_length=100)     #附加信息（先空着）
    number = models.IntegerField()                   #可重复的标记号（先空着）
    class Meta:
        db_table = 'library_usergroup'
    def __unicode__(self):
        return u"编号%d,介绍%s"%(self.id,self.introduction)

class users(models.Model):
    id = models.AutoField(primary_key=True)          #编号
    stuid = models.CharField(max_length=15)          #学号
    code = models.CharField(max_length=60)           #加密后的密码
    realname = models.CharField(max_length=30)       #真实姓名
    tel = models.CharField(max_length=15)            #手机号
    email = models.CharField(max_length=60)          #邮箱

    borrowstate = models.CharField(max_length=100)   #借书状态,两位数,十位保留用的
                                                     #个位:0-8为借阅的书总量
    state = models.SmallIntegerField()               #当前用户状态,0为正常,1为账号冻结
    usergroupid = models.IntegerField()              #用户组别编号，相当于外键,2为普通用户,1为管理员,目前还没用
    extrainfo = models.CharField(max_length=100)     #附加信息（先空着）
    class Meta:
        db_table = 'library_users'
    def __unicode__(self):
        return u"学号%s,真实姓名%s"%(self.stuid,self.realname)

class books(models.Model):
    id = models.AutoField(primary_key=True)          #编号
    bookname = models.CharField(max_length=32)       #书名
    introduction = models.CharField(max_length=32)   #介绍
    writers = models.CharField(max_length=100)       #作者
    booktype = models.CharField(max_length=20)       #类别
    hits = models.IntegerField()                     #被借次数（热门度）
    extrainfo = models.CharField(max_length=100)     #附加信息（先空着）
    attachid = models.IntegerField()

    class Meta:
        db_table = 'library_books'

    def attach(self):
        tface = face.objects.filter(id = self.attachid)
        if tface:
            return tface[0].adress
        else:
            return ''

    def __unicode__(self):
        return self.bookname

class record(models.Model):
    id = models.AutoField(primary_key=True)          #编号
    username = models.CharField(max_length=32)       #借书人（的学号），相当于外键
    writers = models.CharField(max_length=32)        #作者
    uid = models.IntegerField()                      #用户id，相当于外键
    bookname = models.CharField(max_length=32)       #书名，相当于外键
    bid = models.IntegerField()                      #书id，相当于外键
    time = models.DateTimeField()                    #借书时间
    state = models.SmallIntegerField()               #此借书记录的状态,0为正在借阅，1为过期，2为已还
    class Meta:
        db_table = 'library_record'
    def __unicode__(self):
        return u"%s借了%s"%(self.username,self.bookname)

class face(models.Model):
    id = models.AutoField(primary_key=True)          #编号
    bname = models.CharField(max_length=100)         #书名，相当于外键
    bid = models.IntegerField()                      #书id，相当于外键
    adress = models.CharField(max_length=100)        #存放地址
    pic_name = models.CharField(max_length=100)      #图片名字
    class Meta:
        db_table = 'library_face'
    def __unicode__(self):
        return u"%s的缩略图"%(self.bname)
