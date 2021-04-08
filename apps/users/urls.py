# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/08 22:58
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url

from apps.users.views import UserInfoView

urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserInfoView.as_view(), name="info"),
]


