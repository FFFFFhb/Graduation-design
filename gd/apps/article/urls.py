# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import ArticleView,ArticleDetailView

urlpatterns = [
    url(r'^list$', ArticleView.as_view(), name='article_list'),
    url(r'^detail/(?P<article_id>\d+)/$',ArticleDetailView.as_view(), name='article_detail'),

]