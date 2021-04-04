# -*- coding: utf-8 -*-
# @File : forms.py
# @Author :WeiSanJin
# @Time :2021/04/04 17:24
# @Site :https://github.com/WeiSanJin
from django import forms


class LoginForm(forms.Form):
    # 变量username要与前端页面表单输入框name一致| required：必填字段 min_length：最小长度
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)
