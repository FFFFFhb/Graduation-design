from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class WriteArticleView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request , 'writearticle.html',{})
    # def post(self,request):
    #     new_article_form = NewArticleForm(request.POST,request.FILES)
    #     if new_article_form.is_valid():
    #         image = new_article_form.cleaned_data['image']
    #         title = request.POST.get('title', '')
    #         desc = request.POST.get('desc', '')
    #         detail = request.POST.get('detail', '')
    #         author = request.user
    #         new_article = Article()
    #         new_article.author = author
    #         new_article.title = title
    #         new_article.image = image
    #         new_article.desc = desc
    #         new_article.detail = detail
    #         new_article.save()
    #
    #         return render(request, 'success.html')
    #     else:
    #         return render(request, 'failde.html')