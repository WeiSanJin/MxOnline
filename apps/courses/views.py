from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Course.objects.order_by("-add_time");

        # 最热门排序、参与人数排序
        sort = request.GET.get("sort", "")
        if sort == 'hot':
            all_courses = Course.objects.order_by("-click_nums")
        elif sort == 'students':
            all_courses = Course.objects.order_by("-students")

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=9, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort
        })
