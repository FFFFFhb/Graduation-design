# _*_ coding:utf-8 _*_
from .models import Article
import xadmin

class ArticleAdmin(object):
    #author,title,desc,detail,click_num,fav_nums,image,score,add_time
    list_display = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num']
    list_filter = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']

xadmin.site.register(Article, ArticleAdmin)