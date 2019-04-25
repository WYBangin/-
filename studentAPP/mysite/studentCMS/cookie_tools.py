import base64

from django.shortcuts import render


def encode_cookie(sentence):
    '''
    中文不能存储在cookie中，所以，需要编码处理
    :param sentence: 要转码的字符串
    :return: 编码字符串
    '''
    word = base64.b64encode(sentence.encode("utf-8"))
    return word


def count_cookie(request, context):
    '''
    统计错误登录的次数，以便三次显示验证码
    :param request: 客户端请求对象
    :param context: 错误信息，字典对象
    :return: 返回响应对象
    '''
    count = int(request.COOKIES.get("login_error", 0))
    count += 1
    response = render(request, "studentCMS/login.html", {"msg": context, "count": count})
    response.set_cookie("login_error", count, max_age=60*10)
    return response
