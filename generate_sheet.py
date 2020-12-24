from pathlib import Path

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())


# 基礎資訊獲取
video_path = Path(reverse_config['video_path']).resolve()
if not video_path.exists():
    logger.warning('video_path is not exist!')
    exit()
cap = cv2.VideoCapture(str(video_path))
frame_end = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
duration = frame_end / fps
minute = int(duration / 60)
seconds = int(duration % 60)

logger.info('base data got it!')

# 先到達指定偵數
st_specify_count = fps * \
    (60 * int(rc['start_minute']) + int(rc['start_second']))

for i in range(0, st_specify_count):
    ret, frame = cap.read()

ed_specify_count = fps * (60 * int(rc['end_minute']) + int(rc['end_second']))

# 再處理剩下的
# 生成 frame_keyboards
frame_keyboards = []
logger.info('frame_keyboards now is generating, need more times,')
logger.info('maybe eat something? for wait time~')
while cap.isOpened():
    ret, frame = cap.read()
    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
    if frame_count == frame_end or frame_count == ed_specify_count:
        print("影片讀取完畢")
        break
    if not ret:
        print("影片讀取失敗，請確認影片格式...")
        break

    # 畫面處理
    mask, res = ru.get_keyboard_by_hsv(frame)
    binary = ru.get_binary_img(res, 127)
    left_upper = rc['left_upper']
    right_lower = rc['right_lower']
    crop_img = ru.get_crop_img(binary, left_upper, right_lower)
    img = ru.link_line(crop_img)
    keyboards = ru.split_keyboard(img, 5, 3)
    keyboards_count = []
    for k in keyboards:
        keyboards_count.append(ru.get_img_number_count(k))
    frame_keyboards.append(keyboards_count)

with open('./frame_keyboards.txt', mode='w', encoding='utf-8') as f:
    f.write(str(frame_keyboards))
logger.info('frame_keyboards is generated!')
logger.info('now start generated original sheet...')
# ------------------
# with open('./frame_keyboards.txt', mode='r', encoding='utf-8') as f:
#     frame_keyboards = f.read()

# frame_keyboards = json.loads(frame_keyboards)


# 先來定義一下 kb_list 格式
kb_list = []
for i in range(0, len(frame_keyboards[0])):
    # logger.debug(frame_keyboards[0][i])
    kb_list.append([])

# 再來要找區域的像素數量總和
max_pixel_len = 0
for i in range(0, len(frame_keyboards[0])):
    # logger.debug(frame_keyboards[0][i])
    try:
        b = frame_keyboards[0][i][0]
        k = frame_keyboards[0][i][1]
        max_pixel_len = b + k
        break
    except Exception as e:
        e
        pass

for i in frame_keyboards:
    for j in range(0, len(i)):
        kb_list[j].append(max_pixel_len - i[j][0])


# 狀態器初始化
refractory_time = 35  # 單位 偵數
temp_state_list = []  # 狀態器陣列
for i in range(0, len(frame_keyboards[0])):
    temp_state = {
        "st_frame": 0,
        "refractory": False
    }
    temp_state_list.append(temp_state)

# 生成閥值陣列
trigger_valve = []
for i in kb_list:
    mean = int(np.mean(i))
    # logger.debug(mean)
    trigger_valve.append(mean / 2)


len(frame_keyboards)
len(kb_list)
# 譜面生成
sheet = [].copy()
for n in range(0, len(kb_list)):
    # n = 1
    for m in range(0, len(frame_keyboards)):
        # m = 0
        # logger.debug('+')
        track = n
        after_time = (m - temp_state_list[track]['st_frame'])
        refractory_timeout = after_time > refractory_time
        trigger = kb_list[track][m] < trigger_valve[n]
        if trigger and refractory_timeout:
            # logger.debug('.')
            temp_state_list[track]['st_frame'] = m
            temp_state_list[track]['refractory'] = True
            sheet.append({"frame": m, "keyboard": track})

sort_sheet = sorted(sheet, key=lambda s: s['frame'])
sort_sheet
logger.info('generated original sheet done.')
with open('./sort_sheet.txt', mode='w', encoding='utf-8') as f:
    f.write(str(sort_sheet))
