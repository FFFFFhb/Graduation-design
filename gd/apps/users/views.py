from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin

from .models import UserProfile
from .forms import LoginForm

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

class UserDetailView(View):
    def get(self,request):
        return render(request,'mymessage.html',{})

class UserInfoView(LoginRequiredMixin,View):
    # 用户个人信息
    def get(self, request):
        return render(request, 'userdetail.html', {
        })
