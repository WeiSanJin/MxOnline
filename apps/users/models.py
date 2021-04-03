from datetime import datetime

from django.db import models
# 继承auth_user表
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male", u"男"),
    ("female", u"女")
)


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        # 不生成表
        abstract = True


class UserProfile(AbstractUser):
    nick_name = models.CharField(verbose_name=u"昵称", max_length=50, default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", max_length=6, choices=GENDER_CHOICES, default="female")
    address = models.CharField(verbose_name=u"地址", max_length=100, default="")
    mobile = models.CharField(verbose_name=u"手机号码", max_length=11)
    image = models.ImageField(verbose_name=u"头像", max_length=100, upload_to="head_image/%Y/%m", default="default.jpg")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
