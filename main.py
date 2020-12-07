from pathlib import Path

import cv2

from matplotlib import pyplot as plt

import numpy as np


def get_keyboard(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([0, 0, 140])
    upper_yellow = np.array([75, 100, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(img, img, mask=mask)
    return mask, res


def get_binary_img(img, thresh):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    return binary


def get_do_contour_by_binary(img):
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


if __name__ == '__main__':
    img_path = str(Path("./color.png").resolve())
    template_img_path = str(Path("./template.png").resolve())

    img = cv2.imread(img_path)
    mask, res = get_keyboard(img)
    template = cv2.imread(template_img_path)

    binary = get_binary_img(res, 127)
    template_binary = get_binary_img(template, 127)

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    w = template.shape[1]
    h = template.shape[0]
    img2 = img
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img, top_left, bottom_right, 255, 2)

        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()

    contours = get_do_contour_by_binary(binary)

    cv2.drawContours(binary, contours, -1, (0, 255, 0), 3)

    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('img', img)
    cv2.imshow('binary', binary)
    cv2.imshow('template_binary', template_binary)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


#
