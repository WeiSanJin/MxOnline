# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/07 15:16
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url
from apps.operations.views import AddFavView

urlpatterns = [
    # 用户收藏
    url(r'^fav/$', AddFavView.as_view(), name="fav"),
]
