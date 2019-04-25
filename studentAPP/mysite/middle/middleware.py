from django.http import HttpResponse

try:
    from django.utils.deprecation import MiddlewareMixin    # Django 1.10x
except ImportError:
    MiddlewareMixin = object    # Django 1.4.x —— Django1.9.x


class MyMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 判断session是否存在登录用户
        login_user = request.session.get("loginUser", None)
        if login_user is not None:
            pass
        else:
            return HttpResponse("该页面需要登录才能访问，请<a href='/studentCMS/login/'>登录</a>")
