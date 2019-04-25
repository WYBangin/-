import random as r

from io import BytesIO
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from . import models
from . import encry_tools
from . import code_tools
from . import cookie_tools


def code(request):
    '''
    加一个验证码视图函数
    :param request: 请求，可以将验证码的值存储到session上
    :return:在网页上返回一张图片
    '''
    img, msg = code_tools.create_img()
    # 获取一个字节IO
    file = BytesIO()
    img.save(file, "PNG")
    # 将验证码的值存储到session中
    request.session["code"] = msg
    # MIME文件类型
    return HttpResponse(file.getvalue(), 'image/png')


@encry_tools.require_login
def reset_pwd(request, u_id):
    '''
    重置密码的函数，只有管理员可以操作
    :param request: 请求对象
    :param u_id: 重置哪个用户的密码
    :return: 响应对象
    '''
    password = encry_tools.encrypt_pwd_hmac("wyb123")
    try:
        user = models.Student.objects.get(pk=u_id)
        user.password = password
        user.save()
    except:
        user = models.Teacher.objects.get(pk=u_id)
        user.teaPassword = password
        user.save()
    finally:
        return render(request, "studentCMS/reset_success.html", {"msg": "您的密码已经重置成功，密码wyb123已经发送到邮箱了"})


@encry_tools.require_login
def index(request):
    '''
    首页面用来充当掌上校园模块
    :param request: 请求对象
    :return: 响应对象
    '''
    return render(request, "studentCMS/index.html", {})


def reg(request):
    '''
    注册页面，项目完成后，把这个藏起来，只有管理员知道方式，哈哈
    :param request: 请求对象
    :return: 响应对象
    '''
    classes = models.Classes.objects.all()
    if request.method == "GET":
        return render(request, "studentCMS/reg.html", {"msg": "请认真填写注册信息", "classes": classes})
    elif request.method == "POST":
        identity = request.POST["identity"]
        name = request.POST.get("name").strip()
        password = request.POST.get("password").strip()
        confirm_pwd = request.POST.get("confirm_pwd").strip()
        my_code = request.POST.get("code").strip()
        check_id = request.POST.get("check_id", None)

        # 数据校验
        msg_code = request.session["code"]

        if check_id is None:
            return render(request, "studentCMS/reg.html", {"msg": "注册前请同意安全协议", "classes": classes})
        if my_code.upper() != msg_code.upper():
            return render(request, "studentCMS/reg.html", {"msg": "验证码错误", "classes": classes})
        if name == "":
            return render(request, "studentCMS/reg.html", {"msg": "用户名不能为空", "classes": classes})
        if password == "":
            return render(request, "studentCMS/reg.html", {"msg": "密码不能为空", "classes": classes})
        if confirm_pwd == "":
            return render(request, "studentCMS/reg.html", {"msg": "确认密码不能为空", "classes": classes})
        if len(password) < 6 and password.isalnum():
            return render(request, "studentCMS/reg.html", {"msg": "密码须由字母数字组成，且不少于6位", "classes": classes})
        if password != confirm_pwd:
            return render(request, "studentCMS/reg.html", {"msg": "两次密码不一致", "classes": classes})

        # 判断注册者的身份
        if identity == "3":
            try:
                models.AdminMan.objects.get(adminName=name)
                return render(request, "studentCMS/reg.html", {"msg": "用户名已存在，请重新注册", "classes": classes})
            except:
                try:
                    password = encry_tools.encrypt_pwd_hmac(password)
                    user = models.AdminMan(adminName=name, password=password)
                    user.save()
                    return render(request, "studentCMS/login.html", {"msg": "恭喜您注册成功，请登录"})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/reg.html", {"msg": "对不起，注册失败，请重新注册", "classes": classes})

        elif identity == "2":
            try:
                models.Teacher.objects.get(teaName=name)
                return render(request, "studentCMS/reg.html", {"msg": "用户名已存在，请重新注册", "classes": classes})
            except:
                try:
                    password = encry_tools.encrypt_pwd_hmac(password)
                    user = models.Teacher(teaName=name, teaPassword=password)
                    user.save()
                    return render(request, "studentCMS/login.html", {"msg": "恭喜您注册成功，请登录"})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/reg.html", {"msg": "对不起，注册失败，请重新注册", "classes": classes})

        elif identity == "1":
            cls = request.POST.get("cls")
            if cls == "":
                return render(request, "studentCMS/reg.html", {"msg": "学生身份，必须选择班级", "classes": classes})
            if cls == "学生必选":
                return render(request, "studentCMS/reg.html", {"msg": "请选择学生的班级", "classes": classes})


        try:
                models.Student.objects.get(name=name)
                return render(request, "studentCMS/reg.html", {"msg": "用户名已存在，请重新注册", "classes": classes})
        except:
            try:
                password = encry_tools.encrypt_pwd_hmac(password)
                class_id = models.Classes.objects.get(className=cls)
                user = models.Student(name=name, password=password, classId_id=class_id.id)
                user.save()
                return render(request, "studentCMS/login.html", {"msg": "恭喜您注册成功，请登录"})
            except Exception as e:
                print(e)
                return render(request, "studentCMS/reg.html", {"msg": "对不起，注册失败，请重新注册，注意学生必选 ", "classes": classes})


def login(request):
    '''
    登录页面，这是项目开始展示的地方
    :param request: 请求对象
    :return: 响应对象
    '''
    if request.method == "GET":
        return render(request, "studentCMS/login.html", {"msg": "请认真填写登录信息"})
    elif request.method == "POST":
        identity = request.POST["identity"]
        name = request.POST.get("name").strip()
        password = request.POST.get("password").strip()
        my_code = request.POST.get("code", None)

        # 三次出现验证码，进行接收验证
        if my_code is not None:
            # 数据校验
            msg_code = request.session["code"]
            if my_code.upper() != msg_code.upper():
                msg = "验证码错误"
                response = cookie_tools.count_cookie(request=request, context=msg)
                return response
        if name == "":
            msg = "用户名不能为空"
            response = cookie_tools.count_cookie(request=request, context=msg)
            return response
        if password == "":
            msg = "密码不能为空"
            response = cookie_tools.count_cookie(request=request, context=msg)
            return response
        if my_code is not None:
            msg = request.session["code"]
            if msg.upper() != my_code.upper():
                msg = "验证码错误"
                response = cookie_tools.count_cookie(request=request, context=msg)
                return response
        # 判断登陆者的身份
        if identity == "3":
            try:
                user = models.AdminMan.objects.get(adminName=name)
                password = encry_tools.encrypt_pwd_hmac(password)
                if password == user.password:
                    # 使用session存储登录者的身份和名字
                    request.session["flag"] = 1
                    request.session["loginUser"] = user
                    # 使用cookie存储用户名称
                    response = redirect(reverse("studentCMS:user_info"))
                    b64_name = cookie_tools.encode_cookie(user.adminName)
                    response.set_cookie("name", b64_name)
                    # 登录之后立即把登录错误的login_error清零
                    count = 0
                    response.set_cookie("login_error", count, max_age=60*10)
                    return response
                else:
                    msg = "请确认密码是否正确"
                    response = cookie_tools.count_cookie(request=request, context=msg)
                    return response
            except Exception as e:
                print("出现错误，错误的信息是：", e)
                msg = "请确认用户名或身份是否正确"
                response = cookie_tools.count_cookie(request=request, context=msg)
                return response
        elif identity == "2":
            try:
                user = models.Teacher.objects.get(teaName=name)
                password = encry_tools.encrypt_pwd_hmac(password)
                if user.is_shield == 0:
                    if password == user.teaPassword:
                        request.session["flag"] = 2
                        request.session["loginUser"] = user
                        # 使用cookie存储用户名称
                        response = redirect(reverse("studentCMS:user"))
                        b64_name = cookie_tools.encode_cookie(user.teaName)
                        response.set_cookie("name", b64_name)
                        # 登录之后立即把登录错误的login_error清零
                        count = 0
                        response.set_cookie("login_error", count, max_age=60*10)
                        return response
                    else:
                        msg = "请确认密码是否正确"
                        response = cookie_tools.count_cookie(request=request, context=msg)
                        return response
                elif user.is_shield == 1:
                    return render(request, "studentCMS/login.html", {"msg": "您已被屏蔽登录，需要联系管理员"})
            except Exception as e:
                print("出现错误，错误的信息是：", e)
                msg = "请确认用户名或身份是否正确"
                response = cookie_tools.count_cookie(request=request, context=msg)
                return response

        elif identity == "1":
            try:
                user = models.Student.objects.get(name=name)
                password = encry_tools.encrypt_pwd_hmac(password)
                if user.is_shield == 0:
                    if password == user.password:
                        request.session["flag"] = 3
                        request.session["loginUser"] = user
                        # 使用cookie存储用户名称
                        response = redirect(reverse("studentCMS:user"))
                        b64_name = cookie_tools.encode_cookie(user.name)
                        response.set_cookie("name", b64_name)
                        # 登录之后立即把登录错误的login_error清零
                        count = 0
                        response.set_cookie("login_error", count, max_age=60*10)
                        return response
                    else:
                        msg = "请确认密码是否正确"
                        response = cookie_tools.count_cookie(request=request, context=msg)
                        return response
                elif user.is_shield == 1:
                    return render(request, "studentCMS/login.html", {"msg": "您已被屏蔽登录，需要联系管理员"})
            except Exception as e:
                print("出现错误，错误的信息是：", e)
                msg = "请确认用户名是否正确"
                response = cookie_tools.count_cookie(request=request, context=msg)
                return response


def logout(request):
    '''
    登出页面，根据不同的人，登出存储的登录时间方式不一致，超管不存登录时间
    :param request: 请求对象
    :return: 响应对象
    '''
    if request.session["flag"] == 1:
        try:
            del request.session["loginUser"]
            del request.session["flag"]
        except:
            pass
        finally:
            return render(request, "studentCMS/login.html", {"msg": "账号已安全退出，欢迎再次光临"})
    if request.session["flag"] == 2:
        try:
            u_id = request.session["loginUser"].id
            time = datetime.now()
            user = models.Teacher.objects.get(id=u_id)
            user.teaLast_login = time
            user.save()
            del request.session["loginUser"]
            del request.session["flag"]
        except:
            pass
        finally:
            return render(request, "studentCMS/login.html", {"msg": "账号已安全退出，欢迎再次光临"})
    if request.session["flag"] == 3:
        try:
            u_id = request.session["loginUser"].id
            time = datetime.now()
            user = models.Student.objects.get(id=u_id)
            user.last_login = time
            user.save()
            del request.session["loginUser"]
            del request.session["flag"]
        except:
            pass
        finally:
            return render(request, "studentCMS/login.html", {"msg": "账号已安全退出，欢迎再次光临"})


@encry_tools.require_login
def user(request):
    '''
    学生和教师用来展示信息的地方，很重要哦
    :param request: 请求对象
    :return: 响应对象
    '''
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    return render(request, "studentCMS/user.html", {"students": students, "teachers": teachers})


@encry_tools.require_login
def user_info(request):
    '''
    超管用来操作教师和学生的函数
    :param request: 请求对象
    :return: 响应对象
    '''
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    return render(request, "studentCMS/user_info.html", {"students": students, "teachers": teachers})


@encry_tools.require_login
def add_course(request):
    '''
    开设课程的函数，这个只有超管才有的权限，普通教师不行
    :param request:
    :return:
    '''
    courses = models.Course.objects.all()
    if request.method == "GET":
        return render(request, "studentCMS/add_course.html", {"courses": courses})
    elif request.method == "POST":
        course = request.POST.get("course").strip()
        desc = request.POST.get("desc").strip()

        if course == "":
            return render(request, "studentCMS/add_course.html", {"msg": "课程名不能为空", "courses": courses})
        if desc == "":
            return render(request, "studentCMS/add_course.html", {"msg": "课程描述不能为空", "courses": courses})

        try:
            sub = models.Course(course=course, desc=desc)
            sub.save()
            return redirect("studentCMS:add_course")
        except:
            return render(request, "studentCMS/add_course.html", {"msg": "添加失败，请重新添加                    ", "courses": courses})


@encry_tools.require_login
def show_course(request):
    '''
    教师查看所有选课的函数
    :param request: 请求对象
    :return: 响应对象
    '''
    users = models.SelectCourse.objects.all()
    return render(request, "studentCMS/show_course.html", {"users": users})


@encry_tools.require_login
def delete_course(request, u_id):
    '''
    删除课程页面，这个需要谨慎，如果这个课程有人选，不能让删除，
    因为数据库没有关联，所以这个删除检测功能未完善
    :param request:请求对象
    :param u_id:删除课程的id
    :return:响应对象
    '''
    try:
        course = models.Course.objects.get(pk=u_id)
        course.delete()
        return redirect("studentCMS:add_course")
    except:
        return render(request, "studentCMS/add_course.html", {"msg": "删除失败，请重新删除"})


@encry_tools.require_login
def delete_student(request, u_id):
    '''
    删除学生的原理和删除课程类似，故不介绍了，学生毕业最好也不要删除，可以移到废旧的数据库
    后面用屏蔽功能代替删除了
    :param request: 请求对象
    :param u_id: 删除学生id
    :return: 响应对象
    '''
    try:
        student = models.Student.objects.get(pk=u_id)
        student.delete()
        return redirect("studentCMS:user")
    except:
        return render(request, "studentCMS/user.html", {"msg1": "删除失败，请重新删除"})


@encry_tools.require_login
def delete_teacher(request, u_id):
    '''
    和删除学生一样，故这里不介绍了
    :param request: 请求对象
    :param u_id: 删除教师的id
    :return: 响应对象
    '''
    try:
        teacher = models.Teacher.objects.get(pk=u_id)
        teacher.delete()
        return redirect("studentCMS:user")
    except:
        return render(request, "studentCMS/user.html", {"msg2": "删除失败，请重新删除"})


@encry_tools.require_login
def start_shield_student(request, u_id):
    user = models.Student.objects.get(pk=u_id)
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    if user.is_shield == 0:
        try:
            user.is_shield = 1
            user.save()
            return render(request, "studentCMS/user_info.html", {"msg1": "该学生已成功屏蔽", "students": students, "teachers": teachers})
        except:
            return render(request, "studentCMS/user_info.html", {"msg1": "屏蔽学生失败，请稍后重试", "students": students, "teachers": teachers})
    elif user.is_shield == 1:
        return render(request, "studentCMS/user_info.html", {"msg2": "该学生已屏蔽，不要重复操作", "students": students, "teachers": teachers})


@encry_tools.require_login
def start_shield_teacher(request, u_id):
    user = models.Teacher.objects.get(pk=u_id)
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    if user.is_shield == 0:
        try:
            user.is_shield = 1
            user.save()
            return render(request, "studentCMS/user_info.html", {"msg2": "该教师已成功屏蔽", "students": students, "teachers": teachers})
        except:
            return render(request, "studentCMS/user_info.html", {"msg2": "屏蔽教师失败，请稍后重试", "students": students, "teachers": teachers})
    elif user.is_shield == 1:
        return render(request, "studentCMS/user_info.html", {"msg2": "该教师已屏蔽，不要重复操作", "students": students, "teachers": teachers})


@encry_tools.require_login
def end_shield_student(request, u_id):
    user = models.Student.objects.get(pk=u_id)
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    if user.is_shield == 1:
        try:
            user.is_shield = 0
            user.save()
            return render(request, "studentCMS/user_info.html", {"msg1": "该学生已成功取消屏蔽", "students": students, "teachers": teachers})
        except:
            return render(request, "studentCMS/user_info.html", {"msg1": "取消屏蔽学生失败，请稍后重试", "students": students, "teachers": teachers})
    elif user.is_shield == 0:
        return render(request, "studentCMS/user_info.html", {"msg2": "该学生已取消屏蔽，不要重复操作", "students": students, "teachers": teachers})


@encry_tools.require_login
def end_shield_teacher(request, u_id):
    user = models.Teacher.objects.get(pk=u_id)
    students = models.Student.objects.all()
    teachers = models.Teacher.objects.all()
    if user.is_shield == 1:
        try:
            user.is_shield = 0
            user.save()
            return render(request, "studentCMS/user_info.html", {"msg2": "该教师已成功取消屏蔽", "students": students, "teachers": teachers})
        except:
            return render(request, "studentCMS/user_info.html", {"msg2": "取消屏蔽教师失败，请稍后重试", "students": students, "teachers": teachers})
    elif user.is_shield == 0:
        return render(request, "studentCMS/user_info.html", {"msg2": "该教师已取消屏蔽，不要重复操作", "students": students, "teachers": teachers})


@encry_tools.require_login
def update_student(request, u_id):
    '''
    修改学生部分信息，这个没有后面个人中心修改强大，
    放出来是管理员要修改的基本信息，意思意思
    :param request: 请求对象
    :param u_id: 修改学生信息的id
    :return: 响应对象
    '''
    student = models.Student.objects.get(id=u_id)
    if request.method == "GET":
        return render(request, "studentCMS/update_student.html", {"student": student})
    else:
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        enter_date = request.POST.get("enter_date").strip()
        remark = request.POST.get("remark").strip()

        # 数据校验
        if enter_date == "":
            return render(request, "studentCMS/update_student.html", {"student": student, "msg": "入学时间不能为空"})
        if remark == "":
            return render(request, "studentCMS/update_student.html", {"student": student, "msg": "备注内容不能为空"})

        try:
            student.age = age
            student.gender = gender
            student.enter_date = enter_date
            student.remark = remark
            student.save()
            return redirect(reverse("studentCMS:user"))
        except Exception as e:
            print(e)
            return render(request, "studentCMS/update_student.html", {"student": student, "msg": "修改失败，请重新修改"})


@encry_tools.require_login
def update_teacher(request, u_id):
    '''
    这个和修改学生一样，故不介绍了
    :param request: 请求对象
    :param u_id: 修改教师信息的id
    :return: 响应对象
    '''
    teacher = models.Teacher.objects.get(id=u_id)
    if request.method == "GET":
        return render(request, "studentCMS/update_teacher.html", {"teacher": teacher})
    else:
        age = request.POST.get("age")
        gender = request.POST.get("gender")

        try:
            teacher.teaAge = age
            teacher.teaGender = gender
            teacher.save()
            return redirect(reverse("studentCMS:user"))
        except Exception as e:
            print(e)
            return render(request, "studentCMS/update_teacher.html", {"teacher": teacher, "msg": "修改失败，请重新修改"})


@encry_tools.require_login
def mod_pwd(request):
    '''
    修改个人密码的函数，和管理员重置密码不是一个概念哇,教师密码字段和其他不一样，故分开了
    :param request: 请求对象
    :return: 响应对象
    '''
    global person
    person = None
    try:
        person = request.session["loginUser"]
    except:
        return render(request, "studentCMS/login.html", {"msg": "请先登录系统！！！"})

    if request.method == "GET":
        # return render(request, "studentCMS/mod_pwd.html", {"msg": "密码修改成功后需要重新登录..."})
        return render(request, "studentCMS/mod_pwd.html", {})
    else:
        old_pwd = request.POST["old_pwd"].strip()
        new_pwd = request.POST["new_pwd"].strip()
        confirm_pwd = request.POST["confirm_pwd"].strip()
        # 加密之后再进行密码比较
        old_pwd = encry_tools.encrypt_pwd_hmac(old_pwd)
        if request.session["flag"] == 1 or request.session["flag"] == 3:

            if person.password != old_pwd:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "原密码输入有误，请重新输入"})
            if len(new_pwd) < 6 and new_pwd.isalnum():
                return render(request, "studentCMS/mod_pwd.html", {"msg": "密码长度不能小于6位，且由数字和字母组成"})
            if new_pwd != confirm_pwd:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "两次密码不一致"})

            try:
                # 密码加密之后存入数据库
                new_pwd = encry_tools.encrypt_pwd_hmac(new_pwd)
                person.password = new_pwd
                person.save()
                request.session["loginUser"] = person
                return redirect(reverse("studentCMS:logout"))
            except:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "修改密码失败，请重新修改"})
        elif request.session["flag"] == 2:
            print(person.teaPassword)
            if person.teaPassword != old_pwd:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "原密码输入有误，请重新输入"})
            if len(new_pwd) < 6 and new_pwd.isalnum():
                return render(request, "studentCMS/mod_pwd.html", {"msg": "密码长度不能小于6位，且由数字和字母组成"})
            if new_pwd != confirm_pwd:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "两次密码不一致"})

            try:
                # 密码加密之后存入数据库
                new_pwd = encry_tools.encrypt_pwd_hmac(new_pwd)
                person.teaPassword = new_pwd
                person.save()
                request.session["loginUser"] = person
                return redirect(reverse("studentCMS:logout"))
            except:
                return render(request, "studentCMS/mod_pwd.html", {"msg": "修改密码失败，请重新修改"})


@encry_tools.require_login
def choose_course(request):
    '''
    选择课程，这个也是重点难点啊，要考虑好表的关系，及选课方式
    :param request:请求对象
    :return: 响应对象
    '''
    # 获取数据库中学生的课程
    courses = models.Course.objects.all()

    if request.method == "GET":
        return render(request, "studentCMS/choose_course.html", {"courses": courses})
    elif request.method == "POST":
        # 接收学生选择的课程
        sub_list = request.POST.getlist("cos", [])   # 用来存储复选框的课程
        sub_length = len(sub_list)
        # 得到学生对象，查询看看数据库中该学生是否选课
        try:
            models.SelectCourse.objects.get(stuName=request.session["loginUser"].name)
            return render(request, "studentCMS/choose_course.html", {"msg": "已成功选课，学期结束前不可修改", "courses": courses})
        except:
            if sub_length <= 0:
                return render(request, "studentCMS/choose_course.html", {"msg": "请选择课程，至少一门", "courses": courses})
            if sub_length >= 4:
                return render(request, "studentCMS/choose_course.html", {"msg": "请重新选择课程，至多四门", "courses": courses})
            # 这个功能是专门提供给学生的
            name = request.session["loginUser"].name

            if sub_length == 1:
                try:
                    sub = models.SelectCourse(
                        selCourse1=sub_list[0],
                        stuName=name,
                    )
                    sub.save()
                    return render(request, "studentCMS/choose_course.html", {"msg": "已成功选课", "courses": courses})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/choose_course.html", {"msg": "添加失败，请重新添加", "courses": courses})
            elif sub_length == 2:
                try:
                    sub = models.SelectCourse(
                        selCourse1=sub_list[0],
                        selCourse2=sub_list[1],
                        stuName=name,
                    )
                    sub.save()
                    return render(request, "studentCMS/choose_course.html", {"msg": "已成功选课", "courses": courses})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/choose_course.html", {"msg": "添加失败，请重新添加", "courses": courses})

            elif sub_length == 3:
                try:
                    sub = models.SelectCourse(
                        selCourse1=sub_list[0],
                        selCourse2=sub_list[1],
                        selCourse3=sub_list[2],
                        stuName=name,
                    )
                    sub.save()
                    return render(request, "studentCMS/choose_course.html", {"msg": "已成功选课", "courses": courses})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/choose_course.html", {"msg": "添加失败，请重新添加", "courses": courses})
            elif sub_length == 4:
                try:
                    sub = models.SelectCourse(
                        selCourse1=sub_list[0],
                        selCourse2=sub_list[1],
                        selCourse3=sub_list[2],
                        selCourse4=sub_list[3],
                        stuName=name,
                    )
                    sub.save()
                    return render(request, "studentCMS/choose_course.html", {"msg": "已成功选课", "courses": courses})
                except Exception as e:
                    print(e)
                    return render(request, "studentCMS/choose_course.html", {"msg": "添加失败，请重新添加", "courses": courses})


@encry_tools.require_login
def get_score(request, u_id):
    '''
    学生个人查看分数的函数
    :param request: 请求对象
    :param u_id: 学生id
    :return: 响应对象
    '''
    # models.Student.objects.get()得到的是一个对象
    try:
        user = models.Student.objects.get(pk=u_id)
        name = user.name
        score_obj = models.Score.objects.get(studentId_id=u_id)
        score = score_obj.score
        return render(request, "studentCMS/show_score.html", {"name": name, "score": score})
    except:
        return render(request, "studentCMS/show_score.html", {"msg": "该学生没有测试"})


@encry_tools.require_login
def get_select_course(request, u_id):
    '''
    学生查看选课的函数
    :param request:请求对象
    :param u_id:学生id
    :return:响应对象
    '''
    student = models.Student.objects.get(pk=u_id)
    try:
        user = models.SelectCourse.objects.get(stuName=student.name)
        return render(request, "studentCMS/get_select_course.html", {"user": user})
    except:
        return redirect("/studentCMS/choose_course/")


@encry_tools.require_login
def get_all_score(request):
    '''教师查询学生成绩的方式'''
    try:
        scores = models.Score.objects.all()
        users = models.Student.objects.all()
        return render(request, "studentCMS/get_all_score.html", {"scores": scores, "users": users})
    except:
        return render(request, "studentCMS/get_all_score.html", {"msg": "请先组织学生进行测试"})


@encry_tools.require_login
def add_stu_score(request):
    '''
    这个是生成学生成绩的方式，不可修改学生分数，因为实际情况肯定是教师填写成绩，
    本来想操作Excel表格，写好存入数据库，发现这个有点难，故未完善，写了一个简单的意思意思
    :param request:
    :return:
    '''
    students = models.Student.objects.all()
    if request.method == "GET":
        return render(request, "studentCMS/add_stu_score.html", {"msg": "执行此页面操作需要确认教师身份，请谅解", "students":students})
    elif request.method == "POST":
        stu = request.POST.get("stu")
        name = request.POST.get("name").strip()
        password = request.POST.get("password").strip()

        # 数据校验
        if stu == "" or stu == "选择学生":
            return render(request, "studentCMS/add_stu_score.html", {"msg": "未选择学生，请选择", "students": students})
        if name == "":
            return render(request, "studentCMS/add_stu_score.html", {"msg": "用户名不能为空", "students": students})
        if password == "":
            return render(request, "studentCMS/add_stu_score.html", {"msg": "密码不能为空",  "students": students})

        try:
            user = models.Teacher.objects.get(teaName=name)
            password = encry_tools.encrypt_pwd_hmac(password)

            if password == user.teaPassword:
                stu_obj = models.Student.objects.get(name=stu)
                try:
                    # 如果查询到，说明该学生有分数，否则进行分数添加
                    models.Score.objects.get(studentId_id=stu_obj.id)
                    return render(request, "studentCMS/add_stu_score.html", {"msg": "该学生的分数已经存在",  "students": students})
                except:
                    stu_score = r.randint(20, 99)
                    user_obj = models.Score(score=stu_score, studentId_id=stu_obj.id)
                    user_obj.save()
                    return render(request, "studentCMS/add_stu_score.html", {"msg": "该学生的分数添加成功！",  "students": students})
            else:
                return render(request, "studentCMS/add_stu_score.html", {"msg": "密码错误！！！",  "students": students})
        except Exception as e:
            print("出现错误，错误信息是：", e)
            return render(request, "studentCMS/add_stu_score.html", {"msg": "用户名错误！！！",  "students": students})


@encry_tools.require_login
@require_GET
def my_center(request):
    '''
    这个是个人中心查看的函数，与下面的修改在同一个页面的
    :param request:请求对象
    :return:请求对象
    '''
    # 获取当前登录者的个人信息
    own = request.session["loginUser"]
    return render(request, "studentCMS/my_center.html", {"own": own})


@encry_tools.require_login
@require_POST
def my_center_edit(request, u_id):
    '''
    个人中心，这个是教师和学生修改信息的地方，一个页面，两类人功能，
    也是一个页面当两个页面来用啊，这是除了选课功能之外的重头戏哇，超管就账户密码，
    所以没有设置修改信息页面哦
    :param request:请求对象
    :param u_id:登录者（教师或学生）id
    :return:响应对象
    '''
    if request.session["flag"] == 2:
        if request.method == "POST":
            own = request.session["loginUser"]
            age = request.POST.get("age").strip()
            gender = request.POST.get("gender")
            photo = request.FILES.get("avatar")

            if age == "":
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "年龄不能为空"})
            if photo is None:
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "头像不能为空"})
            try:
                user = models.Teacher.objects.get(pk=u_id)
                user.teaAge = age
                user.teaGender = gender
                user.teaPhoto = photo
                user.save()
                request.session["loginUser"] = user
                return redirect(reverse("studentCMS:my_center"))
            except Exception as e:
                print(e)
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "修改失败，请重新修改"})

    elif request.session["flag"] == 3:
        if request.method == "POST":
            own = request.session["loginUser"]
            age = request.POST.get("age").strip()
            gender = request.POST.get("gender")
            photo = request.FILES.get("photo")
            enter_date = request.POST.get("enter_date")
            remark = request.POST.get("remark").strip()

            # 数据校验 gender是单选按钮，肯定有值，头像有默认，也不用校验，其他都要校验
            if age == "":
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "年龄不能为空"})
            if photo is None:
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "头像不能为空"})
            if enter_date == "":
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "入学时间不能为空"})
            if remark == "":
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "备注不能为空"})

            try:
                user = models.Student.objects.get(pk=u_id)
                user.age = age
                user.gender = gender
                user.photo = photo
                user.enter_date = enter_date
                user.remark = remark
                user.save()
                request.session["loginUser"] = user
                return redirect("/studentCMS/my_center/")
            except:
                return render(request, "studentCMS/my_center.html", {"own": own, "msg": "修改失败，请重新修改"})


@encry_tools.require_login
def tea_notice(request):
    '''
    这是教师发布公告的函数，用cookie来记录发布时间，这样避免一个人重复发，
    或者一直发的情况
    :param request: 请求对象
    :return: 响应对象
    '''
    if request.method == "GET":
        response = render(request, "studentCMS/tea_notice.html", {"msg": "请在两分钟之内发布公告"})
        try:
            if request.COOKIES["notice_time"] == "22222" or request.COOKIES["edit_time"] == "44444":
                response = render(request, "studentCMS/tea_notice.html", {"msg": "公告为重要内容，一位教师一小时只能发一次，切勿重复操作"})
        except:
            response.set_cookie("notice_time", "11111", max_age=60*2)
        finally:
            return response
    elif request.method == "POST":
        try:
            if request.COOKIES["notice_time"] == "22222":
                return render(request, "studentCMS/tea_notice.html", {"msg": "公告为重要内容，一位教师一小时只能发一次，切勿重复操作"})
        except:
            # # 时间（前端获取的系统时间），留言者（登陆的教师），内容
            time = request.POST.get("tim")
            cmt = request.POST.get("cmt").strip()
            # 数据校验
            if cmt == "":
                return render(request, "studentCMS/tea_notice.html", {"msg": "提交的公告内容不能为空"})

            try:
                notice = models.Notice(context=cmt, pub_time=time, author_id=request.session["loginUser"].id)
                notice.save()
                response = render(request, "studentCMS/tea_notice.html", {"msg": "公告发布成功，切勿多次操作"})
                response.set_cookie("notice_time", "22222", max_age=60*60)
                return response
            except Exception as e:
                print(e)
                return render(request, "studentCMS/tea_notice.html", {"msg": "公告发布失败，请稍后重试"})


@encry_tools.require_login
def view_notice(request):
    '''
    这是查看通知公告的函数，管理员可以看和删除不良公告，教师可以修改自己的公告，
    学生只有阅读通知公告的权利
    :param request: 请求对象
    :return: 响应对象
    '''
    teachers = models.Teacher.objects.all()
    notices = models.Notice.objects.all()
    return render(request, "studentCMS/view_notice.html", {"teachers": teachers, "notices": notices})


@encry_tools.require_login
def edit_notice(request, u_id):
    '''
    修改公告函数，发布者才具有的权利，管理员可以删除，但是不能修改
    :param request: 请求对象
    :param u_id: 要修改的公告id
    :return: 响应对象
    '''
    notice = models.Notice.objects.get(id=u_id)
    if request.method == "GET":
        response = render(
            request,
            "studentCMS/edit_notice.html",
            {"msg": "修改和发布一样，请在两分钟之内完成公告修改", "notice": notice}
        )
        # 这里的错误利用和写公告的错误利用有点区别，需要注意哈
        try:
            if request.COOKIES["notice_time"] == "22222" or request.COOKIES["edit_time"] == "44444":
                response = render(request, "studentCMS/edit_notice.html", {"msg": "公告为重要内容，一小时只能修改一次，切勿重复操作", "notice": notice})
        except Exception as e:
            print("出现错误，错误信息是：", e)
            response.set_cookie("edit_time", "33333", max_age=60*2)
        finally:
            return response
    elif request.method == "POST":
        try:
            if request.COOKIES["edit_time"] == "44444":
                return render(request, "studentCMS/edit_notice.html", {"msg": "公告为重要内容，一小时只能修改一次，切勿重复操作",  "notice": notice})        # # 时间（前端获取的系统时间），留言者（登陆的教师），内容
        except:
            time = request.POST.get("tim")
            cmt = request.POST.get("cmt").strip()
            # 数据校验
            if cmt == "":
                return render(request, "studentCMS/edit_notice.html", {"msg": "提交的公告内容不能为空",  "notice": notice})
            try:
                notice.context = cmt
                notice.mod_time = time
                notice.save()
                response = render(request, "studentCMS/edit_notice.html", {"msg": "公告修改成功，切勿多次操作", "notice": notice})
                response.set_cookie("edit_time", "44444", max_age=60*60)
                return response
            except Exception as e:
                print(e)
                return render(request, "studentCMS/edit_notice.html", {"msg": "公告修改失败，请稍后重试",  "notice": notice})


@encry_tools.require_login
def delete_notice(request, u_id):
    '''
    删除公告函数，管理员才有的权限啊，谨慎操作啊
    redirect两种重定向方式看心情使用...
    重定向传参指的URI参数，并非页面参数
    :param request: 请求对象
    :param u_id: 要删除的公告id
    :return: 响应对象
    '''
    try:
        notice = models.Notice.objects.get(id=u_id)
        notice.delete()
    except:
        pass
    finally:
        return redirect("/studentCMS/view_notice/")
