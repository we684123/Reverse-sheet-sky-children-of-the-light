from pathlib import Path
import time
import json

import cv2
import pygame

from library import reverse_utilities as ru
from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())


# 讀取譜面
logger.info('Loading  sheet...')
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

# load 聲音路徑
note_songs_path = Path('./note_songs')
sounds_path = []
for i in range(0, 15):
    sounds_path.append(note_songs_path / f"{i}.ogg")

# 載入聲音
pygame.mixer.init()
sounds = []
for p in sounds_path:
    sounds.append(pygame.mixer.Sound(p))

# 影片基礎
video_path = Path(rc['video_path'])
cap = cv2.VideoCapture(str(video_path))
frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# 控制播放速度用
frame_time = 1 / fps
wait_time = 0
area_time = 0
now_time = time.time()

# 處理聲音延遲問題
st_specify_count = fps * \
    (60 * int(rc['start_minute']) + int(rc['start_second']))

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

    # 僅取鍵盤畫面
    # 裁剪坐标为[y0:y1, x0:x1]
    left_upper = rc['left_upper']
    right_lower = rc['right_lower']
    video = ru.get_crop_img(frame, left_upper, right_lower)

    # 轉灰階畫面顯示
    mask, res = ru.get_keyboard_by_hsv(
        video,
        rc['hsv']['lower_yellow'],
        rc['hsv']['upper_yellow'],
        rc['hsv']['lower_rad'],
        rc['hsv']['upper_rad'])
    binary = ru.get_binary_img(res, 127)
    video = ru.link_line(binary)

    # # 接下來要上色，表示音符觸發
    # # frame_count = 123
    # rt = list(filter(lambda x: x['frame'] == int(frame_count), o_s))
    # for

    cv2.imshow('Video Player', video)

    # 播放對應的聲音用
    _for_sound_frame_count = frame_count - st_specify_count
    rt = filter(lambda x: x['frame'] == int(_for_sound_frame_count), o_s)
    rt = list(rt)
    for note in rt:
        sounds[note['keyboard']].play()

    # 控制播放速度用
    # frame_time
    area_time = time.time() - now_time
    wait_time = abs(frame_time - area_time)
    time.sleep(wait_time)
    now_time = time.time()

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

o_s
#
