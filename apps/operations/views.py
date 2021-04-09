from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from apps.operations.models import UserFavorite, CourseComments, Banner
from apps.operations.form import UserFavForm, CommentsForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher


# 用户收藏、取消收藏
class AddFavView(View):
    def post(self, request, *args, **kwargs):

        # 如果用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        # 如果检验全部通过
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            # 是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            # 如果用户已经收藏，则取消收藏
            if existed_records:
                # 将收藏数据从数据库中删除
                existed_records.delete()
                """:收藏类型
                    1.课程
                    2.课程机构
                    3.讲师
                """
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    tracher = Teacher.objects.get(id=fav_id)
                    tracher.fav_nums -= 1
                    tracher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


# 用户评论
class CommentView(View):
    def post(self, request, *args, **kwargs):

        # 如果用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        # 如果检验全部通过
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


# 首页
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # 首页轮播图
        banners = Banner.objects.all().order_by("index")
        # 首页展示课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 首页课程轮播图
        banner_courses = Course.objects.filter(is_banner=True)
        # 首页机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs
        })
