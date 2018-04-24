import datetime
import json

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile
from .forms import LoginForm,UserInfoForm,UploadSurfaceForm,UploadImageForm
from article.models import Article
from operation.models import UserFavorite,ArticleComments
from operation.gongtonong import GongToNong



class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# Create your views here.
# 用户登录
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'wellcomepage.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'login.html', {'login_form':login_form})

#用户登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('wellcomepage'))

class UserListView(View):
    def get(self,request):
        all_user = UserProfile.objects.all()
        user_nums = all_user.count()
        showtime = datetime.datetime.now().date()

        #搜索功能
        search_keywords = request.GET.get('keywords',"")
        if search_keywords:
            all_user = all_user.filter(Q(username__icontains=search_keywords)|Q(nick_name__icontains=search_keywords)|Q(educated__icontains=search_keywords)|Q(profession__icontains=search_keywords))


        # 公历转换成农历显示
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        lunar_year, change_year, lunar_month, lunar_day = GongToNong.setnong(self, y, m, d)
        shownong = "\t农历 " + change_year + "年" + lunar_month + lunar_day + " " + lunar_year + "年 "

        # 收藏
        favlist = None
        if request.user:
            favlist = UserFavorite.objects.filter(user_id=int(request.user.id))
        fav_list = []
        for i in favlist:
            if i.fav_type == '2' or i.fav_type == 2:
                fav_list.append(i.fav_id)

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "new":
                all_articles = all_user.order_by("-add_time")
            elif sort == "hot":
                all_articles = all_user.order_by("-fans_nums")

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_user, 10, request=request)
        atcs = p.page(page)
        return render(request, "userlist.html", {
            "all_user":atcs,
            "showtime": showtime,
            "shownong": shownong,
            "sort": sort,
            "user_nums":user_nums,
            "fav_list":fav_list,
        })

class UserDetailView(View):
    def get(self,request,user_id):
        userdetail = UserProfile.objects.get(id=int(user_id))
        my_article = Article.objects.filter(author_id=int(user_id))

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(my_article, 10, request=request)
        atcs = p.page(page)
        return render(request,'mymessage.html',{
            'userdetail':userdetail,
            'my_article':atcs,
        })

class UserInfoView(LoginRequiredMixin,View):
    # 用户个人信息
    def get(self, request):
        user_id = request.user.id
        my_article = Article.objects.filter(author_id=int(user_id))
        my_fav_user = UserFavorite.objects.filter(user_id=int(user_id),fav_type=2)
        my_fav_article = UserFavorite.objects.filter(user_id=int(user_id),fav_type=1)
        my_fav_article_list = []
        my_fav_user_list = []
        my_comment_list = ArticleComments.objects.filter(user_id=int(user_id))
        for my_fav_id in my_fav_user:
            fav_user_id = my_fav_id.fav_id
            fu = UserProfile.objects.get(id=int(fav_user_id))
            my_fav_user_list.append(fu)
        for my_fav_id in my_fav_article:
            fav_article_id = my_fav_id.fav_id
            fa = Article.objects.get(id=int(fav_article_id))
            my_fav_article_list.append(fa)

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(my_article, 5, request=request)
        atcs1 = p.page(page)

        return render(request, 'userdetail.html', {
            'my_article': atcs1,
            'my_fav_article_list':my_fav_article_list,
            'my_fav_user_list':my_fav_user_list,
            'my_comment_list':my_comment_list,
        })

class EditUserMessage(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"editmessage.html",{
        })
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,request.FILES,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return render(request, 'editmessage.html', {'msg': '修改成功!'})
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UploadSurfaceView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form = UploadSurfaceForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class AddFavView(LoginRequiredMixin,View):
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
            if int(fav_type) == 2:
                user = UserProfile.objects.get(id=int(fav_id))
                user.fans_nums -= 1
                if user.fans_nums < 0:
                    user.fans_nums = 0
                user.save()

            return HttpResponse('{"status":"success", "msg":"关注"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)

                user_fav.save()
                if int(fav_type) == 2:
                    user = UserProfile.objects.get(id=int(fav_id))
                    user.fans_nums += 1
                    user.save()
                return HttpResponse('{"status":"success", "msg":"已关注"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

def page_not_found(request):
    #全局404配置函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    #全局404配置函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response

