from pathlib import Path
import json

import numpy as np

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())
# ===== 環境OK =====

logger.info("Loading analysis_from_video.json ...")
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './analysis_from_video.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _analysis_from_video = f.read()

analysis_from_video = json.loads(_analysis_from_video)
frame_keyboards = json.loads(analysis_from_video['notes'])
fps = analysis_from_video['fps']
cool_down_time = rc['cool_down_time']  # 冷卻時間(單位 ms)
cool_down_frame = round((cool_down_time / 1000) / (1 / fps))  # 冷卻時間(單位 偵數)
logger.info("Loaded analysis_from_video.json.")

logger.info('generating original sheet...')
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
    trigger_valve.append(mean / rc['trigger_valve_parameter'])


# 譜面生成
sheet = [].copy()
for track in range(0, len(kb_list)):
    # track = 1
    for m in range(0, len(frame_keyboards)):
        # m = 0
        # logger.debug('+')
        after_time = (m - temp_state_list[track]['st_frame'])
        refractory_timeout = after_time > cool_down_frame
        trigger = kb_list[track][m] < trigger_valve[track]
        if trigger and refractory_timeout:
            # logger.debug('.')
            temp_state_list[track]['st_frame'] = m
            temp_state_list[track]['refractory'] = True
            sheet.append({"type": "note", "frame": m, "keyboard": track})

sort_sheet = sorted(sheet, key=lambda s: s['frame'])
sort_sheet

# 加個正確時間(frame -> time)
# 順便給個編號
for j in range(0, len(sort_sheet)):
    sort_sheet[j]['time'] = sort_sheet[j]['frame'] / fps
    sort_sheet[j]['note'] = j
analysis_from_video['original_sheet'] = sort_sheet
logger.info('generated original sheet done.')

del analysis_from_video['notes']

analysis_from_video['trigger_valve'] = trigger_valve

# ============================================================
# 經評估後決定把原本負責 index "4_generate_sheet" 內容搬移過來

logger.info('generating native sheet...')

original_sheet = analysis_from_video['original_sheet']
# 基本設定讀取
sheet_formats = rc['sheet_formats'][rc['output_sheet_format']]
sync_area_time = rc['sync_area_time']
sync_symbol = rc['sync_symbol']
blank_symbol = rc['blank_symbol']


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


# 開始將同時按的標註起來
original_sheet_len = len(original_sheet)
osl = original_sheet_len
index = 0
for i in range(0, osl):
    # i = 0
    for j in range(i, get_in_area(i, 15, osl)):
        # j = 0
        if j == (osl - 1):  # 防止 out of range
            break
        interval = original_sheet[j + 1]['time'] - original_sheet[i]['time']
        if interval * 1000 > sync_area_time:  # 高於差值的就直接下一個
            break
        if 'index' in original_sheet[j]:  # 有 index 帶被被分類過了，下一個
            continue
        else:
            if 'index' in original_sheet[i]:  # 初始 index 綁定
                original_sheet[j + 1]['index'] = original_sheet[i]['index']
            else:  # 被初始 index 綁定
                original_sheet[i]['index'] = index
                original_sheet[j + 1]['index'] = index
                index += 1

# 按照 index(同時) 分組
sheet = ""
index_st = ''
for i in range(0, osl):
    # i = 0
    # i = 9
    # i = 10

    if 'index' in original_sheet[i]:
        if original_sheet[i]['index'] == index_st:
            continue
        index_st = original_sheet[i]['index']
        _text_1 = str(sheet_formats[int(original_sheet[i]['keyboard'])])
        _text_2 = ""

        # 接下來在15個音符中搜尋哪個是同時按的
        # (這已被index標註，所以換句話說找接下來15個有沒有跟開頭的index一樣的)
        # ps 設15個是因為鍵盤最多15個，如果之後有增加數量要再改
        # TODO: 看看要不要把這個用base設定的鍵盤數動態生成，畢竟有8個的鍵盤
        for k in range(i, get_in_area(i, 15, osl)):
            # 如果有的話看看index一不一樣
            if 'index' in original_sheet[k]:
                # 一樣就標起來，組合字串
                if original_sheet[k]['index'] == index_st:
                    # 按他base中的譜面格式設定生成要被組合的字串
                    _a = original_sheet[k]['keyboard']
                    _text_2 += str(sheet_formats[_a]) + blank_symbol
                else:
                    break
        # 組合完畢就用組合符號括起來(預設是 【 】)
        note = f"{sync_symbol[0]}{_text_2[:-1]}{sync_symbol[1]}"
    else:
        # 沒有index的就直接按base要求組起來就好
        note = str(sheet_formats[int(original_sheet[i]['keyboard'])])
    sheet += note + blank_symbol

logger.info('generated native sheet done.')
# ============================================================

# 先存 output_sheet
logger.info('generating output_sheet.')
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / "penultimate_sheet.txt"
with open(_temp, mode='w', encoding='utf-8') as f:
    f.write(str(sheet))
logger.info('generated output_sheet done.')

# 再存 original_sheet
logger.info('generating native_sheet.')
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / 'native_sheet.json'
_afv = analysis_from_video
with open(_temp, mode='w', encoding='utf-8') as f:
    new_data = {
        "original_sheet": original_sheet,
        "frame_end": _afv['frame_end'],
        "fps": _afv['fps'],
        "duration": _afv['duration'],
        "minute": _afv['minute'],
        "seconds": _afv['seconds'],
        "st_specify_count": _afv['st_specify_count'],
        "ed_specify_count": _afv['ed_specify_count'],
        "trigger_valve": _afv['trigger_valve'],
        "cool_down_frame": cool_down_frame,
    }
    f.write(json.dumps(new_data))
logger.info('generated native_sheet done.')

logger.info('save data done.')
logger.info('Please proceed to the next action.')
input('input any key to exit. 輸入任意值離開.')


#
