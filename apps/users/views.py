from turtledemo.penrose import f

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

import redis

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, \
    UploadImageForm
from apps.utils.random_str import generate_random
from apps.utils.TencentSendSms import send_sms_single
from MxOnline.settings import TENCENT_Template_ID, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


# 登录
class LoginView(View):
    def get(self, request, *args, **kwargs):
        # 判断用户是否登录
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next
        })

    def post(self, request, *args, **kwargs):
        # 表单验证--此方法造成代码冗余不适用
        # username = request.POST.get("username", "")
        # password = request.POST.get("password", "")
        # if not username:
        #     return render(request, "login.html", {"msg": "请输入用户名"})
        # if not password:
        #     return render(request, "login.html", {"msg": "请输入密码"})

        # 表单验证
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # 用于通过用户和密码查询用户是否存在
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                # 查询到用户
                login(request, user)
                # 登录成功之后返回页面
                # return render(request, "index.html") # 登录成功后url无法重定向
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 退出登录
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        # 重定向到首页
        return HttpResponseRedirect(reverse("index"))


# 发送验证码
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        # 如果前端图形验证码输入正确
        if send_sms_form.is_valid():
            # 验证码验证成功
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成验证码
            code = generate_random(4, 0)
            # 验证码接口返回信息
            re_json = send_sms_single(mobile, TENCENT_Template_ID, [code, 5])
            # 如果手机验证码发送成功
            if re_json['result'] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                # 设置验证码五分钟过去
                r.expire(str(mobile), 60 * 5)
            else:
                re_dict["msg"] = re_json["errmsg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


# 动态验证码登录
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("idnex"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next
        })

    def post(self, request, *args, **kwargs):
        # 验证用户输入是否正确
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            mobile = login_form.cleaned_data["mobile"]
            # 查询用户是否存在
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                # 存在——获取用户信息进行登录
                user = existed_users[0]
            else:
                # 用户不存在，进行注册用户
                user = UserProfile(username=mobile)
                # 随机生成密码
                password = generate_random(10, 2)
                # 将随机密码进行加密
                user.set_password(password)
                user.mobile = mobile
                user.save()
            # 进行登录并跳转至首页
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm
            return render(request, "login.html",
                          {"login_form": login_form, 'd_form': d_form, "dynamic_login": dynamic_login})


# 用户注册
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        # 获取验证码返回给前端
        register_get_form = RegisterGetForm
        return render(request, "register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        # 验证用户输入是否正确
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]

            # 用户不存在，进行注册用户
            user = UserProfile(username=mobile)
            # 将随机密码进行加密
            user.set_password(password)
            user.mobile = mobile
            user.save()
            # 进行登录并跳转至首页
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form
            })


# 用户个人中心
class UserInfoView(LoginRequiredMixin, View):
    # 用户要进入此方法前必须是登录状态
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        return render(request, "usercenter-info.html")


# 头像上传
class UploadImageView(LoginRequiredMixin, View):
    # 用户要进入此方法前必须是登录状态
    login_url = '/login/'

    # def save_file(self, file):
    #     with open("F:/痞老板过年学编程/MxOnline/media/head_image/2021/04"):
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        # files = request.FILES["image"]
        # self.save_file(files)

        """问题
            1. 如果同一个文件上传多次，相同名称的文件应该如何处理
            2. 文件的保存路径应该写入到user
            3. 还没有做表单验证
        """
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })
