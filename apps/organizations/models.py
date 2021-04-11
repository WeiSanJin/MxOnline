from django.db import models

from apps.users.models import BaseModel

from DjangoUeditor.models import UEditorField


# 城市
class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程机构
class CourseOrg(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")
    name = models.CharField(verbose_name="机构名称", max_length=50)
    desc = UEditorField(verbose_name="描述", width='100%', height=300, imagePath="courses/ueditor/images/",
                        filePath="courses/ueditor/files/", default="")
    tag = models.CharField(verbose_name="机构标签", max_length=10, default="全国知名")
    category = models.CharField(verbose_name="机构类别", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="封面图", max_length=100, upload_to="org/%Y/%m")
    address = models.CharField(verbose_name="机构地址", max_length=150)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    course_nums = models.IntegerField(verbose_name="课程数", default=0)

    is_auth = models.BooleanField(verbose_name="是否认证", default=False)
    is_gold = models.BooleanField(verbose_name="是否金牌", default=False)

    def courses(self):
        '''
        # 此方法易出现异常
        from apps.courses.models import Course
        courses = Course.objects.filter(course_org=self)
        '''
        # 经典课程前3个
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    def teachers(self):
        return self.teacher_set.all()

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 教师
class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y%m", max_length=100, verbose_name="头像")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()
