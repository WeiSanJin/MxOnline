# Generated by Django 2.2 on 2021-04-06 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20210406_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='degree',
            new_name='category',
        ),
    ]
