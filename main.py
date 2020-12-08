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
            print(f"i={i},j={j}")
            rd = [int(j * area_x), int(i * area_y)]
            lu = [int(rd[0] - area_x), int(rd[1] - area_y)]
            print(f"lu={lu},rd={rd}")
            print(f"{lu[1]}:{rd[1]}, {lu[0]}:{rd[0]}")
            new_img = img[lu[1]:rd[1], lu[0]:rd[0]]
            keyboard.append(new_img)
    return keyboard


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
    upper_left = [121, 530]
    lower_right = [623, 1400]
    crop_img = get_crop_img(binary, upper_left, lower_right)
    img = link_line(crop_img)

    cv2.imwrite("./video_link_line.png", img)

    keyboard = split_keyboard(img, 5, 3)
    keyboard[0]
    cv2.imwrite("./kbs/kb14.png", keyboard[i])

    for i in range(0, len(keyboard)):
        cv2.imwrite(f"./kbs/kb{i}.png", keyboard[i])

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
