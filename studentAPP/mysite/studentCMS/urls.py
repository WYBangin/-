from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^code/$', views.code, name="code"),
    url(r'^reg/$', views.reg, name="reg"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^mod_pwd/$', views.mod_pwd, name="mod_pwd"),
    url(r'^reset_pwd/(?P<u_id>\d+)/$', views.reset_pwd, name="reset_pwd"),
    url(r'^user/$', views.user, name="user"),
    url(r'^user_info/$', views.user_info, name="user_info"),
    url(r'^choose_course/$', views.choose_course, name="choose_course"),
    url(r'^my_center/$', views.my_center, name="my_center"),
    url(r'^my_center_edit/(?P<u_id>\d+)/$', views.my_center_edit, name="my_center_edit"),
    # 管理员
    url(r'^add_course/$', views.add_course, name="add_course"),
    url(r'^delete_course/(?P<u_id>\d+)/$', views.delete_course, name="delete_course"),
    url(r'^delete_student/(?P<u_id>\d+)/$', views.delete_student, name="delete_student"),
    url(r'^delete_teacher/(?P<u_id>\d+)/$', views.delete_teacher, name="delete_teacher"),
    url(r'^update_student/(?P<u_id>\d+)/$', views.update_student, name="update_student"),
    url(r'^update_teacher/(?P<u_id>\d+)/$', views.update_teacher, name="update_teacher"),
    url(r'^reset_pwd/(?P<u_id>\d+)/$', views.reset_pwd, name="reset_pwd"),
    url(r'^delete_notice/(?P<u_id>\d+)/$', views.delete_notice, name="delete_notice"),
    # 屏蔽教师或学生登录
    url(r'^start_shield_student/(?P<u_id>\d+)/$', views.start_shield_student, name="start_shield_student"),
    url(r'^start_shield_teacher/(?P<u_id>\d+)/$', views.start_shield_teacher, name="start_shield_teacher"),
    url(r'^end_shield_student/(?P<u_id>\d+)/$', views.end_shield_student, name="end_shield_student"),
    url(r'^end_shield_teacher/(?P<u_id>\d+)/$', views.end_shield_teacher, name="end_shield_teacher"),
    # 学生
    url(r'^get_score/(?P<u_id>\d+)/$', views.get_score, name="get_score"),
    url(r'^get_select_course/(?P<u_id>\d+)/$', views.get_select_course, name="get_select_course"),
    # 教师
    url(r'^add_stu_score/$', views.add_stu_score, name="add_stu_score"),
    url(r'^get_all_score/$', views.get_all_score, name="get_all_score"),
    url(r'^show_course/$', views.show_course, name="show_course"),
    url(r'^tea_notice/$', views.tea_notice, name="tea_notice"),
    url(r'^view_notice/$', views.view_notice, name="view_notice"),
    url(r'^edit_notice/(?P<u_id>\d+)/$', views.edit_notice, name="edit_notice"),

]