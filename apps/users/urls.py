# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/08 22:58
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView, MyFavOrgView, \
    MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    # 头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),
    # 修改密码
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="upload_pwd"),
    # 修改手机号码
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name="update_mobile"),

    # # 我的课程
    # url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    # 我的课程（优化）
    url(r'^mycourse/$',
        login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"), login_url="/login/"),
        name="mycourse"),

    # 我的收藏
    url(r'^myfav_org/$', MyFavOrgView.as_view(), name="myfav_org"),
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name="myfav_teachers"),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
    url(r'^message/$', MyMessageView.as_view(), name="message"),
]
