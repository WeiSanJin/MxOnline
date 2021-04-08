# 规范 1.python自带方法、库 2.第三方库  3.自定义方法
from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher, CourseOrg

# 1.设计表结构注意的点
'''
    实体1 <关系> 实体2
    课程 章节 视频 课程资源 
'''


# 2.实体的具体字段
# 3.每个字段的类型，是否必填


# 课程信息
class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="课程机构")
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=100)
    tag = models.CharField(verbose_name="课程标签", max_length=10, default="")
    category = models.CharField(verbose_name="课程类别", max_length=20, default=u"后端开发")
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    fav_num = models.IntegerField(verbose_name="收藏人数", default=0)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    youneed_know = models.CharField(verbose_name="课程须知", max_length=300, default="")
    teacher_tell = models.CharField(verbose_name="老师告诉你", max_length=300, default="")
    degree = models.CharField(verbose_name="难度", max_length=2, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")))
    detail = models.TextField(verbose_name="课程详情")
    image = models.ImageField(verbose_name="封面图", max_length=100, upload_to="courses/%Y/%m")
    is_classics = models.BooleanField(verbose_name="是否经典课程", default=False)
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 章节数量
    def lesson_nums(self):
        return self.lesson_set.all().count()


# 课程标签
class CourseTag(BaseModel):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE, )
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


# 章节信息
class Lesson(BaseModel):
    # 外键(ForeignKey)    on_delete：对应的外键数据被删除后，当前的数据应该怎么办
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE, )
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 视频
class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    url = models.CharField(max_length=200, verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程资源
class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(verbose_name="名称", max_length=100)
    file = models.FileField(verbose_name="文件", upload_to="courses/resourse/%Y/%M", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
