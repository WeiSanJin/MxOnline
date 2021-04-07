# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/07 17:16
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url
from apps.courses.views import CourseListView, CourseDetailView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
]
