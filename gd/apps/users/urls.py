# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from .views import UserDetailView,UserInfoView

urlpatterns = [
    #用户信息
    url(r'^detail/(?P<user_id>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),
]