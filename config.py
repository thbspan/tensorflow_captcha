# -*- coding: utf-8 -*-
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

CHAR_SMALL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
CHAR_BIG = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

# VALIDATE_CHAR = NUMBER + CHAR_SMALL + CHAR_BIG
VALIDATE_CHAR = NUMBER[:]
CHAR_SET_LEN = len(VALIDATE_CHAR)

IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
FONT_SIZE = 35

IMAGE_DIR = "images/"
TF_RECORD_DIR = "captcha/"
MODELS_DIR = "models/"
