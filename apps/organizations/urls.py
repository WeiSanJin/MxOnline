# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/06 21:39
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url

from apps.organizations.views import OrgView

urlpatterns = [
    url('list/', OrgView.as_view(), name="list"),
]
