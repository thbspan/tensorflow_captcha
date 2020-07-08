import random

from captcha.image import ImageCaptcha

import config


def random_captcha_text(char_set=None, captcha_size=4):
    if char_set is None:
        char_set = config.VALIDATE_CHAR
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha(width=config.IMAGE_WIDTH, height=config.IMAGE_HEIGHT, font_sizes=[config.FONT_SIZE])
    # 获得随机生成的验证码
    captcha_text = random_captcha_text()
    # 把验证码列表转为字符串
    captcha_text = ''.join(captcha_text)
    # 生成验证码
    image.generate(captcha_text)
    # 写到文件
    image.write(captcha_text, config.IMAGE_DIR + captcha_text + '.jpg')


if __name__ == '__main__':
    num = 10000
    for i in range(num):
        gen_captcha_text_and_image()
    print("gen done!")
