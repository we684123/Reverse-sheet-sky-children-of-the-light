from pathlib import Path
import json
import time

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(
    base.logger_config(),
    name='reverse_sheet_log'
)


# 基礎資訊獲取
aims_folder_path = Path(rc['aims_folder_path'])
video_path = aims_folder_path / Path(rc['video_path']).resolve()
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
        logger.info("影片讀取完畢")
        break
    if not ret:
        logger.info("影片讀取失敗，請確認影片格式...")
        break

    # 畫面處理
    crop_img = ru.get_crop_img(frame, left_upper, right_lower)
    mask, res = ru.get_keyboard_by_hsv(
        crop_img,
        hsv['lower_yellow'],
        hsv['upper_yellow'],
        hsv['lower_rad'],
        hsv['upper_rad'])
    img = ru.get_binary_img(res, binarization_thresh)
    if closing:
        img = ru.link_line(img)
    keyboards = ru.split_keyboard(
        img,
        rc['keyboards_X_format'],
        rc['keyboards_y_format']
    )
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
logger.info('✧◝(⁰▿⁰)◜✧')
sounds = ru.get_sounds()
sounds[7].play()
time.sleep(0.3)
sounds[8].play()
time.sleep(0.4)
sounds[9].play()
time.sleep(0.5)
sounds[14].play()
input('input any key to exit. 輸入任意值離開.')
