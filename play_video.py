from pathlib import Path

import cv2

import numpy as np


def get_keyboard_by_hsv(img):
    img_1 = img.copy()
    img_2 = img.copy()

    hsv1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 0, 0])
    upper_yellow = np.array([75, 255, 255])
    mask1 = cv2.inRange(hsv1, lower_yellow, upper_yellow)
    res1 = cv2.bitwise_and(img_1, img_1, mask=mask1)

    lower_rad = np.array([150, 0, 0])
    upper_rad = np.array([255, 255, 255])
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


def get_do_contour_by_binary(img):
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
    crop_img = img[ul[0]:lr[0], ul[1]:lr[1]]
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


if __name__ == '__main__':
    video_path = './sky.mkv'
    cap = cv2.VideoCapture(video_path)
    frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # 再處理剩下的
    while cap.isOpened():

        ret, frame = cap.read()

        # 正確讀取影像時 ret 回傳 True
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if frame_count == frame_end:
            print("影片讀取完畢")
            break
        if not ret:
            print("影片讀取失敗，請確認影片格式...")
            break

        # 轉灰階畫面顯示
        mask, res = get_keyboard_by_hsv(frame)
        binary = get_binary_img(res, 127)
        video = link_line(binary)

        # 僅取鍵盤畫面
        # 裁剪坐标为[y0:y1, x0:x1]
        upper_left = [121, 530]
        lower_right = [623, 1400]
        video = get_crop_img(video, upper_left, lower_right)

        cv2.imshow('Video Player', video)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#
