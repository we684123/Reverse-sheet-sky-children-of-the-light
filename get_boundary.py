import time
from pathlib import Path

import cv2
import numpy as np

from config import base
base = base.base()


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


def get_binary_img(img, thresh):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary


video_path = Path(base['video_path'])  # "./sky.mkv"
if video_path.exists():
    cap = cv2.VideoCapture(video_path)

    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = count / fps
    minute = int(duration / 60)
    seconds = int(duration % 60)

    print(f'frame_count = {frame_count}')
    print(f'fps = {fps}')
    print(f'count= {count}')
    print(f'duration= {duration}')
    print(f'minute= {minute}')
    print(f'seconds= {seconds}')

    specify_minute = input('plz input specify "minute" = ')
    specify_seconds = input('plz input specify "seconds" = ')

    specify_count = int(specify_minute) * 60 * fps + int(specify_seconds) * fps
    for i in range(0, specify_count):
        ret, frame = cap.read()
    mask, res = get_keyboard_by_hsv(frame)
    binary = get_binary_img(res, 127)

    cv2.imwrite("./binary.png", binary)

    print('===已生成 done===')
else:
    print('video_path is not exist!')
time.sleep(2)
