import xadmin

from . import models
from xadmin import views

xadmin.site.register(models.AdminMan)
xadmin.site.register(models.Student)
xadmin.site.register(models.Teacher)
xadmin.site.register(models.Classes)
xadmin.site.register(models.Course)
xadmin.site.register(models.AsSchedule)
xadmin.site.register(models.SelectCourse)
xadmin.site.register(models.Score)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "博雅管理系统后台"
    site_footer = "2018@qikuedu.com"
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView,GlobalSettings)
