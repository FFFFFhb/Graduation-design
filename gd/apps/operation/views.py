import json

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
            new_article = Article()
            new_article.author = author
            new_article.title = title
            new_article.image = image
            new_article.detail = detail
            new_article.save()
            return render(request, 'success.html')
            # return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
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
            edit_article = Article.objects.get(pk=edit_article_id)
            edit_article.title = title
            if image:
                edit_article.image = image
            edit_article.detail = detail
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