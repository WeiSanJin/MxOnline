from django.db import models

from django.contrib.auth import get_user_model

from apps.users.models import BaseModel
from apps.courses.models import Course

UserProfile = get_user_model()


# 用户咨询
class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "用户：{name}({mobile})，咨询：{course}课程".format(name=self.name, course=self.course_name, mobile=self.mobile)


# 课程评论
class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


# 用户收藏
class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


# 用户消息
class UserMessage(BaseModel):
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户学习的课程
class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "用户学习的课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name
