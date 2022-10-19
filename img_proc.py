import os.path

import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

def resizeAndPad(img, size, pad_color=0):

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC


    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h
    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(pad_color, (list, tuple, np.ndarray)): # color image but only one color provided
        pad_color = [pad_color]*3
    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=pad_color)

    return scaled_img


def getOutlineImg(img):
    return cv2.Canny(img, 25,101)
    # return cv2.Canny(img, 25, 150)

def getColoredImage(img, new_color, pattern_image):

    hsv_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv_image)
    new_hsv_image = hsv_image
    if new_color is not None:
        color = np.uint8([[new_color]])
        hsv_color = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
        h.fill(hsv_color[0][0][0])  # todo: optimise to handle black/white walls
        s.fill(hsv_color[0][0][1])
        new_hsv_image = cv2.merge([h, s, v])

    else:
        pattern = cv2.imread(pattern_image)
        hsv_pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2HSV)
        hp, sp, vp = cv2.split(hsv_pattern)
        new_hsv_image = cv2.merge([hp, sp, v])

    new_rgb_image = cv2.cvtColor(new_hsv_image, cv2.COLOR_HSV2RGB)
    return new_rgb_image


def selectWall(outline_img, position):
    h, w = outline_img.shape[:2]

    wall = outline_img.copy()
    scaled_mask = resizeAndPad(outline_img, (h+2,w+2), 255)
    scaled_mask = np.uint8(scaled_mask)
    wall = np.uint8(wall)
    cv2.floodFill(wall, scaled_mask, position, 255)   # todo: can be optimised later
    cv2.subtract(wall, outline_img, wall)
    return wall


def mergeImages(img, colored_image, wall):
    colored_image = cv2.bitwise_and(colored_image, colored_image, mask=wall)
    marked_img = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(wall))
    final_img = cv2.bitwise_xor(colored_image, marked_img)
    return final_img



def changeColor(org_img, new_img, position, color, pattern_image = None):
    colored_image = getColoredImage(org_img, color, pattern_image)
    outline_img = getOutlineImg(org_img)
    selected_wall = selectWall(outline_img, position)
    final_img = mergeImages(new_img, colored_image, selected_wall)
    return final_img

 changeColor(r'C:\Users\user\Videos\1.jpg',r'C:\Users\user\Videos\1.jpg',(300,100),(255,0,0),None);


