# -*- coding: utf-8 -*-
# @File : adminx.py
# @Author :WeiSanJin
# @Time :2021/04/03 21:16
# @Site :https://github.com/WeiSanJin
import xadmin


class GlovalSettings(object):
    site_title = "在线教育网站后台管理系统"
    site_footer = "在线教育网站"


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
    # menu_style = "accordion"


xadmin.site.register(xadmin.views.CommAdminView, GlovalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
