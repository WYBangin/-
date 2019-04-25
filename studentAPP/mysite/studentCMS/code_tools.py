import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

'''
    这个一个验证码工具类，用于产生图形验证码
'''


def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_random_char():
    '''
    从数字、大小写字母里生成随机字符
    :return: 生成随机字符串
    '''
    random_num = str(random.randint(0, 9))
    random_lower = chr(random.randint(97, 122))  # 小写字母a~z
    random_upper = chr(random.randint(65, 90))  # 大写字母A~Z
    random_char = random.choice([random_num, random_lower, random_upper])
    return random_char


# 图片的宽和高
width = 120
height = 30


# 随机画线，在图片宽高范围内随机生成2个坐标点，并通过随机颜色产生线条
def draw_line(draw):
    for i in range(4):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())


# 随机画点，随机生成横纵坐标点
def draw_point(draw):
    for i in range(40):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=get_random_color())


def create_img():
    bg_color = get_random_color()
    # 创建一张随机颜色的背景图片 size包含图片的宽高，单位px
    img = Image.new(mode="RGB", size=(width, height), color=bg_color)
    # 获取图片画笔，用于描绘字
    draw = ImageDraw.Draw(img)
    # 修改字体
    font = ImageFont.truetype(font="arial.ttf", size=25)
    code = ""
    for i in range(4):
        # 随机生成4种字符加颜色
        random_txt = get_random_char()
        code += random_txt
        txt_color = get_random_color()
        # 避免文字颜色和背景色一致重合
        while txt_color == bg_color:
            txt_color = get_random_color()
        # 根据坐标填充文字
        draw.text((30*i+3, 2), text=random_txt, fill=txt_color, font=font)
        # 画干扰点
        draw_point(draw)

        # 打开图片操作，并保存在当前文件夹下,如果需要保存图片，可以用这种方法
        # with open("test.png", "wb") as f:
        #     img.save(f, format="png")

    # 为了让图片上少一点干扰线，故把画干扰线的放在外面，就是只画四条干扰线
    draw_line(draw)

    return img, code


if __name__ == '__main__':
    create_img()


