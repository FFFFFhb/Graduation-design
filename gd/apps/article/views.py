import datetime

from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Article
from operation.models import ArticleComments
from operation.gongtonong import GongToNong

# Create your views here.
class ArticleView(View):
    """
     文章列表功能
    """
    def get(self,request):
        #文章列表
        all_articles = Article.objects.all()
        article_nums = all_articles.count()
        article_id = request.GET.get('articleid',"")
        hot_article = all_articles.order_by("-click_num")[:5]
        showtime = datetime.datetime.now().date()

        #公历转换成农历显示
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        lunar_year, change_year, lunar_month, lunar_day = GongToNong.setnong(self,y,m,d)
        shownong = "\t农历 "+change_year+"年"+lunar_month+lunar_day+" "+lunar_year+"年 "

        #排序
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "new":
                all_articles = all_articles.order_by("-add_time")
            elif sort == "hot":
                all_articles = all_articles.order_by("-fav_nums")


        #评论
        all_comments = ArticleComments.objects.all()
        all_comments = all_comments.order_by("-fav_time")
        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_articles, 5, request=request)

        atcs = p.page(page)

        return render(request,"articlelist.html",{
            "all_articles":atcs,
            "article_nums":article_nums,
            "all_comments":all_comments,
            "hot_article":hot_article,
            "sort":sort,
            "showtime":showtime,
            "shownong":shownong,
        })


class ArticleDetailView(View):
    def get(self,request,article_id):
        articledetail = Article.objects.get(id=int(article_id))
        # 评论
        all_comments = ArticleComments.objects.all()
        all_comments = all_comments.order_by("-fav_time")

        articledetail.click_num += 1
        articledetail.save()
        return render(request,'article_detail.html',{
            'articledetail':articledetail,
            "all_comments":all_comments,
        })
