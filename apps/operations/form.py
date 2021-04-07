# -*- coding: utf-8 -*-
# @File : forms.py
# @Author :WeiSanJin
# @Time :2021/04/06 21:57
# @Site :https://github.com/WeiSanJin
from django import forms
from apps.operations.models import UserFavorite


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]
