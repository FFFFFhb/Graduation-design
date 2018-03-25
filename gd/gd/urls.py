"""gd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from gd.settings import MEDIA_ROOT
from users.views import LoginView,LogoutView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='wellcomepage.html'),name='wellcomepage'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),

    #apps url
    url(r'^article/', include('article.urls', namespace='article')),
    url(r'^user/',include('users.urls',namespace='user')),
    url(r'^operation/',include('operation.urls',namespace='operation')),

    #
    # url(r'^success/',SuccessView.as_view(),name='success'),
    # url(r'^failed/',FailedView.as_view(),name='failed'),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]

#全局404页面配置
handler404 = 'users.view.page_not_found'
#全局500页面配置
handler500 = 'users.view.page_error'