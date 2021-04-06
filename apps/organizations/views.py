from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_data": org_data,
        })
