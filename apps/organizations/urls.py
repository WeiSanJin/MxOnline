# -*- coding: utf-8 -*-
# @File : urls.py
# @Author :WeiSanJin
# @Time :2021/04/06 21:39
# @Site :https://github.com/WeiSanJin
from django.conf.urls import url

from apps.organizations.views import OrgView, AddAskView,OrgHomeView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),

    # path('<intt:org_id>/', OrgHomeView.as_view(), name="home")
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),


]
