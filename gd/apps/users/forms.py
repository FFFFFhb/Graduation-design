# _*_ coding:utf-8 _*_
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# class RegisterForm(forms.Form):
#     email = forms.EmailField(required=True)
#     password = forms.CharField(required=True, min_length=5)
#     captcha = CaptchaField(error_messages={"invalid": u'验证码错误'})
#
# class ForgetForm(forms.Form):
#     email = forms.EmailField(required=True)
#     captcha = CaptchaField(error_messages={"invalid": u'验证码错误'})
#
# class ModifyPwdForm(forms.Form):
#     password1 = forms.CharField(required=True, min_length=5)
#     password2 = forms.CharField(required=True, min_length=5)
#
class UploadImageForm(forms.Form):
    class Meta:
        model = UserProfile
        fields = ['image']

class UploadSurfaceForm(forms.Form):
    class Meta:
        model = UserProfile
        fields = ['surface']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['surface','image','nick_name','email','gender','short_summary','birthday','address','educated','profession','summary']
#nick_name,birthday,gender,educated,profession,mobile,image,fans_num,address,summary,short_summary