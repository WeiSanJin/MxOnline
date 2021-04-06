# -*- coding: utf-8 -*-
# @File : forms.py
# @Author :WeiSanJin
# @Time :2021/04/06 21:57
# @Site :https://github.com/WeiSanJin
import re
from django import forms
from apps.operations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")


"""
    当models需要验证字段较多时不适用        
class AddAskForm2(forms.Form):
    name = forms.CharField(required=True, min_length=2, max_length=20)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=2, max_length=20)
"""
