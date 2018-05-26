# _*_ coding:utf-8 _*_
import datetime
import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Article
from operation.models import ArticleComments,UserFavorite
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
        hot_article = all_articles.order_by("-click_num")[:5]
        showtime = datetime.datetime.now().date()

        #搜索功能
        search_keywords = request.GET.get('keywords',"")
        if search_keywords:
            all_articles = all_articles.filter(Q(title__icontains=search_keywords)|
                                               Q(desc__icontains=search_keywords)|
                                               Q(detail__icontains=search_keywords))

        # 收藏
        favlist = None
        fav_list = []
        if request.user.id:
            favlist = UserFavorite.objects.filter(user_id=int(request.user.id))
            for i in favlist:
                if i.fav_type == '1' or i.fav_type == 1:
                    fav_list.append(i.fav_id)

        #公历转换成农历显示
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        lunar_year, change_year, lunar_month, lunar_day = GongToNong.setnong(self,y,m,d)
        shownong = "\t农历 "+change_year+"年"+lunar_month+lunar_day+" "+lunar_year+"年 "

        #排序
        sort = request.GET.get('sort',"")
        all_articles = all_articles.order_by("-add_time")
        if sort:
            if sort == "new":
                all_articles = all_articles.order_by("-add_time")
            elif sort == "hot":
                all_articles = all_articles.order_by("-click_num")
            elif sort == "hot2":
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
        p = Paginator(all_articles, 10, request=request)
        atcs = p.page(page)

        return render(request,"articlelist.html",{
            "all_articles":atcs,
            "article_nums":article_nums,
            "all_comments":all_comments,
            "hot_article":hot_article,
            "sort":sort,
            "showtime":showtime,
            "shownong":shownong,
            "favlist":favlist,
            "fav_list":fav_list,
        })


class ArticleDetailView(View):
    def get(self,request,article_id):
        articledetail = Article.objects.get(id=int(article_id))
        # 评论
        all_comments = ArticleComments.objects.all()
        all_comments = all_comments.order_by("-fav_time")
        #收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=articledetail.id, fav_type=1):
                has_fav = True
        articledetail.click_num += 1
        articledetail.save()
        return render(request,'article_detail.html',{
            'articledetail':articledetail,
            "all_comments":all_comments,
            'has_fav':has_fav,
        })


class AddFavView(View):
    #用户收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                article = Article.objects.get(id=int(fav_id))
                article.fav_nums -= 1
                if article.fav_nums < 0:
                    article.fav_nums = 0
                article.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)

                user_fav.save()
                if int(fav_type) == 1:
                    article = Article.objects.get(id=int(fav_id))
                    article.fav_nums += 1
                    article.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')
        article_id = request.POST.get('article_id',0)
        comments = request.POST.get('comments','')
        if int(article_id) > 0 and comments:
            article_comments = ArticleComments()
            article = Article.objects.get(id=int(article_id))
            article_comments.article = article
            article_comments.comments = comments
            article_comments.user = request.user
            article_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')

