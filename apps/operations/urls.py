# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/07 15:16
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url
from apps.operations.views import AddFavView, CommentView

urlpatterns = [
    # 用户收藏
    url(r'^fav/$', AddFavView.as_view(), name="fav"),
    # 用户评论
    url(r'^comment/$', CommentView.as_view(), name="comment"),
]
