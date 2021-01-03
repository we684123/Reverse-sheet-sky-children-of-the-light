from pathlib import Path

import cv2

from library import reverse_utilities as ru
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
hsv = rc['hsv']


if __name__ == '__main__':
    video_path = Path(rc['video_path'])
    cap = cv2.VideoCapture(str(video_path))
    frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

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

        cv2.imshow('Video Player', video)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#
