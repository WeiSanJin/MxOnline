from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.courses.models import Course, CourseTag, CourseResource, Video

# 公开课列表
from apps.operations.models import UserFavorite, UserCourse, CourseComments


# 课程列表
class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Course.objects.order_by("-add_time")

        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(desc__icontains=keywords))

        # 对授课机构进行排名
        hot_courses = all_courses.order_by("-click_nums")[:3]

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
            "sort": sort,
            "hot_courses": hot_courses,
            "s_type": s_type,
            "keywords": keywords
        })


# 课程详情页面
class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 用户是否收藏 fav_type:1(课程) 2(课程机构)
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        """ 通过课程的tag做课程的推荐
        tag = course.tag
        related_courses = []
        if tag:
            related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]
        """

        """ = tag_list = [tag.tag for tag in tags]
        tag_list = []
        for tag in tags:
            tag_list.append(tag.tag)
        """
        # 当前课程所有的tag
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        # 查询和当前课程相同tag的记录，过滤当前课程
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })


# 课程章节信息
class CourseLessonView(LoginRequiredMixin, View):
    # 用户要进入此方法前必须是登录状态
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        """
            1. 用户和课程之间的关联
            2. 对view进行login登录验证
            3. 该课的同学还学过
        """

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("course__click_nums")[:3]

        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


# 课程评论
class CourseCommentView(LoginRequiredMixin, View):
    # 用户要进入此方法前必须是登录状态
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 评论信息
        comments = CourseComments.objects.filter(course=course).order_by("-add_time")

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("course__click_nums")[:3]

        related_courses = []
        for item in all_courses:
            if item.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments
        })


# 课程视频
class VideoView(LoginRequiredMixin, View):
    # 用户要进入此方法前必须是登录状态
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("course__click_nums")[:3]

        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video
        })
