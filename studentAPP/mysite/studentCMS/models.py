from django.db import models
from tinymce.models import HTMLField


class AdminMan(models.Model):
    '''
    管理员表
    '''
    id = models.AutoField(primary_key=True, verbose_name="超管主键")
    adminName = models.CharField(max_length=30, unique=True, verbose_name="超管姓名")
    password = models.CharField(max_length=100, verbose_name="超管密码")

    class Meta:
        ordering = ['id']
        db_table = 't_admin'

    def __str__(self):
        return self.adminName


class Classes(models.Model):
    '''
    班级表，用到一点点，功能没有深入，只写学生的，教师的没有写，这个未完善吧
    '''
    id = models.AutoField(primary_key=True, verbose_name="班级主键")
    className = models.CharField(max_length=30, unique=True, verbose_name="班级名称")

    class Meta:
        ordering = ['id']
        db_table = 't_class'

    def __str__(self):
        return self.className


class Teacher(models.Model):
    '''
    教师表
    '''
    id = models.AutoField(primary_key=True, verbose_name="教师主键")
    teaName = models.CharField(max_length=30, unique=True, verbose_name="教师姓名")
    teaPassword = models.CharField(max_length=100, verbose_name="教师密码")
    teaAge = models.IntegerField(default=26, verbose_name="教师年龄")
    teaGender = models.CharField(default="男", max_length=6, verbose_name="教师性别", db_column="teaSex")
    teaLast_login = models.DateTimeField(null=True, blank=True, verbose_name="上次登录时间")
    teaPhoto = models.ImageField(upload_to="static/img/photo", default="static/img/tea.jpg", verbose_name="教师照片")
    is_shield = models.IntegerField(default=0, verbose_name="是否屏蔽")
    clsId = models.ManyToManyField(Classes)

    class Meta:
        ordering = ['id']
        db_table = 't_teacher'

    def __str__(self):
        return self.teaName


class AsSchedule(models.Model):
    '''
    教师任课表，感觉这个和学生选课差不多，就没用这个，只做了学生选课部分
    '''
    id = models.AutoField(primary_key=True, verbose_name="课程主键")
    courseName = models.CharField(max_length=30, unique=True, verbose_name="课程名")
    teaId = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        db_table = 't_as_schedule'

    def __str__(self):
        return self.courseName


class Course(models.Model):
    '''
    学生课程表
    '''
    id = models.AutoField(primary_key=True, verbose_name="课程主键")
    course = models.CharField(max_length=30, unique=True, verbose_name="课程名")
    desc = models.TextField(verbose_name="课程描述")

    class Meta:
        ordering = ['id']
        db_table = 't_course'

    def __str__(self):
        return self.course


class Student(models.Model):
    '''
    学生表
    '''
    id = models.AutoField(primary_key=True, verbose_name="学生主键")
    name = models.CharField(max_length=50, unique=True, verbose_name="学生姓名")
    password = models.CharField(max_length=100, verbose_name="学生密码")
    age = models.IntegerField(default=18, verbose_name="学生年龄")
    gender = models.CharField(default="男", max_length=6, verbose_name="学生性别")
    enter_date = models.DateTimeField(auto_now=True, verbose_name="入学时间")
    photo = models.ImageField(upload_to="static/img/photo", default="static/img/stu.jpg", verbose_name="学生照片")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="上次登录时间")
    remark = models.TextField(verbose_name="备注信息")
    is_shield = models.IntegerField(default=0, verbose_name="是否屏蔽")
    classId = models.ForeignKey(Classes, on_delete=models.PROTECT)
    courseId = models.ManyToManyField(Course)

    class Meta:
        ordering = ['id']
        db_table = 't_student'

    def __str__(self):
        return self.name


class SelectCourse(models.Model):
    '''
    学生选课表
    '''
    id = models.AutoField(primary_key=True, verbose_name="选课主键")
    selCourse1 = models.CharField(max_length=30, null=True, blank=True, verbose_name="课程名1")
    selCourse2 = models.CharField(max_length=30, null=True, blank=True, verbose_name="课程名2")
    selCourse3 = models.CharField(max_length=30, null=True, blank=True, verbose_name="课程名3")
    selCourse4 = models.CharField(max_length=30, null=True, blank=True, verbose_name="课程名4")
    stuName = models.CharField(max_length=30, null=True, blank=True, verbose_name="选课的人")

    class Meta:
        ordering = ['id']
        db_table = 't_select_course'

    def __str__(self):
        return self.selCourse1, self.selCourse2, self.selCourse3, self.selCourse4


class Score(models.Model):
    '''
    成绩表
    '''
    id = models.AutoField(primary_key=True, verbose_name="成绩主键")
    score = models.CharField(max_length=20, null=True, blank=True, verbose_name="学生成绩")
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        db_table = 't_score'

    def __str__(self):
        return self.score


# 留言板，需要有id，教师id，内容，发言时间
class Notice(models.Model):
    '''
    小论坛，只是一个小的留言板，通知公告之类的功能
    教师发言，超管管理（删除），学生只有查看功能,内容写成context（文本）了，后面使用时候要注意
    '''
    id = models.AutoField(primary_key=True, verbose_name="成绩主键")
    context = HTMLField(verbose_name="留言内容")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    mod_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time', 'id']
        db_table = 't_notice'
