# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from .views import WriteArticleView


urlpatterns = [
    url(r'^write/$',WriteArticleView.as_view(),name='operation_write'),

]