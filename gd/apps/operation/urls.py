# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from .views import WriteArticleView,TestEditorView,EditArticleView


urlpatterns = [
    url(r'^write/$',WriteArticleView.as_view(),name='operation_write'),
    # 修改文章
    url(r'^editarticle/(?P<edit_article_id>\d+)/$', EditArticleView.as_view(), name='operation_edit'),
    url(r'^testeditor/$',TestEditorView.as_view(),name='test_editor'),
]