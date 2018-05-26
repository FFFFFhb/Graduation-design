import json
from jieba.analyse import *
from snownlp import SnowNLP

from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect

from .forms import NewArticleForm,EditArticleForm
from article.models import Article

# Create your views here.
class WriteArticleView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request , 'writearticle.html',{})
    def post(self,request):
        new_article_form = NewArticleForm(request.POST,request.FILES)
        if new_article_form.is_valid():
            image = new_article_form.cleaned_data['image']
            title = request.POST.get('title', '')
            detail = request.POST.get('detail', '')
            author = request.user

            #结巴分词 TextRank 关键词提取
            data = detail
            desc = ''
            tsum = 0
            if len(detail) >= 280:
                for keyword, weight in textrank(data, topK=10, withWeight=True):
                    desc += (keyword+',')

                s = SnowNLP(detail)
                for sentence in s.sentences:
                    tsum += float(SnowNLP(sentence).sentiments) - 0.5

            new_article = Article()
            new_article.author = author
            new_article.title = title
            new_article.image = image
            new_article.desc = desc
            new_article.detail = detail
            new_article.score = tsum
            new_article.save()
            return render(request, 'success.html')
        else:
            return render(request, 'failed.html')


class TestEditorView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request , 'testeditor.html',{})

class EditArticleView(LoginRequiredMixin,View):
    def get(self,request,edit_article_id):
        edit_article = Article.objects.get(id=int(edit_article_id))
        return render(request,'editarticle.html',{
            'edit_article':edit_article,
        })
    def post(self,request,edit_article_id):
        edit_article = EditArticleForm(request.POST, request.FILES)
        if edit_article.is_valid():
            image = edit_article.cleaned_data['image']
            title = request.POST.get('title', '')
            detail = request.POST.get('detail', '')

            # 结巴分词 TextRank 关键词提取
            data = detail
            desc = ''
            tsum = 0
            if len(detail) >= 280:
                for keyword, weight in textrank(data, topK=10, withWeight=True):
                    desc += (keyword + ',')

                s = SnowNLP(detail)
                for sentence in s.sentences:
                    tsum += float(SnowNLP(sentence).sentiments) - 0.5

            edit_article = Article.objects.get(pk=edit_article_id)
            edit_article.title = title
            if image:
                edit_article.image = image
            edit_article.detail = detail
            edit_article.score = tsum
            edit_article.desc = desc
            edit_article.save()
            return render(request, 'success.html')
        else:
            return render(request, 'failed.html')


class DeleteArticleView(LoginRequiredMixin,View):
    def post(self,request):
        article_id = request.POST.get('article_id',0)

        if not request.user.is_authenticated():
            return  HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
        exist_records = Article.objects.filter(pk=article_id)
        if exist_records:
            #如果记录已经存在，则删除文章
            exist_records.delete()
            return render(request, 'success.html')