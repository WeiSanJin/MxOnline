# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/06 21:39
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),

    # path('<intt:org_id>/', OrgHomeView.as_view(), name="home")
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="desc"),

    # 讲师列表页
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),

    # 讲师详情页
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
