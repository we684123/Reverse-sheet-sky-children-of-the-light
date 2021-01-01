from pathlib import Path
import json

import cv2

from library import reverse_utilities as ru
from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())


# 讀取譜面
logger.info('generated  sheet ing...')
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './original_sheet.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _data = f.read()

data = json.loads(_data)
original_sheet = data['original_sheet']
o_s = original_sheet
fps = data['fps']


video_path = Path(rc['video_path'])
cap = cv2.VideoCapture(str(video_path))
frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# 處理影片
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
    mask, res = ru.get_keyboard_by_hsv(
        frame,
        rc['hsv']['lower_yellow'],
        rc['hsv']['upper_yellow'],
        rc['hsv']['lower_rad'],
        rc['hsv']['upper_rad'])
    binary = ru.get_binary_img(res, 127)
    video = ru.link_line(binary)

    # 僅取鍵盤畫面
    # 裁剪坐标为[y0:y1, x0:x1]
    left_upper = rc['left_upper']
    right_lower = rc['right_lower']
    video = ru.get_crop_img(video, left_upper, right_lower)

    # # 接下來要上色，表示音符觸發
    # # frame_count = 123
    # rt = list(filter(lambda x: x['frame'] == int(frame_count), o_s))
    # for

    cv2.imshow('Video Player', video)

    if cv2.waitKey(1) == ord('q'):  # 離開 BJ4
        break

    # 預計做 z x c 後退 暫停 前進
    # if cv2.waitKey(1) == ord('z'):
    #     cv2.CAP_PROP_POS_FRAMES - fps
    #     cap.get(cv2.CAP_PROP_POS_FRAMES)

    if cv2.waitKey(1) == ord('f'):  # f == flag
        _fc = frame_count
        while 1:
            rt = filter(lambda x: x['frame'] == int(_fc), o_s)
            rt = list(rt)
            if rt == []:
                _d = {'frame': frame_count, "type": "flag"},
                break
            else:
                _fc += 1
        o_s.append(_d)

cap.release()
cv2.destroyAllWindows()

#
