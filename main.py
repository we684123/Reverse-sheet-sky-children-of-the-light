from pathlib import Path

import cv2

import numpy as np


def get_keyboard_by_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([0, 0, 140])
    upper_yellow = np.array([75, 100, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(img, img, mask=mask)
    return mask, res


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
    img_path = str(Path("./color.png").resolve())
    template_img_path = str(Path("./template.png").resolve())

    img = cv2.imread(img_path)
    mask, res = get_keyboard_by_hsv(img)
    binary = get_binary_img(res, 127)

    template_binary = get_Template_binary_img(template_img_path)

    do_rt = get_matchTemplate_rt(binary, template_binary)
    upper_left, lower_right = get_crop_area(do_rt, template_binary)
    crop_binary = get_crop_img(binary, upper_left, lower_right)

    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    # cv2.imshow('img', img)
    # cv2.imshow('binary', binary)
    # cv2.imshow('template_binary', template_binary)
    # cv2.imshow('crop_binary', crop_binary)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    video_path = './sky.mkv'
    cap = cv2.VideoCapture(video_path)
    frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # 先到達指定偵數
    specify_count = 60
    for i in range(0, specify_count):
        ret, frame = cap.read()

    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
    print(f'frame_count = {frame_count}')
    print(cap.get(cv2.CAP_PROP_FPS))
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    mask, res = get_keyboard_by_hsv(frame)
    binary = get_binary_img(res, 127)
    cv2.imwrite("./video_binary.png", binary)

    template_binary = get_Template_binary_img("./video_binary.png")
    do_rt = get_matchTemplate_rt(binary, template_binary)
    upper_left, lower_right = get_crop_area(do_rt, template_binary)
    print('if frame_count == 0:')
    print(do_rt)
    print(upper_left)
    print(lower_right)

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

        crop_binary = get_crop_img(binary, upper_left, lower_right)

        cv2.imshow('Video Player', crop_binary)

        if cv2.waitKey(1) == ord('q'):
            print('===')
            print(do_rt)
            print(upper_left)
            print(lower_right)
            break

    cap.release()
    cv2.destroyAllWindows()

#
