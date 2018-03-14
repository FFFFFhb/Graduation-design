import datetime

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile
from .forms import LoginForm
from article.models import Article
from operation.models import UserFavorite
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
                if user.is_active:
                    login(request, user)
                    return render(request, 'wellcomepage.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误或未激活!'})
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
        favlist = UserFavorite.objects.filter(user_id=int(request.user.id))

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
        })

class UserDetailView(View):
    def get(self,request,user_id):
        userdetail = UserProfile.objects.get(id=int(user_id))
        my_article = Article.objects.filter(author_id=int(user_id))
        #收藏
        # has_fav = False
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=userdetail.id, fav_type=2):
        #         has_fav = True
        # userdetail.click_num += 1
        # userdetail.save()
        return render(request,'mymessage.html',{
            'userdetail':userdetail,
            'my_article':my_article,
        })

class UserInfoView(LoginRequiredMixin,View):
    # 用户个人信息
    def get(self, request):
        user_id = request.user.id
        my_article = Article.objects.filter(author_id=int(user_id))
        return render(request, 'userdetail.html', {
            'my_article': my_article,
        })

class EditUserMessage(View):
    def get(self,request):
        return render(request,"editmessage.html",{
        })
