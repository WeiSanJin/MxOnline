# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 20:39
# @Site :https://github.com/WeiSanJin
import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


# 用户咨询
class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    list_editable = ['name', 'mobile', 'course_name']
    search_fields = ['name', 'mobile', 'course_name']


# 课程评论
class CourseCommentsAdmin(object):
    list_filter = ['user', 'course__name', 'comments', 'add_time']
    list_display = ['user', 'course', 'comments', 'add_time']
    list_editable = ['user', 'course', 'comments']
    search_fields = ['user', 'course', 'comments']


# 用户收藏
class UserFavoriteAdmin(object):
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    list_editable = ['user', 'fav_id', 'fav_type']
    search_fields = ['user', 'fav_id', 'fav_type']


# 用户消息
class UserMessageAskAdmin(object):
    list_filter = ['user', 'message', 'has_read', 'add_time']
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_editable = ['user', 'message', 'has_read']
    search_fields = ['user', 'message', 'has_read']


# 用户学习的课程
class UserCourseAdmin(object):
    search_fields = ['user__name', 'course']
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    list_editable = ['user', 'course']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
