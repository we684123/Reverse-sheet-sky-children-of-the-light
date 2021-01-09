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
o_s_2 = o_s.copy()
o_s_3 = o_s.copy()
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


# 加個進度條
def nothing(x):
    pass


cv2.namedWindow('Video Player')
cv2.createTrackbar('Time_line', 'Video Player', 0, int(frame_end), nothing)
cv2.createTrackbar('change', 'Video Player', 0, 1, nothing)
change_Time = 0

# 加個時間狀態
time_stop = False
# 處理影片
while cap.isOpened():

    if not time_stop:
        ret, frame = cap.read()

        # 正確讀取影像時 ret 回傳 True
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if frame_count == frame_end:
            print("影片讀取完畢")
            break
        if not ret:
            print("影片讀取失敗，請確認影片格式...")
            break

        # 設定時間軸
        if change_Time == 0:
            cv2.setTrackbarPos('Time_line', 'Video Player', int(frame_count))

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
        _fsfc = int(_for_sound_frame_count)
        rt = filter(lambda x: x['frame'] == _fsfc, o_s_2)
        rt = list(rt)
        for note in rt:
            sounds[note['keyboard']].play()

        # 控制播放速度用
        # frame_time
        area_time = time.time() - now_time
        wait_time = abs(frame_time - area_time)
        time.sleep(wait_time)
        now_time = time.time()

    input_key = cv2.waitKey(1)
    if input_key == ord('q'):  # 離開 BJ4
        break

    # z x c 後退 暫停 前進
    if input_key == ord('x'):
        print('x tigger')
        time_stop = not time_stop
        print(time_stop)
        # if cv2.waitKey(0) == ord('x'):
        #     continue
    if input_key == ord('z'):
        print('z tigger')
        aims_frame = frame_count - fps * 5

        if aims_frame < 0:
            aims_frame = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)
    if input_key == ord('c'):
        print('c tigger')
        aims_frame = frame_count + fps * 5
        if aims_frame >= frame_end:
            aims_frame = frame_end
        cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)

    # 處理進度
    if input_key == ord('s'):
        cv2.setTrackbarPos('change', 'Video Player', 1)
        change_Time = 1
    if input_key == ord('d'):
        if change_Time == 1:
            aims_frame = cv2.getTrackbarPos('Time_line', 'Video Player')
            cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)
            cv2.setTrackbarPos('change', 'Video Player', 0)
            change_Time = 0

    if input_key == ord('f'):  # f == flag
        print('f tigger')
        _for_flag_frame_count = int(frame_count - st_specify_count)
        _fffc = int(_for_flag_frame_count)
        while 1:
            rt = filter(lambda x: x['frame'] == _fffc, o_s_3)
            rt = list(rt)
            if rt == []:
                _d = {'frame': frame_count, "type": "flag"}
                break
            else:
                _for_flag_frame_count += 1
        o_s.append(_d)

cap.release()
cv2.destroyAllWindows()

# print(o_s_3)
_temp = output_sheet_path / './030.json'
with open(str(_temp), mode='w', encoding='utf-8') as f:
    f.write(json.dumps(o_s))
#
