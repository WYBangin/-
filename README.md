# studentManagementSystem
选课功能的实现，关于表的关联操作 教师发表公告，实现一小时只能发一条 管理员、教师、学生三种角色功能的划分 常规的密码加密，验证码、三次登录错误，显示需要验证码登录 管理员可以屏蔽学生或教师，不让其登录啊，（学生休学可用。。。） 教师生成学生成绩、管理员开设课程等等功能的实现。

* 安卓依赖 *
    studentManagementSystem目录下, 执行 pip3 install -r requirements.txt
* 配置文件 *
    -- studentAPP/mysite/mysite/settings.py
    -- 'ENGINE' 配置数据库类型
    -- 'NAME': 数据库名称
    -- 'USER': 数据库账号
    -- 'PASSWORD' 数据库密码

    这里采用MySQL数据库, 需创建名为db_studentCMS的数据库。
    创建数据库后, 然后执行以下命令:
        python manage.py makemigrations
        python manage.py migrate (如果都是ok，则证明数据库同步完成)
* 运行命令 *
    studentAPP/mysite目录下, 执行 python manage.py runserver 0.0.0.0:9999 (9999是是端口号, 可修改)
    然后访问本地：http://127.0.0.1:9999/studentCMS/index/  (即可秀出你的操作)
    http://127.0.0.1:9999/studentCMS/reg/ (注册页)
    http://127.0.0.1:9999/studentCMS/login/ (登录页)

-- 因为后面做了权限限制,可能直接让登录，可先通过http://127.0.0.1:9999/studentCMS/reg/ 注册账号