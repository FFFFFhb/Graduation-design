# _*_ encoding:utf-8 _*_
from datetime import datetime
from django.db import models

from users.models import UserProfile

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name=u'作者', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name=u'标题')
    desc = models.CharField(max_length=100, verbose_name=u'标签', null=True, blank=True)
    detail = models.TextField(verbose_name=u'内容')
    #detail = UEditorField(verbose_name=u"文章详情",width=600,hight=300,imagePath="article/ueditor",filePath="article/ueditor/",default="")
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums =models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='article/%Y/%m', verbose_name=u'封面图', max_length=100,null=True, blank=True)
    score = models.IntegerField(default=0, verbose_name=u'评分')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#author,title,desc,detail,click_num,fav_nums,image,score,add_time
    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title