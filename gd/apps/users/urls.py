# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from .views import UserDetailView,UserInfoView,UserListView,EditUserMessage,AddFavView,UploadImageView,UploadSurfaceView

urlpatterns = [
    url(r'^list$', UserListView.as_view(), name='user_list'),
    #用户信息
    url(r'^detail/(?P<user_id>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),
    url(r'^editmymessage/$',EditUserMessage.as_view(),name='edit_message'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    #用户头像上传
    url(r'image/upload/$',UploadImageView.as_view(),name='image_upload'),
    #用户封面页上传
    url(r'surface/upload/$',UploadSurfaceView.as_view(),name='surface_upload'),
]