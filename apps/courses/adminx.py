# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 18:36
# @Site :https://github.com/WeiSanJin
import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource


# 课程信息
class CourseAdmin(object):
    list_filter = ['name', 'teacher__name', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                   'add_time']
    list_display = ['name', 'teacher', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                    'image',
                    'add_time']
    list_editable = ['degree', 'desc']
    search_fields = ['name', 'teacher', 'desc', 'detail', 'degree', 'learn_times', 'students']


# 章节信息
class LessonAdmin(object):
    list_filter = ['course__name', 'name', 'add_time']
    list_display = ['course', 'name', 'add_time']
    list_editable = ['course', 'name']
    search_fields = ['course', 'name']


# 课程视频
class VideoAdmin(object):
    list_filter = ['lesson__name', 'name', 'add_time']
    list_display = ['lesson', 'name', 'learn_times', 'url']
    list_editable = ['lesson', 'name', 'learn_times', 'url']
    search_fields = ['lesson', 'name']


# 课程资源
class CourseResourceAdmin(object):
    list_filter = ['course__name', 'name', 'add_time']
    list_display = ['course', 'name', 'file', 'add_time']
    list_editable = ['course', 'name']
    search_fields = ['course', 'name']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
