# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 18:36
# @Site :https://github.com/WeiSanJin
import xadmin
from import_export import resources

from xadmin.layout import Main, Fieldset, Side, Row

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse


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


class LessonInline(object):
    model = Lesson
    style = "tab"
    extra = 0
    exclude = ["add_time"]


class CourseResourceInline(object):
    model = CourseResource
    style = "tab"
    extra = 0


# 导入导出
class MyResource(resources.ModelResource):
    class Meta:
        model = CourseResource
        # fields = ('name', 'description',)
        # exclude = ()


# 修改xadmin页面的布局
class NewCourseAdmin(object):
    # 导入导出配置，此处也可以只配置一个导入功能或导出功能，而把另一个功能关掉
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_filter = ['name', 'teacher__name', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                   'add_time']
    list_display = ['name', 'teacher', 'category', 'degree', 'students', 'fav_num', 'click_nums',
                    'is_classics', 'is_banner',
                    'show_image', 'go_to', 'add_time']
    list_editable = ['degree', 'is_classics', 'is_banner', 'desc']
    search_fields = ['name', 'teacher', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 只读
    # readonly_fields = ["students", "click_nums", "fav_num", "add_time"]
    # 隐藏
    # exclude = ["click_nums", "fav_nums"]
    # 排序
    ordering = ["click_nums"]
    # 更换图标
    model_icon = 'fa fa-address-book'
    # 关联其他表
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {
        "detail": "ueditor"
    }

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


# 轮播课程管理
class BannerCourseAdmin(object):
    list_filter = ['name', 'teacher__name', 'category', 'degree', 'learn_times', 'students', 'fav_num', 'click_nums',
                   'add_time']
    list_display = ['name', 'teacher', 'category', 'degree', 'students', 'fav_num', 'click_nums',
                    'is_classics', 'is_banner',
                    'add_time']
    list_editable = ['degree', 'is_classics', 'is_banner', 'desc']
    search_fields = ['name', 'teacher', 'desc', 'detail', 'degree', 'learn_times', 'students']

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
