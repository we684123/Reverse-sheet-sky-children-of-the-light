import sys

import cv2

import numpy as np


def video_player(video_path):

    # 調用cv2.VideoCapture()讀取影片
    cap = cv2.VideoCapture(video_path)  # "xxx.aiv"
    # 影片格式支援

    # cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)

    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(cap.get(cv2.CAP_PROP_FPS))
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("影片總偵數:", frame_end)

    while cap.isOpened():

        ret, frame = cap.read()
        img = frame

        # 正確讀取影像時 ret 回傳 True
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if frame_count == frame_end:
            print("影片讀取完畢")
            break
        if not ret:
            print("影片讀取失敗，請確認影片格式...")
            break

        # 轉灰階畫面顯示
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 提取鍵盤的顏色
        keyboard_colour = np.uint8([[[254, 250, 229]]])  # BGR
        hsv_keyboard_colour = cv2.cvtColor(keyboard_colour, cv2.COLOR_BGR2HSV)
        keyboard_colour2 = np.uint8([[[234, 213, 206]]])  # BGR
        hsv_keyboard_colour2 = cv2.cvtColor(keyboard_colour2, cv2.COLOR_BGR2HSV)

        lower_colour = np.array([95, 25, 254])
        upper_colour = np.array([113, 31, 234])

        mask = cv2.inRange(hsv, lower_colour, upper_colour)

        res = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imshow('frame', img)
        cv2.imshow('mask', mask)
        # cv2.imshow('res', res)

        # cv2.imshow('Video Player', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    print(argv)
    print('OpenCV 版本:', cv2.__version__)

    # 載入影片播放
    video_player("./sky.mkv")


if __name__ == '__main__':
    sys.exit(main())
