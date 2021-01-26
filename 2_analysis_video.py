from pathlib import Path
import json
import time

import cv2

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())


# 基礎資訊獲取
aims_folder_path = Path(rc['aims_folder_path'])
video_path = aims_folder_path / Path(rc['video_path']).resolve()
left_upper = rc['left_upper']
right_lower = rc['right_lower']

if not video_path.exists():
    logger.warning('video_path is not exist!')
    exit()
cap = cv2.VideoCapture(str(video_path))
frame_end = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
duration = frame_end / fps
minute = int(duration / 60)
seconds = int(duration % 60)
hsv = rc['hsv']
binarization = rc['binarization']
closing = rc['closing']

logger.info('base data got it!')

# 先到達指定偵數
st_specify_count = fps * \
    (60 * int(rc['start_minute']) + int(rc['start_second']))

cap.set(cv2.CAP_PROP_POS_FRAMES, st_specify_count)
ret, frame = cap.read()

ed_specify_count = fps * (60 * int(rc['end_minute']) + int(rc['end_second']))

# 再處理剩下的
# 生成 frame_keyboards
frame_keyboards = []
logger.info((
    'analysis_from_video.json now is generating, need more times,',
    'maybe eat something, for wait time?'
))
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
    crop_img = ru.get_crop_img(frame, left_upper, right_lower)
    mask, res = ru.get_keyboard_by_hsv(
        crop_img,
        hsv['lower_yellow'],
        hsv['upper_yellow'],
        hsv['lower_rad'],
        hsv['upper_rad'])
    img = ru.get_binary_img(res, binarization['thresh'])
    if closing['use']:
        img = ru.link_line(img)
    keyboards = ru.split_keyboard(img, 5, 3)
    keyboards_count = []
    for k in keyboards:
        keyboards_count.append(ru.get_img_number_count(k))
    frame_keyboards.append(keyboards_count)
logger.info('analysis_from_video.json is generated!')
logger.info('now to save data...')


# 生成完後要儲存資料
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './analysis_from_video.json'
with open(str(_temp), mode='w', encoding='utf-8') as f:
    data = {
        "notes": str(frame_keyboards),
        "frame_end": frame_end,
        "fps": fps,
        "duration": duration,
        "minute": minute,
        "seconds": seconds,
        "st_specify_count": st_specify_count,
        "ed_specify_count": ed_specify_count,
    }
    f.write(json.dumps(data))
logger.info('save data done.')
logger.info('Please proceed to the next action.')

# 播放音樂表示完結了~
# 🎵╰(´꒳`⸝⸝⸝)╯🎵  ✧◝(⁰▿⁰)◜✧
# 花媽廚房好囉~
print('✧◝(⁰▿⁰)◜✧')
sounds = ru.get_sounds()
sounds[7].play()
time.sleep(0.3)
sounds[8].play()
time.sleep(0.4)
sounds[9].play()
time.sleep(0.5)
sounds[14].play()
input('input any key to exit. 輸入任意值離開.')
