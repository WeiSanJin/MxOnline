# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 18:36
# @Site :https://github.com/WeiSanJin
import xadmin

from xadmin.layout import Main, Fieldset, Side, Row, FormHelper

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag


# 课程信息
class CourseAdmin(object):
    list_filter = ['name', 'teacher__name', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                   'add_time']
    list_display = ['name', 'teacher', 'category', 'degree', 'students', 'fav_num', 'click_nums',
                    'is_classics', 'is_banner',
                    'add_time']
    list_editable = ['degree', 'is_classics', 'is_banner', 'desc']
    search_fields = ['name', 'teacher', 'desc', 'detail', 'degree', 'learn_times', 'students']


# 课程标签
class CourseTagAdmin(object):
    list_filter = ['course', 'tag', 'add_time']
    list_display = ['course', 'tag', 'add_time']
    list_editable = ['course', 'tag']
    search_fields = ['course', 'tag']


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


# 修改xadmin页面的布局
class NewCourseAdmin(object):
    list_filter = ['name', 'teacher__name', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                   'add_time']
    list_display = ['name', 'teacher', 'category', 'degree', 'students', 'fav_num', 'click_nums',
                    'is_classics', 'is_banner',
                    'add_time']
    list_editable = ['degree', 'is_classics', 'is_banner', 'desc']
    search_fields = ['name', 'teacher', 'desc', 'detail', 'degree', 'learn_times', 'students']

    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset("讲师信息",
                         'teacher', 'course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset("基本信息",
                         'name', 'desc',
                         Row('learn_times', 'degree'),
                         Row('category', 'tag'),
                         'youneed_know', 'teacher_tell', 'detail',
                         ),
            ),
            Side(
                Fieldset("访问信息",
                         'fav_nums', 'click_nums', 'students', 'add_time'
                         ),
            ),
            Side(
                Fieldset("选择信息",
                         'is_banner', 'is_classics'
                         ),
            )
        )
        return super(NewCourseAdmin, self).get_form_layout()


# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, NewCourseAdmin)
