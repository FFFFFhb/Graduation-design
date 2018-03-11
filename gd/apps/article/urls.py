# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import ArticleView,ArticleDetailView,AddFavView

urlpatterns = [
    url(r'^list$', ArticleView.as_view(), name='article_list'),
    url(r'^detail/(?P<article_id>\d+)/$',ArticleDetailView.as_view(), name='article_detail'),
    #收藏文章
    url(r'^add_fav/$',AddFavView.as_view(), name='add_fav')
]