from pathlib import Path

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())

hsv = rc['hsv']
binarization = rc['binarization']
closing = rc['closing']


def ng(x):  # nothing
    pass


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
lasting_seconds = input('plz input Lasting "seconds" = ')


specify_count = int(specify_minute) * 60 * fps + int(specify_seconds) * fps
cap.set(cv2.CAP_PROP_POS_FRAMES, specify_count)

return_frame = int(lasting_seconds) * fps + specify_count


# 調整視窗的名稱
_wn = 'effect_config'
cv2.namedWindow(_wn)
img_zeros = np.zeros((300, 512, 3), np.uint8)

# RGB 顏色調整軸0~255
cv2.createTrackbar('H_1_0', _wn, hsv['lower_yellow'][0], 255, ng)
cv2.createTrackbar('S_1_0', _wn, hsv['lower_yellow'][1], 255, ng)
cv2.createTrackbar('V_1_0', _wn, hsv['lower_yellow'][2], 255, ng)
cv2.createTrackbar('H_1_1', _wn, hsv['upper_yellow'][0], 255, ng)
cv2.createTrackbar('S_1_1', _wn, hsv['upper_yellow'][1], 255, ng)
cv2.createTrackbar('V_1_1', _wn, hsv['upper_yellow'][2], 255, ng)
cv2.createTrackbar('H_2_0', _wn, hsv['lower_rad'][0], 255, ng)
cv2.createTrackbar('S_2_0', _wn, hsv['lower_rad'][1], 255, ng)
cv2.createTrackbar('V_2_0', _wn, hsv['lower_rad'][2], 255, ng)
cv2.createTrackbar('H_2_1', _wn, hsv['upper_rad'][0], 255, ng)
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

    lower_yellow = np.array([H_1_0, S_1_0, V_1_0])
    upper_yellow = np.array([H_1_1, S_1_1, V_1_1])
    lower_rad = np.array([H_2_0, S_2_0, V_2_0])
    upper_rad = np.array([H_2_1, S_2_1, V_2_1])

    mask, res = ru.get_keyboard_by_hsv(
        frame,
        lower_yellow, upper_yellow,
        lower_rad, upper_rad)

    img = ru.get_binary_img(res, binarization_thresh)
    # (binary == mask).all()
    # np.unique(binary)
    # np.sum(binary)
    # np.sum(mask)
    if int(use_closing) == 1:
        img = ru.link_line(img)

    pic = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('result', pic)

    if cv2.waitKey(1) == ord('q'):
        break


#
