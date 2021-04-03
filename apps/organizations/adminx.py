# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 18:36
# @Site :https://github.com/WeiSanJin
import xadmin

from apps.organizations.models import Teacher, CourseOrg, City

'''
list_display(列表中显示那些字段)
search_fields(搜索字段)
list_filter(过滤字段)
list_editable(那些字段可以直接修改)
'''


# 教师
class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'age', 'add_time']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                   'fav_nums',
                   'age', 'add_time']
    list_editable = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                     'age']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'age']


# 课程机构
class CourseOrgAdmin(object):
    list_filter = ['city__name', 'name', 'desc', 'tag', 'degree', 'click_nums', 'fav_nums', 'course_nums', 'students',
                   'address', 'add_time']
    list_display = ['name', 'desc', 'tag', 'degree', 'click_nums', 'fav_nums', 'course_nums', 'students', 'image',
                    'address', 'city', 'add_time']
    list_editable = ['name', 'desc', 'tag', 'degree', 'click_nums', 'fav_nums', 'course_nums', 'students', 'image',
                     'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'tag', 'degree', 'address', 'city']


# 城市管理
class CityAdmin(object):
    list_filter = ['name', 'desc', 'add_time']
    list_display = ['id', 'name', 'desc', 'add_time']
    list_editable = ['name', 'desc']
    search_fields = ['name', 'desc']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
