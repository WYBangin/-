import hashlib
import hmac

from django.shortcuts import render
from django.conf import settings


'''
     this is tool.
    这个一个工具类
'''


def require_login(fn):
    '''

    这是一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果登录，就进入视图，如果没登录，则返回登录界面
    '''
    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_user = request.session.get("loginUser", None)
        if login_user is not None:
            return fn(request, *args, **kwargs)
        else:
            return render(request, "studentCMS/login.html", {"msg": "该页面需要登录才能访问，请先登录..."})
    return inner


def encrypt_pwd_hashlib(password):
    '''
    使用hashlib模块对用户密码进行加密,这种主要用于对文章摘要等加密
    :param password:用户密码
    :return:一个加密后密文
    '''

    md5 = hashlib.md5(password.encode("utf-8"))
    md5.update(settings.SALT.encode("utf-8"))
    # md5.update("wyb@qq.com".encode("utf-8"))
    return md5.hexdigest()


def encrypt_pwd_hmac(password):
    '''
    使用hashlib模块对用户密码进行加密，这种安全性更高，所以项目中用的是这种
    :param password:用户密码
    :return:一个加密后密文
    '''

    return hmac.new(settings.SALT.encode("utf-8"), password.encode("utf-8")).hexdigest()


if __name__ == '__main__':
    print(encrypt_pwd_hashlib("123456"))





