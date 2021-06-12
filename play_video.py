from pathlib import Path
import time
import json

import cv2
import numpy as np

from library import reverse_utilities as ru
from config import base
reverse_config = base.reverse_config()
rc = reverse_config

aims_folder_path = Path(rc['aims_folder_path'])
effect_config_path = \
    f"{str(aims_folder_path / './config/effect_config_parameter.json')}"
with open(effect_config_path, mode='r', encoding='utf-8') as f:
    content = f.read()
ec = json.loads(content)

left_upper = [int(ec['boundary_left']), int(ec['boundary_up'])]
right_lower = [int(ec['boundary_right']), int(ec['boundary_down'])]
hsv = {
    'lower_yellow': np.array(ec['hsv']['lower_yellow']),
    'upper_yellow': np.array(ec['hsv']['upper_yellow']),
    'lower_rad': np.array(ec['hsv']['lower_rad']),
    'upper_rad': np.array(ec['hsv']['upper_rad']),
}
binarization_thresh = int(ec['binarization_thresh'])
closing = bool(ec['use_closing'])

if __name__ == '__main__':
    video_path = Path(rc['video_path'])
    cap = cv2.VideoCapture(str(video_path))
    frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # 控制播放速度用
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_time = 1 / fps
    wait_time = 0
    area_time = 0
    now_time = time.time()

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

        # 僅取鍵盤畫面
        img = ru.get_crop_img(frame, left_upper, right_lower)

        # 轉灰階畫面顯示
        mask, res = ru.get_keyboard_by_hsv(
            img,
            hsv['lower_yellow'],
            hsv['upper_yellow'],
            hsv['lower_rad'],
            hsv['upper_rad'])
        img = ru.get_binary_img(res, binarization_thresh)
        if closing:
            img = ru.link_line(img)

        cv2.imshow('Video Player', img)

        # frame_time
        area_time = time.time() - now_time
        wait_time = abs(frame_time - area_time)
        time.sleep(wait_time)
        now_time = time.time()

        # print(f"area_time = {area_time} wait_time = {wait_time}")
        # if frame_count >= 500:
        #     print(area_time)
        #     break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#
