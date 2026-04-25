import json
import logging
import sys
from pathlib import Path

import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer

from config import base
from library import input_then_exit as ite
from library import logger_generate
from library import reverse_utilities as ru

"""
☆    　  ∧＿∧
  　　 (´・ω・｀)
　　　 /つ¶つ¶
( ((　／￣￣￣￣＼
　    |) ○ ○ ○ (|
　  ／″ 　　ν.　　＼
  ／＿＿＿＿＿＿＿＿＼
    ＼＿＼＿_／＿／
"""


def ng(x):  # nothing
    pass


# ↓=====先處理設定檔=====↓
# ↓ 嘗試在 local 端找設定檔
# ↓↓ 先把基本的東西訂好，並且從 base 中取基本的 config、logger
this_py_path = Path().absolute()
video_is_ready = False
config = base.config()
logger = logger_generate.generate(base.logger_config(), name="reverse_sheet_log")
# ↓↓ 再從 config 取得預設參數
hsv = config["hsv"]
binarization = config["binarization"]
closing = int(config["closing"]["use"])

aims_video_file = None

len_sys_argv = len(sys.argv)
logger.debug(f"{sys.argv=}")
logger.debug(f"{len_sys_argv=}")
IS_CHECK_PYTHON_FILE: bool = len_sys_argv == 1
IS_DRAG_VIDEO_TO_HERE: bool = len_sys_argv == 2  # noqa: PLR2004
IS_DRAG_VIDEO_TO_HERE_BY_IDE: bool = len_sys_argv == 3 and sys.argv[1] == "-f"  # noqa: PLR2004
IS_TOO_MUCH_ARGS: bool = len_sys_argv > 2  # noqa: PLR2004

# ↓↓ 處理被拖到這個程式的影片
if IS_DRAG_VIDEO_TO_HERE_BY_IDE:  # TODO(we684123): 這個之後移除  # noqa: TD003
    # 如果是在 IDE(Hydrogen)下的話則自動覆蓋 sys.argv
    # ps'影片如果改了的話，請記得改下面的影片名稱
    sys.argv = [str(this_py_path / "./test.py"), str(this_py_path / "能看見海的街道.mp4")]
if IS_CHECK_PYTHON_FILE:
    # 代表是直接點執行檔
    logger.info("🔎🈚Did not drag video to here,📗so will use tmp effect_config_parameter")
if IS_DRAG_VIDEO_TO_HERE:
    # 代表是拖影片檔到執行檔，此時需要驗證是否為影片
    aims_video_file = Path(sys.argv[1])
    logger.debug(sys.argv)
    try:
        cap = cv2.VideoCapture(str(aims_video_file))
        # 如果是影片那應該可以直接跑 read 而不出錯
        ret = None
        for i in range(2):
            ret, frame = cap.read()
        if not ret:
            logger.error(f'🎞️❌ "{aims_video_file!s}" not a Video.')
            ite.input_then_exit()
        video_is_ready = True
        del cap
        logger.info(f'🎞️✅ "{aims_video_file!s}" is a video, and can use.')
    except Exception:
        logger.exception(f'🎞️❌ "{aims_video_file!s}" not a Video.')
        ite.input_then_exit()
if IS_TOO_MUCH_ARGS:
    logger.error("🈵 sorry, but you only can drag a video to here, can't too more😅")
    ite.input_then_exit()
# ↓↓之後從 effect_config 中找到調好的臨時設定檔，並從裡面取值覆蓋
effect_config_path = Path(f"{this_py_path}/config/effect_config_parameter.json")
if effect_config_path.exists():
    # 如果存在就開始動作
    logger.info(f'📝✅ "{effect_config_path!s}" exists.')

    with effect_config_path.open(encoding="utf-8") as f:
        content = f.read()
    ec = json.loads(content)

    # 如果是用拖影片進來的，那就依拖的為主，如果是點的就拿 effect_config_path 覆蓋
    logger.debug(f"len(sys.argv) = {len_sys_argv}")
    if len_sys_argv == 1:  # ←這是點的
        aims_video_file = str(ec["aims_video_file"])

    left_upper = [int(ec["boundary_left"]), int(ec["boundary_up"])]
    right_lower = [int(ec["boundary_right"]), int(ec["boundary_down"])]
    hsv = {
        "lower_yellow": np.array(ec["hsv"]["lower_yellow"]),
        "upper_yellow": np.array(ec["hsv"]["upper_yellow"]),
        "lower_rad": np.array(ec["hsv"]["lower_rad"]),
        "upper_rad": np.array(ec["hsv"]["upper_rad"]),
    }
    binarization_thresh = int(ec["binarization_thresh"])
    closing = bool(ec["closing"])
    frame_start = int(ec["frame_start"])
    frame_end = int(ec["frame_end"])
else:
    logger.warning(f'📝🈚 "{effect_config_path!s}" not exists.')

# ↓=====開始處理影片=====↓
logger.debug(f"str(aims_video_file) = {aims_video_file!s}")
cap = cv2.VideoCapture(str(aims_video_file))
frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
fps = int(cap.get(cv2.CAP_PROP_FPS))
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

duration = count / fps
minute = int(duration / 60)
seconds = int(duration % 60)

logger.info(f"frame_count = {frame_count}")
logger.info(f"fps = {fps}")
logger.info(f"count= {count}")
logger.info(f"duration= {duration}")
logger.info(f"minute= {minute}")
logger.info(f"seconds= {seconds}")
logger.info("---------------")
logger.info("d(`･∀･)b When you finish setting, plz click 'result' window and input keyboard 's' to save config.")
logger.info("---------------")

# specify_minute = input('plz input specify "minute" = ')
# specify_seconds = input('plz input specify "seconds" = ')
# lasting_seconds = input('plz input Lasting "seconds" = ')
#
#
# specify_count = int(specify_minute) * 60 * fps + int(specify_seconds) * fps
# cap.set(cv2.CAP_PROP_POS_FRAMES, specify_count)
#
# return_frame = int(lasting_seconds) * fps + specify_count


# 調整視窗的名稱
_wn = "effect_config"
cv2.namedWindow(_wn, 0)
_wn2 = "hsv_color_config"
cv2.namedWindow(_wn2, 0)
_wn3 = "Sheet Player"
cv2.namedWindow(_wn3, 0)
img_zeros = np.zeros((100, 512, 3), np.uint8)

# 邊界、比例控制
cv2.createTrackbar("up", _wn, 0, frame_height, ng)
cv2.createTrackbar("down", _wn, frame_height, frame_height, ng)
# cv2.setTrackbarMin('down', _wn, 1)
cv2.createTrackbar("left", _wn, 0, frame_width, ng)
cv2.createTrackbar("right", _wn, frame_width, frame_width, ng)
# cv2.setTrackbarMin('right', _wn, 1)
# cv2.setTrackbarMax('right', _wn, frame_width)
cv2.createTrackbar("scale", _wn, 250, frame_width, ng)
# cv2.setTrackbarMin('scale', _wn, 1)
cv2.createTrackbar("binarization_thresh", _wn, binarization["thresh"], 255, ng)
cv2.createTrackbar("closing", _wn, closing, 1, ng)
cv2.createTrackbar("original", _wn, 0, 1, ng)
cv2.imshow(_wn, img_zeros)

# RGB 顏色調整軸0~255
cv2.createTrackbar("H_1_0", _wn2, hsv["lower_yellow"][0], 179, ng)
cv2.createTrackbar("S_1_0", _wn2, hsv["lower_yellow"][1], 255, ng)
cv2.createTrackbar("V_1_0", _wn2, hsv["lower_yellow"][2], 255, ng)
cv2.createTrackbar("H_1_1", _wn2, hsv["upper_yellow"][0], 179, ng)
cv2.createTrackbar("S_1_1", _wn2, hsv["upper_yellow"][1], 255, ng)
cv2.createTrackbar("V_1_1", _wn2, hsv["upper_yellow"][2], 255, ng)
cv2.createTrackbar("H_2_0", _wn2, hsv["lower_rad"][0], 179, ng)
cv2.createTrackbar("S_2_0", _wn2, hsv["lower_rad"][1], 255, ng)
cv2.createTrackbar("V_2_0", _wn2, hsv["lower_rad"][2], 255, ng)
cv2.createTrackbar("H_2_1", _wn2, hsv["upper_rad"][0], 179, ng)
cv2.createTrackbar("S_2_1", _wn2, hsv["upper_rad"][1], 255, ng)
cv2.createTrackbar("V_2_1", _wn2, hsv["upper_rad"][2], 255, ng)
cv2.imshow(_wn2, img_zeros)

cv2.createTrackbar("replay_st", _wn3, 0, count, ng)
cv2.createTrackbar("replay_end", _wn3, count, count, ng)
cv2.createTrackbar("progress", _wn3, 0, count, ng)
cv2.imshow(_wn2, img_zeros)


frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)
replay_st = int(cv2.getTrackbarPos("replay_st", _wn3))
replay_end = int(cv2.getTrackbarPos("replay_end", _wn3))

# 處理音樂播放
player = MediaPlayer(str(aims_video_file))

while cap.isOpened():
    ret, frame = cap.read()
    frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    logger.debug(f"frame_count = {frame_count}")
    cv2.setTrackbarPos("progress", _wn3, frame_count)

    audio_frame, val = player.get_frame()
    if val != "eof" and audio_frame is not None:
        img, t = audio_frame
        logger.debug(f"t = {t}")

    if not ret:
        logger.warning("影片讀取失敗，請確認影片格式...")
        break

    replay_end = int(cv2.getTrackbarPos("replay_end", _wn3))
    if (frame_count > replay_end) or (frame_count >= frame_end):
        replay_st = cv2.getTrackbarPos("replay_st", _wn3)
        cap.set(cv2.CAP_PROP_POS_FRAMES, replay_st)

    boundary_up = cv2.getTrackbarPos("up", _wn)
    boundary_down = cv2.getTrackbarPos("down", _wn)
    boundary_left = cv2.getTrackbarPos("left", _wn)
    boundary_right = cv2.getTrackbarPos("right", _wn)
    scale = cv2.getTrackbarPos("scale", _wn)
    binarization_thresh = cv2.getTrackbarPos("binarization_thresh", _wn)
    closing = cv2.getTrackbarPos("closing", _wn)
    show_original = cv2.getTrackbarPos("original", _wn)
    H_1_0 = cv2.getTrackbarPos("H_1_0", _wn2)
    S_1_0 = cv2.getTrackbarPos("S_1_0", _wn2)
    V_1_0 = cv2.getTrackbarPos("V_1_0", _wn2)
    H_1_1 = cv2.getTrackbarPos("H_1_1", _wn2)
    S_1_1 = cv2.getTrackbarPos("S_1_1", _wn2)
    V_1_1 = cv2.getTrackbarPos("V_1_1", _wn2)
    H_2_0 = cv2.getTrackbarPos("H_2_0", _wn2)
    S_2_0 = cv2.getTrackbarPos("S_2_0", _wn2)
    V_2_0 = cv2.getTrackbarPos("V_2_0", _wn2)
    H_2_1 = cv2.getTrackbarPos("H_2_1", _wn2)
    S_2_1 = cv2.getTrackbarPos("S_2_1", _wn2)
    V_2_1 = cv2.getTrackbarPos("V_2_1", _wn2)

    frame = ru.remove_irrelevant(frame, boundary_left, boundary_up, boundary_right, boundary_down, _wn)

    lower_yellow = np.array([H_1_0, S_1_0, V_1_0])
    upper_yellow = np.array([H_1_1, S_1_1, V_1_1])
    lower_rad = np.array([H_2_0, S_2_0, V_2_0])
    upper_rad = np.array([H_2_1, S_2_1, V_2_1])
    mask, res = ru.get_keyboard_by_hsv(frame, lower_yellow, upper_yellow, lower_rad, upper_rad)

    img = ru.get_binary_img(res, binarization_thresh)

    if int(closing) == 1:
        img = ru.link_line(img)

    img = ru.img_resize(img, scale, frame_width)
    cv2.imshow("result", img)
    if show_original:
        cv2.imshow("result_original", frame)

    # ===== 處理keyboard輸入 =====
    input_key = cv2.waitKey(1)
    if input_key == ord("q"):  # 離開 BJ4
        logger.info("quit.")
        break
    elif input_key == ord("s"):
        effect_config = {
            "aims_video_file": str(aims_video_file),
            "boundary_up": boundary_up,
            "boundary_down": boundary_down,
            "boundary_left": boundary_left,
            "boundary_right": boundary_right,
            "hsv": {
                "lower_yellow": lower_yellow.tolist(),
                "upper_yellow": upper_yellow.tolist(),
                "lower_rad": lower_rad.tolist(),
                "upper_rad": upper_rad.tolist(),
            },
            "binarization_thresh": binarization_thresh,
            "closing": closing,
            "frame_start": replay_st,
            "frame_end": replay_end,
        }
        logger.info(f"effect_config = \n{effect_config}")
        with effect_config_path.open("w", encoding="utf-8") as outfile:
            json.dump(effect_config, outfile, ensure_ascii=False, indent=2)
        logger.info(f'📝✨ create "{effect_config_path!s}"✅.')
        logger.info("config saved.")
    # 處理進度
    CHANGE_TIME: None | int = None
    if input_key == ord("w"):
        logger.debug("w trigger")
        cv2.setTrackbarPos("change", _wn3, 1)
        CHANGE_TIME = 1

    if input_key == ord("e"):
        logger.debug("e trigger")
        if CHANGE_TIME == 1:
            aims_frame = cv2.getTrackbarPos("Time_line", _wn3)
            cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)
            cv2.setTrackbarPos("change", _wn3, 0)
            CHANGE_TIME = 0
if logger.level == logging.DEBUG:
    input("input enter to exit.")

player.close_player()
cap.release()
cv2.destroyAllWindows()
