# Generated by Django 2.2 on 2021-04-10 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_is_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('courses.course',),
        ),
    ]