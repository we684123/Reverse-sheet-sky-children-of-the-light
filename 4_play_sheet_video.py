import json
import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from config import base
from library import logger_generate
from library import reverse_utilities as ru

reverse_config = base.config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())

CHOOSE_ENHANCE_SHEET = 2

# 讀取譜面
logger.info("Loading sheet...")
this_py_path = Path().absolute()

effect_config_path: Path = this_py_path / "./config/effect_config_parameter.json"
with effect_config_path.open(encoding="utf-8") as f:
    content: str = f.read()
ec = json.loads(content)

output_sheet_path = this_py_path / rc["output_sheet_path"]
_temp = output_sheet_path / "./native_sheet.json"

_temp2 = output_sheet_path / "./enhance_sheet.json"
if _temp2.exists():
    k = input("plz choose a file load.\n1 native_sheet.json\n2 enhance_sheet.json\n")
    if int(k) == CHOOSE_ENHANCE_SHEET:
        _temp = _temp2

with _temp.open(encoding="utf-8") as f:
    _data = f.read()

data = json.loads(_data)
original_sheet = data["original_sheet"]
o_s = original_sheet
o_s_2 = o_s.copy()
o_s_3 = o_s.copy()
o_s_4 = o_s.copy()
o_s_5 = o_s.copy()
fps = data["fps"]

# load 聲音路徑
sounds = ru.get_sounds()

# 影片基礎
video_path = Path(ec["aims_video_file"])
cap = cv2.VideoCapture(str(video_path))
frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# 控制播放速度用
frame_time = 1 / fps
wait_time = 0
area_time = 0
now_time = time.time()

# 處理聲音延遲問題
st_specify_count = ec["frame_start"]

# 處理附加動畫時間
max_effect_time = 0.4
max_effect_frame = max_effect_time * fps
feed_effect_time = 0.4
feed_effect_frame = feed_effect_time * fps
note_effect_time = 0.2
note_effect_frame = note_effect_time * fps
KEYBOARD_EFFECT_MAX_WIDTH = 20
KEYBOARD_EFFECT_MIN_VISIBLE_WIDTH = 3


with effect_config_path.open(encoding="utf-8") as f:
    content = f.read()
ec = json.loads(content)

# 畫面附加效果狀態器
# frame_count = 124
# temp_state_list = []
# o_s_4.append({'frame': 124, "type": "line_feed"})


def addition_to_video(img, frame_count, o_s):
    # def addition_lf():  # 換行效果登記
    #     # 這裡可以寫的效能更好一點，用指標跟狀態器達成
    #     # 但先不要，要沒時間了
    #     def ld_to_lf(x):
    #         if x['frame'] == int(frame_count) and x['type'] == 'line_feed':
    #             return x
    #     rt = list(filter(ld_to_lf, o_s))
    #     if rt != []:
    #         temp_state_list.append(rt[0])

    _for_addition_frame_count = frame_count - st_specify_count
    _fafc = _for_addition_frame_count

    def ld_to_lf(x) -> Any | None:
        if (abs(int(_fafc) - x["frame"]) < max_effect_frame) and (x["type"] in ("line_feed", "note")):
            return x
        return None

    temp_state_list = list(filter(ld_to_lf, o_s.copy()))

    for i in range(len(temp_state_list)):
        _e = temp_state_list[i]
        _ef = _e["frame"]
        _et = _e["type"]
        width = KEYBOARD_EFFECT_MAX_WIDTH - int(_fafc - _ef)
        # logger.debug(f"width = {width}")
        # logger.debug(type(width))

        _width_in_area = width > KEYBOARD_EFFECT_MIN_VISIBLE_WIDTH and width < KEYBOARD_EFFECT_MAX_WIDTH
        use_keyboard_effect = rc["play_effect_config"]["use_keyboard_effect"]
        _run_keyboard_effect = _width_in_area and use_keyboard_effect

        if _et == "line_feed":
            # logger.debug(width)
            # logger.debug(type(width))
            cv2.rectangle(img, (0, 0), (int(img.shape[1]), int(img.shape[0])), (255, 140, 0), width)
        elif _run_keyboard_effect and _et == "note":
            _ka = keyboard_area[_e["keyboard"]]
            # logger.debug(_ka)
            _keyboard_effect = rc["play_effect_config"]["keyboard_effect"]
            if _keyboard_effect == "center":
                cv2.rectangle(img, (int(_ka[2]), int(_ka[0])), (int(_ka[3]), int(_ka[1])), (255, 140, 0), width)
            elif _keyboard_effect == "upper_left":
                _x = int(_ka[3]) - int(_ka[2])
                _y = int(_ka[1]) - int(_ka[0])
                _x_d = int(_x / 11)
                _y_d = int(_y / 11)
                width -= 9
                # logger.debug("-----")
                # logger.debug(_x)
                # logger.debug(_y)
                # logger.debug(_x_d)
                # logger.debug(_y_d)

                cv2.rectangle(
                    img,
                    (int(_ka[2]), int(_ka[0])),
                    (int(_ka[2]) + _x_d * width, int(_ka[0]) + _y_d * width),
                    (255, 140, 0),
                    3,
                )
    return img


# 這給 createTrackbar 用的
def nothing(x):
    pass


cv2.namedWindow("Sheet Player")
# 加個進度條
cv2.createTrackbar("Time_line", "Sheet Player", 0, int(frame_end), nothing)
# # 加個觀察的目標鍵盤
# # # TODO(we684123): 14要改成可變動
# cv2.createTrackbar('listen_key', 'Sheet Player', 0, 14, nothing)
# change_key = 0
# 改變開關
cv2.createTrackbar("change", "Sheet Player", 0, 1, nothing)
CHANGE_TIME = 0

# 加個時間狀態
time_stop = False

# 狀態器初始化
temp_state_list = []  # 狀態器陣列
tsl = temp_state_list

# 僅取鍵盤畫面
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

# 獲取畫面鍵盤分割座標
ret, frame = cap.read()  # 這裡偷偷拿一
_v = ru.get_crop_img(frame, left_upper, right_lower)
keyboard_area = ru.get_split_keyboard_area(_v, rc["keyboards_X_format"], rc["keyboards_y_format"])

# 處理影片
# TODO(we684123): 這裡要修成符合pep8 最少分2區 waitkey + frame_處理 (影像讀取)
while cap.isOpened():
    frame_count: int | float = 0
    if not time_stop:
        ret, frame = cap.read()

        # 正確讀取影像時 ret 回傳 True
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if float(frame_count) is None:
            logger.error("frame_count can't be None")

        # logger.debug(f"frame_count = {frame_count}")
        if frame_count == frame_end:
            logger.info("影片讀取完畢")
            break
        if not ret:
            logger.info("影片讀取失敗，請確認影片格式...")
            break

        # 設定時間軸
        if CHANGE_TIME == 0:
            cv2.setTrackbarPos("Time_line", "Sheet Player", int(frame_count))

        video = ru.get_crop_img(frame, left_upper, right_lower)

        # 轉灰階畫面顯示
        mask, res = ru.get_keyboard_by_hsv(
            video, hsv["lower_yellow"], hsv["upper_yellow"], hsv["lower_rad"], hsv["upper_rad"]
        )
        img = ru.get_binary_img(res, binarization_thresh)
        if closing:
            img = ru.link_line(img)

        # # 接下來要上色，表 示音符觸發
        # # frame_count = 123
        # rt = list(filter(lambda x: x['frame'] == int(frame_count), o_s))
        # for
        add_ed_img = addition_to_video(img, frame_count, o_s)

        cv2.imshow("Sheet Player", add_ed_img)

        # 播放對應的聲音用
        _for_sound_frame_count = frame_count - st_specify_count
        _fsfc = int(_for_sound_frame_count)
        rt = filter(lambda x: x["frame"] == _fsfc, o_s_2)
        rt = list(rt)
        for note in rt:
            if "keyboard" in note:
                sounds[note["keyboard"]].play()
                logger.debug(f"🎵sounds = {note['keyboard']}")

        # 控制播放速度用
        # frame_time
        area_time = time.time() - now_time
        wait_time = abs(frame_time - area_time)
        time.sleep(wait_time)
        now_time = time.time()

    input_key = cv2.waitKey(1)
    if input_key == ord("q"):  # 離開 BJ4
        break

    # z x c 後退 暫停 前進
    if input_key == ord("x"):
        logger.info("x trigger")
        time_stop = not time_stop
        logger.info(time_stop)
        # if cv2.waitKey(0) == ord('x'):
        #     continue
    if input_key == ord("z"):
        logger.info("z trigger")
        aims_frame = frame_count - fps * 5

        aims_frame = max(aims_frame, 0)
        cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)
    if input_key == ord("c"):
        logger.info("c trigger")
        aims_frame = frame_count + fps * 5
        aims_frame = min(frame_end, aims_frame)
        cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)

    # 處理進度
    _d = None
    if input_key == ord("w"):
        logger.info("w trigger")
        cv2.setTrackbarPos("change", "Sheet Player", 1)
        CHANGE_TIME = 1

    if input_key == ord("e"):
        logger.info("e trigger")
        if CHANGE_TIME == 1:
            aims_frame = cv2.getTrackbarPos("Time_line", "Sheet Player")
            cap.set(cv2.CAP_PROP_POS_FRAMES, aims_frame)
            cv2.setTrackbarPos("change", "Sheet Player", 0)
            CHANGE_TIME = 0

    if input_key == ord("f"):  # f == flag
        logger.info("f trigger")
        _for_flag_frame_count = int(frame_count - st_specify_count)
        _fffc = int(_for_flag_frame_count)
        while 1:
            rt = filter(lambda x: x["frame"] == _fffc, o_s_3)
            rt = list(rt)
            if rt == []:
                _d = {
                    "frame": frame_count,
                    "type": "flag",
                }
                break
            else:
                _fffc += 1
        o_s.append(_d)
    if input_key == ord("a"):  # a == 'line_feed'
        logger.info("a trigger")
        logger.info(frame_count)
        _for_line_feed_frame_count = int(frame_count - st_specify_count)
        _flffc = int(_for_line_feed_frame_count)
        while 1:
            rt = filter(lambda x: x["frame"] == _flffc, o_s_5)
            rt = list(rt)
            if rt == []:
                _d = {
                    "frame": frame_count,
                    "type": "line_feed",
                    # "display": True
                }
                break
            else:
                _flffc += 1
        o_s.append(_d)
    if input_key == ord("s"):  # a == 'line_feed'
        logger.info("s trigger")
        logger.info(frame_count)
        rt = list(filter(lambda x: x["type"] == "line_feed", o_s.copy()))
        logger.info(f"rt = {rt}")
        if len(rt) == 0:
            logger.info("s鍵刪除無效，因為已經沒有分界線可以刪除了")
        else:
            _k = []
            for i in range(len(rt)):
                _k.append(int(rt[i]["frame"]) - frame_count)
            logger.info(f"_k = {_k}")
            logger.info(f"max _k = {max(_k)}")
            logger.info(f"rt[_k.index(max(_k))]  = {rt[_k.index(max(_k))]}")
            # rt[_k.index(max(_k))]
            del o_s[o_s.index(rt[_k.index(max(_k))])]

    if input_key == ord("j"):  # a == 'line_feed'
        logger.info("j trigger")
        rt = list(filter(lambda x: x["type"] == "line_feed", o_s.copy()))
        logger.info(rt)
cap.release()
cv2.destroyAllWindows()


# 最後把 enhance_sheet 譜面輸出
_temp = output_sheet_path / "./enhance_sheet.json"
with _temp.open(mode="w", encoding="utf-8") as f:
    new_data = {
        "original_sheet": sorted(o_s, key=lambda s: s["frame"]),
        "frame_end": data["frame_end"],
        "fps": data["fps"],
        "duration": data["duration"],
        "minute": data["minute"],
        "seconds": data["seconds"],
        "st_specify_count": data["st_specify_count"],
        "ed_specify_count": data["ed_specify_count"],
        "trigger_valve": data["trigger_valve"],
        "cool_down_frame": data["cool_down_frame"],
    }
    f.write(json.dumps(new_data))

# ======================================================================
# 這裡做一下 output_sheet 生成
# 對了 這裡是直接複製 3_generate_native_sheet 的部分，之後看要不要修整
# # TODO(we684123): 如上

# 為了防止 list 在最後倒數14個搜尋 out of range 用的


def get_in_area(n, a, max):
    # n = 6
    # a = 15
    # max = 20
    d = 0
    # max += 1
    if (n + a) > max:
        d = max - (n + a)
    return n + a + d


# 基本設定讀取
sheet_formats = rc["sheet_formats"][rc["output_sheet_format"]]
sync_area_time = rc["sync_area_time"]
sync_symbol = rc["sync_symbol"]
blank_symbol = rc["blank_symbol"]
line_feed_symbol = rc["line_feed_symbol"]

sheet = ""
index_st = ""
osl = len(o_s)
for i in range(osl):
    # i = 0
    # i = 9
    # i = 10

    if o_s[i]["type"] == "line_feed":
        sheet += line_feed_symbol
        continue

    if "index" in o_s[i]:
        if o_s[i]["index"] == index_st:
            continue
        index_st = o_s[i]["index"]
        _text_1 = str(sheet_formats[int(o_s[i]["keyboard"])])
        _text_2 = ""

        # 接下來在15個音符中搜尋哪個是同時按的
        # (這已被index標註，所以換句話說找接下來15個有沒有跟開頭的index一樣的)
        # ps 設15個是因為鍵盤最多15個，如果之後有增加數量要再改
        # TODO(we684123): 看看要不要把這個用base設定的鍵盤數動態生成，畢竟有8個的鍵盤
        for k in range(i, get_in_area(i, 15, osl)):
            # 如果有的話看看index一不一樣
            if "index" in o_s[k]:
                # 一樣就標起來，組合字串
                if o_s[k]["index"] == index_st:
                    # 按他base中的譜面格式設定生成要被組合的字串
                    _a = o_s[k]["keyboard"]
                    _text_2 += str(sheet_formats[_a]) + blank_symbol
                else:
                    break

        # 處理自動排序音符
        # _text_2 = 'B1 A4 C1 B2 '
        if rc["auto_sort_sync_note"]:
            _k1 = _text_2[:-1].split(blank_symbol)
            _k2 = sorted(_k1)
            _k3 = ""
            for _k in _k2:
                _k3 += _k + blank_symbol
            _text_3 = _k3[:-1]

        else:
            _text_3 = _text_2[:-1]
        # 組合完畢就用組合符號括起來(預設是 【 】)
        note = f"{sync_symbol[0]}{_text_3}{sync_symbol[1]}"
    else:
        # 沒有index的就直接按base要求組起來就好
        note = str(sheet_formats[int(o_s[i]["keyboard"])])
    sheet += note + blank_symbol
# ======================================================================
logger.info("generating output_sheet.")
output_sheet_path = (this_py_path / Path(rc["output_sheet_path"])).resolve()
_temp = output_sheet_path / rc["output_file_name"]
with _temp.open(mode="w", encoding="utf-8") as f:
    f.write(str(sheet))
