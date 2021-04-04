from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.users.forms import LoginForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

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
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
