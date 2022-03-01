import base64
import os.path
import random
import string
import typing as t
from io import BytesIO

from PIL import Image
from PIL import ImageFilter
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype


class Bezier:
    def __init__(self):
        self.sequence = tuple([num / 20.0 for num in range(21)])
        self.beziers = {}

    @classmethod
    def pascal_row(cls, n):
        """ Returns n-th row of Pascal's triangle
        """
        result = [1]
        x, numerator = 1, n
        for denominator in range(1, n // 2 + 1):
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
        if n & 1 == 0:
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result))
        return result

    def make_bezier(self, number: int):
        """
        生成贝塞尔曲线
        :param number: 点数
        """
        try:
            return self.beziers[number]
        except KeyError:
            combinations = self.pascal_row(number - 1)
            result = []
            for num in self.sequence:
                tpowers = (num ** i for i in range(number))
                upowers = ((1 - num) ** i for i in range(number - 1, -1, -1))
                coefs = [c * a * b for c, a, b in zip(combinations,
                                                      tpowers, upowers)]
                result.append(coefs)
            self.beziers[number] = result
            return result


class Captcha:
    """
    Usages::
        name, text, images = captcha.generate_captcha()
    """
    def __init__(self):
        self._bezier = Bezier()
        self._dir = os.path.dirname(__file__)

    @staticmethod
    def instance():
        if not hasattr(Captcha, "_instance"):
            Captcha._instance = Captcha()
        return Captcha._instance

    def initialize(self, width: int = 200, height: int = 75, color: str = None,
                   fill_text: str = None, fonts: str = None) -> t.NoReturn:
        """
        初始化
        :param width: 宽度
        :param height: 高度
        :param color: 颜色
        :param fill_text: 文本
        :param fonts: 字体
        :return:
        """
        self._text = fill_text if fill_text else random.sample(
            string.ascii_uppercase + string.ascii_uppercase + '3456789', 4
        )
        self.fonts = fonts if fonts else [
            os.path.join(self._dir, 'fonts', font)
            for font in ['Arial.ttf', 'Georgia.ttf', 'actionj.ttf']
        ]
        self.width = width
        self.height = height
        self._color = color if color else self.random_color(
            0, 200, random.randint(220, 255)
        )

    @staticmethod
    def random_color(start: int, end: int, opacity: int = None) -> \
            t.Union[t.Tuple[int, int, int], t.Tuple[int, int, int, int]]:
        """
        生成随机颜色
        :param start: 颜色起始数值
        :param end: 颜色末尾数值
        :param opacity: 透明度
        :return: tuple (红、绿、蓝) or (红、绿、蓝, 透明度)
        """
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return red, green, blue

        return red, green, blue, opacity

    def gen_image_background(self, image: Image) -> Image:
        """
        设置背景
        :param image: Image对象
        :return: Image对象
        """
        Draw(image).rectangle([(0, 0), image.size],
                              fill=self.random_color(238, 255))
        return image

    @classmethod
    def gen_image_smooth(cls, image: Image) -> Image:
        """
        模糊图像
        :param image: Image对象
        :return: Image对象
        """
        return image.filter(ImageFilter.SMOOTH)

    def gen_image_curve(self, image: Image, width: int = 4,
                        number: int = 6) -> Image:
        """
        设置图像曲线
        :param image: Image对象
        :param width: 宽度
        :param number: 点数
        :return: image对象
        """
        dx, height = image.size
        dx /= number
        path = [(dx * i, random.randint(0, height))
                for i in range(1, number)]

        bcoefs = self._bezier.make_bezier(number - 1)

        points = []
        for coefs in bcoefs:
            points.append(tuple(sum([coef * p for coef, p in zip(coefs, ps)])
                                for ps in zip(*path)))

        Draw(image).line(points, fill=self._color, width=width)

        return image

    def gen_image_noise(self, image: Image, number: int = 50,
                        level: int = 2) -> Image:
        """
        设置图像噪点
        :param image: Image对象
        :param number: 点数
        :param level: 级别
        :return: Image对象
        """
        width, height = image.size
        dx = width / 10
        width -= dx
        dy = height / 10
        height -= dy

        draw = Draw(image)

        for i in range(number):
            x = int(random.uniform(dx, width))
            y = int(random.uniform(dy, height))
            draw.line(((x, y), (x + level, y)), fill=self._color, width=level)

        return image

    def gen_image_text(self, image: Image, fonts: t.Iterable,
                       font_sizes: t.Tuple[int] = None,
                       drawings: t.Iterable = None,
                       squeeze_factor: float = 0.75) -> Image:
        """
        设置图像文本内容
        :param image: Image对象
        :param fonts: 字体
        :param font_sizes: 字体大小
        :param drawings:
        :param squeeze_factor:
        :return: Image对象
        """
        color = self._color
        fonts = tuple([truetype(font, size)
                       for font in fonts
                       for size in font_sizes or (65, 70, 75)])
        draw = Draw(image)

        char_images = []
        for char in self._text:
            font = random.choice(fonts)
            char_width, char_height = draw.textsize(char, font=font)
            char_image = Image.new('RGB', (char_width, char_height), (0, 0, 0))
            char_draw = Draw(char_image)
            char_draw.text((0, 0), char, font=font, fill=color)
            char_image = char_image.crop(char_image.getbbox())

            for drawing in drawings:
                draw_obj = getattr(self, drawing)
                char_image = draw_obj(char_image)

            char_images.append(char_image)

        width, height = image.size
        offset = int((width - sum(
            int(i.size[0] * squeeze_factor) for i in char_images[:-1]
        ) - char_images[-1].size[0]) / 2)

        for char_image in char_images:
            char_width, char_height = char_image.size
            mask = char_image.convert('L').point(lambda i: i * 1.97)
            image.paste(char_image,
                        (offset, int((height - char_height) / 2)),
                        mask)
            offset += int(char_width * squeeze_factor)

        return image

    def gen_image(self) -> Image:
        """
        生成图像
        :return: Image对象
        """
        # 创建初始图像
        image = Image.new('RGB', (self.width, self.height), (64, 224, 208))
        # 设置图像背景
        image = self.gen_image_background(image)
        # 设置图像文本
        image = self.gen_image_text(image, self.fonts,
                                    drawings=['warp', 'rotate', 'offset'])
        # 设置图像曲线
        image = self.gen_image_curve(image)
        # 设置图像噪点
        image = self.gen_image_noise(image)
        # 模糊图像
        image = self.gen_image_smooth(image)

        return image

    @staticmethod
    def warp(image, dx_factor=0.27, dy_factor=0.21):
        width, height = image.size
        dx = width * dx_factor
        dy = height * dy_factor
        x1 = int(random.uniform(-dx, dx))
        y1 = int(random.uniform(-dy, dy))
        x2 = int(random.uniform(-dx, dx))
        y2 = int(random.uniform(-dy, dy))
        image2 = Image.new('RGB',
                           (width + abs(x1) + abs(x2),
                            height + abs(y1) + abs(y2)))
        image2.paste(image, (abs(x1), abs(y1)))
        width2, height2 = image2.size
        return image2.transform(
            (width, height), Image.QUAD,
            (x1, y1,
             -x1, height2 - y2,
             width2 + x2, height2 + y2,
             width2 - x2, -y1))

    @staticmethod
    def offset(image, dx_factor=0.1, dy_factor=0.2):
        width, height = image.size
        dx = int(random.random() * width * dx_factor)
        dy = int(random.random() * height * dy_factor)
        image2 = Image.new('RGB', (width + dx, height + dy))
        image2.paste(image, (dx, dy))
        return image2

    @staticmethod
    def rotate(image, angle=25):
        return image.rotate(
            random.uniform(-angle, angle), Image.BILINEAR, expand=1)

    def captcha(self, path: str = None, fmt: str = 'JPEG'):
        """
        创建图片验证码
        :param path: 文件保存路径
        :param fmt: 图片格式 PNG or JPEG
        :return: tuple, (name, text, StringIO.value)
        """
        image = self.gen_image()

        random_name = "".join(random.sample(
            string.ascii_lowercase + string.ascii_uppercase + '3456789', 24))

        random_text = "".join(self._text)

        out = BytesIO()
        image.save(out, format=fmt)
        if path:
            image.save(os.path.join(path, random_name), fmt)

        return random_name, random_text, self.generate_base64(out.getvalue())

    def generate_captcha(self) -> t.Tuple[str, str, str]:
        """
        生成图片验证码
        :return: tuple (StringIO.value, 验证码文本内容、验证码base64编码)
        """
        # 初始化
        self.initialize()
        # 返回验证码
        return self.captcha("")

    @staticmethod
    def generate_base64(image):
        base64_data = base64.b64encode(image)
        base64_data = 'data:image/bmp;base64,' + base64_data.decode()
        return base64_data


captcha = Captcha.instance()
