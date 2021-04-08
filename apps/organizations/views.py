from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, PageNotAnInteger
from django.http import JsonResponse

from apps.operations.models import UserFavorite
from apps.organizations.models import CourseOrg, City, Teacher
from apps.organizations.form import AddAskForm


class OrgView(View):
    def get(self, request, *args, **kwargs):
        org_data = {}
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        # 全部的城市
        org_data['citys'] = City.objects.all()
        # 对授课机构进行排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 对所在进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        # 总共有多少家机构
        org_data['nums'] = all_orgs.count()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_data": org_data,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs
        })


# 我要学习
class AddAskView(View):
    """
    处理用户的咨询
    """

    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            # 保存数据库
            userask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 课程、讲师
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav": has_fav
        })


# 机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav": has_fav
        })


# 机构课程
class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_course = course_org.course_set.all()
        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, per_page=1, request=request)
        courses = p.page(page)

        return render(request, "org-detail-course.html", {
            "all_course": courses,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav": has_fav
        })


# 机构介绍
class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_course = course_org.course_set.all()
        return render(request, "org-detail-desc.html", {
            "all_course": all_course,
            "course_org": course_org,
            "course_page": course_page,
            "has_fav": has_fav
        })


# 讲师列表
class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 热门讲师
        hot_teachers = Teacher.objects.all().order_by("-fav_nums")[:5]

        # 讲师进行排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")
        elif sort == "":
            all_teachers = all_teachers.order_by("-work_years")

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, per_page=4, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "hot_teachers": hot_teachers
        })
