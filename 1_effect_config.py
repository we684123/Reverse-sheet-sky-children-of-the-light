from pathlib import Path
import json
import sys

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from config import base

# ↓=====先處理設定檔=====↓

# ↓↓ 被拖到這個程式的影片(或設定檔)
# # NOTE: 需要驗證影片
if len(sys.argv) == 0:
    pass
if len(sys.argv) == 2:
    aims_video_file = sys.argv[1]

# ↓嘗試在local端找設定檔，如果沒有找到就去Github專案中下載設定檔模板↓


config = base.config()
logger = logger_generate.generate(
    base.logger_config(),
    name='reverse_sheet_log'
)

hsv = config['hsv']
binarization = config['binarization']
closing = config['closing']
effect_config_path = \
    f"{config['aims_folder_path']}/config/effect_config_parameter.json"


def ng(x):  # nothing
    pass


def remove_irrelevant(img, left: int, up: int, right: int, down: int):
    if up >= down:
        cv2.setTrackbarPos('up', _wn, up - 1)
        up = down - 1
    if left >= right:
        cv2.setTrackbarPos('left', _wn, left - 1)
        left = right - 1
    return ru.get_crop_img(img, [left, up], [right, down])


def img_resize(image, height_new, width_new):
    height, width = image.shape[0], image.shape[1]
    try:
        if width / height >= width_new / height_new:
            img_new = cv2.resize(
                image, (width_new, int(height * width_new / width)))
        else:
            img_new = cv2.resize(
                image, (int(width * height_new / height), height_new))
    except Exception:
        return image
    return img_new


video_path = Path(config['video_path'])
if not video_path.exists():
    logger.warning('video_path is not exist!')
    exit()
cap = cv2.VideoCapture(str(video_path))

frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
fps = int(cap.get(cv2.CAP_PROP_FPS))
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

duration = count / fps
minute = int(duration / 60)
seconds = int(duration % 60)

logger.info(f'frame_count = {frame_count}')
logger.info(f'fps = {fps}')
logger.info(f'count= {count}')
logger.info(f'duration= {duration}')
logger.info(f'minute= {minute}')
logger.info(f'seconds= {seconds}')
logger.info('---------------')
logger.info("".join(("d(`･∀･)b When you finish setting,",
                     " plz click 'result' window and",
                     " input keyboard 's' to save config.")))
logger.info('---------------')

specify_minute = input('plz input specify "minute" = ')
specify_seconds = input('plz input specify "seconds" = ')
lasting_seconds = input('plz input Lasting "seconds" = ')


specify_count = int(specify_minute) * 60 * fps + int(specify_seconds) * fps
cap.set(cv2.CAP_PROP_POS_FRAMES, specify_count)

return_frame = int(lasting_seconds) * fps + specify_count


# 調整視窗的名稱
_wn = 'effect_config'
cv2.namedWindow(_wn, 0)
img_zeros = np.zeros((300, 512, 3), np.uint8)

# 邊界、比例控制
cv2.createTrackbar('up', _wn, 0, frame_height, ng)
cv2.createTrackbar('down', _wn, frame_height, frame_height, ng)
cv2.setTrackbarMin('down', _wn, 1)
cv2.createTrackbar('left', _wn, 0, frame_width, ng)
cv2.createTrackbar('right', _wn, frame_width, frame_width, ng)
cv2.setTrackbarMin('right', _wn, 1)
cv2.createTrackbar('scale', _wn, 250, frame_width, ng)
cv2.setTrackbarMin('scale', _wn, 1)

# RGB 顏色調整軸0~255
cv2.createTrackbar('H_1_0', _wn, hsv['lower_yellow'][0], 179, ng)
cv2.createTrackbar('S_1_0', _wn, hsv['lower_yellow'][1], 255, ng)
cv2.createTrackbar('V_1_0', _wn, hsv['lower_yellow'][2], 255, ng)
cv2.createTrackbar('H_1_1', _wn, hsv['upper_yellow'][0], 179, ng)
cv2.createTrackbar('S_1_1', _wn, hsv['upper_yellow'][1], 255, ng)
cv2.createTrackbar('V_1_1', _wn, hsv['upper_yellow'][2], 255, ng)
cv2.createTrackbar('H_2_0', _wn, hsv['lower_rad'][0], 179, ng)
cv2.createTrackbar('S_2_0', _wn, hsv['lower_rad'][1], 255, ng)
cv2.createTrackbar('V_2_0', _wn, hsv['lower_rad'][2], 255, ng)
cv2.createTrackbar('H_2_1', _wn, hsv['upper_rad'][0], 179, ng)
cv2.createTrackbar('S_2_1', _wn, hsv['upper_rad'][1], 255, ng)
cv2.createTrackbar('V_2_1', _wn, hsv['upper_rad'][2], 255, ng)
cv2.createTrackbar('binarization_thresh', _wn, binarization['thresh'], 255, ng)
cv2.createTrackbar('use_closing', _wn, closing['use'], 1, ng)
cv2.imshow(_wn, img_zeros)

frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)
while cap.isOpened():
    ret, frame = cap.read()
    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
    logger.debug(frame_count)
    if frame_count == frame_end:
        logger.info("影片讀取完畢")
        break
    if not ret:
        logger.warning("影片讀取失敗，請確認影片格式...")
        break
    if frame_count > return_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, specify_count)
    boundary_up = cv2.getTrackbarPos('up', _wn)
    boundary_down = cv2.getTrackbarPos('down', _wn)
    boundary_left = cv2.getTrackbarPos('left', _wn)
    boundary_right = cv2.getTrackbarPos('right', _wn)
    scale = cv2.getTrackbarPos('scale', _wn)
    H_1_0 = cv2.getTrackbarPos('H_1_0', _wn)
    S_1_0 = cv2.getTrackbarPos('S_1_0', _wn)
    V_1_0 = cv2.getTrackbarPos('V_1_0', _wn)
    H_1_1 = cv2.getTrackbarPos('H_1_1', _wn)
    S_1_1 = cv2.getTrackbarPos('S_1_1', _wn)
    V_1_1 = cv2.getTrackbarPos('V_1_1', _wn)
    H_2_0 = cv2.getTrackbarPos('H_2_0', _wn)
    S_2_0 = cv2.getTrackbarPos('S_2_0', _wn)
    V_2_0 = cv2.getTrackbarPos('V_2_0', _wn)
    H_2_1 = cv2.getTrackbarPos('H_2_1', _wn)
    S_2_1 = cv2.getTrackbarPos('S_2_1', _wn)
    V_2_1 = cv2.getTrackbarPos('V_2_1', _wn)
    binarization_thresh = cv2.getTrackbarPos('binarization_thresh', _wn)
    use_closing = cv2.getTrackbarPos('use_closing', _wn)

    frame = remove_irrelevant(
        frame,
        boundary_left, boundary_up,
        boundary_right, boundary_down
    )

    lower_yellow = np.array([H_1_0, S_1_0, V_1_0])
    upper_yellow = np.array([H_1_1, S_1_1, V_1_1])
    lower_rad = np.array([H_2_0, S_2_0, V_2_0])
    upper_rad = np.array([H_2_1, S_2_1, V_2_1])
    mask, res = ru.get_keyboard_by_hsv(
        frame,
        lower_yellow, upper_yellow,
        lower_rad, upper_rad)

    img = ru.get_binary_img(res, binarization_thresh)

    if int(use_closing) == 1:
        img = ru.link_line(img)

    img = img_resize(img, scale, frame_width)
    cv2.imshow('result', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        logger.info('quit.')
        break
    elif key == ord('s'):
        effect_config = {
            "boundary_up": boundary_up,
            "boundary_down": boundary_down,
            "boundary_left": boundary_left,
            "boundary_right": boundary_right,
            "hsv": {
                "lower_yellow": lower_yellow.tolist(),
                "upper_yellow": upper_yellow.tolist(),
                "lower_rad": lower_rad.tolist(),
                "upper_rad": upper_rad.tolist()
            },
            "binarization_thresh": binarization_thresh,
            "use_closing": use_closing
        }
        logger.info(f'effect_config = \n{effect_config}')
        with open(effect_config_path, 'w', encoding='utf-8') as outfile:
            json.dump(effect_config, outfile)
        logger.info('config saved.')

#
