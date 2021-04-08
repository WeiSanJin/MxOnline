# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/07 17:16
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url
from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentView, VideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),
    url(r'^(?P<course_id>\d+)/comment/$', CourseCommentView.as_view(), name="comment"),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),
]
