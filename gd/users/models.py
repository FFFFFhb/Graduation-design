from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.



class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default='')
    birthday = models.DateTimeField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(choices=(('male',u'男'),('female',u'女')),default='female',max_length=7)
    educated = models.CharField(max_length=100,default=u'')
    profession = models.CharField(max_length=100, default=u'')
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)
    fans_nums = models.IntegerField(default=0, verbose_name=u'粉丝数')
    address = models.CharField(max_length=150, default=u'')
    city = models.CharField(max_length=50,verbose_name=u'所在城市',default='')
    # age = models.IntegerField(default=18, verbose_name=u'年龄')
    summary = models.TextField(verbose_name=u'个人简介')
    short_summary = models.CharField(max_length=100,default=u'')
    is_org = models.CharField(choices=(('yes',u'是'),('no',u'否')),default='no',max_length=7)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")),max_length=30)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
