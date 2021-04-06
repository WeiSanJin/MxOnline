from django.shortcuts import render
from django.views.generic.base import View

from apps.organizations.models import CourseOrg, City


class OrgView(View):
    def get(self, request, *args, **kwargs):
        org_data = {}
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        # 总共有多少家机构
        org_data['nums'] = CourseOrg.objects.count()
        # 全部的城市
        org_data['citys'] = City.objects.all()
        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
            "org_data": org_data
        })
