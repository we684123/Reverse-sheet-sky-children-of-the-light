import cv2

import numpy as np


def get_keyboard_by_hsv(img,
                        lower_yellow=[0, 11, 89],
                        upper_yellow=[39, 89, 255],
                        lower_rad=[148, 10, 72],
                        upper_rad=[255, 150, 255]):

    # lower_yellow = np.array([0, 0, 0])
    # upper_yellow = np.array([75, 255, 255])
    # lower_rad = np.array([150, 0, 0])
    # upper_rad = np.array([255, 255, 255])
    lower_yellow = np.array(lower_yellow)
    upper_yellow = np.array(upper_yellow)
    lower_rad = np.array(lower_rad)
    upper_rad = np.array(upper_rad)

    img_1 = img.copy()
    img_2 = img.copy()

    hsv1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv1, lower_yellow, upper_yellow)
    res1 = cv2.bitwise_and(img_1, img_1, mask=mask1)

    mask2 = cv2.inRange(hsv2, lower_rad, upper_rad)
    res2 = cv2.bitwise_and(img_2, img_2, mask=mask2)

    mask = cv2.add(mask1, mask2)
    res = cv2.add(res1, res2)
    return mask, res


def link_line(img):
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    img = erosion

    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)
    img = dilation
    return img


def get_binary_img(img, thresh):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary


def get_do_contour_by_binary(binary):
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_crop_area(do_rt, template):
    # img[127:432+w, 165:773+h]  # 裁剪坐标为[y0:y1, x0:x1]
    # print(do_rt)
    x = []
    y = []
    for i in do_rt:
        x.append(i[0])
        y.append(i[1])
    w = template.shape[1]
    h = template.shape[0]
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)

    upper_left = [min_y, min_x]
    lower_right = [max_y + h, max_x + w]
    return upper_left, lower_right


def get_crop_img(img, upper_left, lower_right):
    # img[127:432+w, 165:773+h]  # 裁剪坐标为[y0:y1, x0:x1]
    ul = upper_left
    lr = lower_right
    crop_img = img[lr[0]:ul[0], lr[1]:ul[1]]
    return crop_img


def get_matchTemplate_rt(img, template):
    # w = template.shape[1]
    # h = template.shape[0]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    do_rt = []  # x,y
    for pt in zip(*loc[::-1]):
        # print(pt)
        list_pt = list(pt)
        do_rt.append(list_pt)

        # cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    return do_rt


def get_Template_binary_img(template_img_path):
    template = cv2.imread(template_img_path)
    template_binary = get_binary_img(template, 127)
    return template_binary


def split_keyboard(img, x, y):
    # area = [0,1,2...(x*y-1)] 一維的喔!
    # 對應
    # [0, 1, 2, 3, 4,
    #  5, 6, 7, 8, 9,
    #  10, 11, 12, 13, 14]
    # x 是對應 "橫向" 有幾個鍵盤
    # y 是對應 "縱向" 有幾個鍵盤
    # x = 5
    # y = 3
    keyboard = []
    w = img.shape[1]
    h = img.shape[0]

    # 定義方向上的分個線數量
    split_line_x = (x)
    split_line_y = (y)

    # 定義一個鍵盤區塊大小
    area_x = w / split_line_x
    area_y = h / split_line_y

    # 這些 i j 測試用的
    i = 1
    i = 2
    i = 3

    j = 1
    j = 2
    j = 3
    j = 4
    j = 5

    for i in range(1, y + 1):
        for j in range(1, x + 1):
            # print(f"i={i},j={j}")
            rd = [int(j * area_x), int(i * area_y)]
            lu = [int(rd[0] - area_x), int(rd[1] - area_y)]
            # print(f"lu={lu},rd={rd}")
            # print(f"{lu[1]}:{rd[1]}, {lu[0]}:{rd[0]}")
            new_img = img[lu[1]:rd[1], lu[0]:rd[0]]
            keyboard.append(new_img)
    return keyboard


def get_img_number_count(keyboard):
    a = []
    for i in np.unique(keyboard):
        a.append(np.sum(keyboard == i))
    return a
