# _*_ coding:utf-8 _*_
from django import forms
from article.models import Article

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author','title','detail','image']

class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','detail','image']