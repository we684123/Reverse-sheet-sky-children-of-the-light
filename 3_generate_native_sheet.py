from pathlib import Path
import json

import numpy as np

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())

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
cool_down_frame = round((cool_down_time/1000) / (1 / fps))  # 冷卻時間(單位 偵數)

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
        refractory_timeout = after_time > cool_down_frame
        trigger = kb_list[track][m] < trigger_valve[n]
        if trigger and refractory_timeout:
            # logger.debug('.')
            temp_state_list[track]['st_frame'] = m
            temp_state_list[track]['refractory'] = True
            sheet.append({"frame": m, "keyboard": track})

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

logger.info('now to save data...')
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './sort_sheet.json'
with open(_temp, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(analysis_from_video))
logger.info('save data done.')
logger.info('Please proceed to the next action.')
input('input any key to exit. 輸入任意值離開.')
