from pathlib import Path

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())


def ng(x):  # nothing
    pass


def get_aims_img():
    video_path = Path(rc['video_path'])  # "./sky.mkv"
    if not video_path.exists():
        logger.warning('video_path is not exist!')
        exit()
    cap = cv2.VideoCapture(str(video_path))

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
    cap.set(cv2.CAP_PROP_POS_FRAMES, specify_count)
    ret, frame = cap.read()
    return frame


def main(img):
    hsv = rc['hsv']
    cv2.namedWindow('hsv_config')
    img_zeros = np.zeros((300, 512, 3), np.uint8)

    # RGB 顏色調整軸0~255
    cv2.createTrackbar('H_1_0', 'hsv_config', hsv['lower_yellow'][0], 255, ng)
    cv2.createTrackbar('S_1_0', 'hsv_config', hsv['lower_yellow'][1], 255, ng)
    cv2.createTrackbar('V_1_0', 'hsv_config', hsv['lower_yellow'][2], 255, ng)
    cv2.createTrackbar('H_1_1', 'hsv_config', hsv['upper_yellow'][0], 255, ng)
    cv2.createTrackbar('S_1_1', 'hsv_config', hsv['upper_yellow'][1], 255, ng)
    cv2.createTrackbar('V_1_1', 'hsv_config', hsv['upper_yellow'][2], 255, ng)
    cv2.createTrackbar('H_2_0', 'hsv_config', hsv['lower_rad'][0], 255, ng)
    cv2.createTrackbar('S_2_0', 'hsv_config', hsv['lower_rad'][1], 255, ng)
    cv2.createTrackbar('V_2_0', 'hsv_config', hsv['lower_rad'][2], 255, ng)
    cv2.createTrackbar('H_2_1', 'hsv_config', hsv['upper_rad'][0], 255, ng)
    cv2.createTrackbar('S_2_1', 'hsv_config', hsv['upper_rad'][1], 255, ng)
    cv2.createTrackbar('V_2_1', 'hsv_config', hsv['upper_rad'][2], 255, ng)
    cv2.imshow('hsv_config', img_zeros)

    while(1):
        # 讀取調整軸顏色數值
        H_1_0 = cv2.getTrackbarPos('H_1_0', 'hsv_config')
        S_1_0 = cv2.getTrackbarPos('S_1_0', 'hsv_config')
        V_1_0 = cv2.getTrackbarPos('V_1_0', 'hsv_config')
        H_1_1 = cv2.getTrackbarPos('H_1_1', 'hsv_config')
        S_1_1 = cv2.getTrackbarPos('S_1_1', 'hsv_config')
        V_1_1 = cv2.getTrackbarPos('V_1_1', 'hsv_config')
        H_2_0 = cv2.getTrackbarPos('H_2_0', 'hsv_config')
        S_2_0 = cv2.getTrackbarPos('S_2_0', 'hsv_config')
        V_2_0 = cv2.getTrackbarPos('V_2_0', 'hsv_config')
        H_2_1 = cv2.getTrackbarPos('H_2_1', 'hsv_config')
        S_2_1 = cv2.getTrackbarPos('S_2_1', 'hsv_config')
        V_2_1 = cv2.getTrackbarPos('V_2_1', 'hsv_config')

        lower_yellow = np.array([H_1_0, S_1_0, V_1_0])
        upper_yellow = np.array([H_1_1, S_1_1, V_1_1])
        lower_rad = np.array([H_2_0, S_2_0, V_2_0])
        upper_rad = np.array([H_2_1, S_2_1, V_2_1])

        mask, res = ru.get_keyboard_by_hsv(
            img,
            lower_yellow, upper_yellow,
            lower_rad, upper_rad)

        pic = cv2.resize(mask, (960, 540), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('fix_hsv_video', pic)

        if cv2.waitKey(100) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    img = get_aims_img()
    main(img)


#
