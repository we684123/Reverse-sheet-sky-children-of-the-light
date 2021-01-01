from pathlib import Path
import json

import matplotlib.pyplot as plt
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
cool_down_frame = round((cool_down_time / 1000) / (1 / fps))  # 冷卻時間(單位 偵數

analysis_from_video = json.loads(_analysis_from_video)
frame_keyboards = json.loads(analysis_from_video['notes'])

len(frame_keyboards)
len(frame_keyboards[0])
len(frame_keyboards[0][0])
frame_keyboards[0]

# 先來定義一下 kb_list 格式
kb_list = []
for i in range(0, len(frame_keyboards[0])):
    # print(frame_keyboards[0][i])
    kb_list.append([])

# 再來要找區域的像素數量總和
max_pixel_len = 0
for i in range(0, len(frame_keyboards[0])):
    # print(frame_keyboards[0][i])
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

len(kb_list)
len(kb_list[0])
len(kb_list[14])

track = 7
ironman = np.linspace(0, len(kb_list[track]), len(kb_list[track]))
fig = plt.figure()  # 定義一個圖像窗口
plt.plot(ironman[0:1000], kb_list[track][0:1000], '.')
plt.plot(ironman[180:220], kb_list[track][180:220], '.')
plt.plot(ironman[180:280], kb_list[track][180:280], '.')
plt.plot(ironman[240:280], kb_list[track][240:280], '.')
plt.plot(ironman[240:260], kb_list[track][240:260], '.')
plt.plot(ironman[247:260], kb_list[track][247:260], '.')
plt.plot(ironman[:500], kb_list[track][:500], '.')
plt.plot(ironman[500:1000], kb_list[track][500:1000], '.')
plt.plot(ironman[1000:1500], kb_list[track][1000:1500], '.')
plt.plot(ironman[1350:1400], kb_list[track][1350:1400], '.')
plt.plot(ironman[1500:2000], kb_list[track][1500:2000], '.')
plt.plot(ironman[2000:2500], kb_list[track][2000:2500], '.')
plt.plot(ironman[:], kb_list[track][:], '.')


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
    # print(mean)
    trigger_valve.append(mean / 2)

trigger_valve[track]

# 譜面生成
len(frame_keyboards)
len(kb_list)
sheet = [].copy()
for n in range(0, len(kb_list)):
    # n = 1
    for m in range(0, len(frame_keyboards)):
        # m = 0
        # print('+')
        track = n
        after_time = (m - temp_state_list[track]['st_frame'])
        refractory_timeout = after_time > cool_down_frame
        trigger = kb_list[track][m] < trigger_valve[n]
        if trigger and refractory_timeout:
            # print('.')
            temp_state_list[track]['st_frame'] = m
            temp_state_list[track]['refractory'] = True
            sheet.append({"frame": m, "keyboard": track})

sheet
len(sheet)
sheet[0]

sheet2 = sheet
sheet2
sheet3 = sheet
sheet3


sort_sheet = sorted(sheet, key=lambda s: s['frame'])
sort_sheet


[1, 2, 3] + [4, 5, 6]
t_sheet = sheet2 + sheet3

test_reverse = {
    "name": "test_reverse",
    "author": "Unknown",
    "transcribedBy": "Unknown",
    "isComposed": True,
    "bpm": 240,
    "bitsPerPage": 16,
    "pitchLevel": 0,
    "isEncrypted": False,
    "songNotes": []
}
test_reverse['songNotes'].append()


#
