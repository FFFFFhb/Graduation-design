# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from .views import UserDetailView,UserInfoView,UserListView,EditUserMessage

urlpatterns = [
    url(r'^list$', UserListView.as_view(), name='user_list'),
    #用户信息
    url(r'^detail/(?P<user_id>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),
    url(r'^editmymessage/$',EditUserMessage.as_view(),name='edit_message'),
]