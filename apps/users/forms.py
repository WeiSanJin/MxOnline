# -*- coding: utf-8 -*-
# @File : forms.py
# @Author :WeiSanJin
# @Time :2021/04/04 17:24
# @Site :https://github.com/WeiSanJin
from django import forms
from captcha.fields import CaptchaField
import redis
from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


# 登录验证
class LoginForm(forms.Form):
    # 变量username要与前端页面表单输入框name一致| required：必填字段 min_length：最小长度
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


# 动态验证码
class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


# 手机动态登录验证
class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    # 只对code字段进行验证
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        # 对动态验证码进行验证
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            # 如果动态验证码不一致-->抛出异常
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    '''
    # 自定义验证码逻辑-对全部字段进行验证
    def clean(self):
        mobile = self.cleaned_data["mobile"]
        code = self.cleaned_data["code"]

        # 对动态验证码进行验证
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            # 如果动态验证码不一致-->抛出异常
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data
    '''


# 注册验证码
class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


# 用户注册验证
class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=6, max_length=20)

    # 验证手机号码是否已经注册
    def clean_mobile(self):
        mobile = self.data.get("mobile")
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号码已注册")
        return mobile

    # 只对code字段进行验证
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        # 对动态验证码进行验证
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            # 如果动态验证码不一致-->抛出异常
            raise forms.ValidationError("验证码不正确")
        return code


# 用户头像上传
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


# 用户信息修改
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birday", "address"]


# 修改密码
class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("您输入的密码不一致")
        return self.cleaned_data
