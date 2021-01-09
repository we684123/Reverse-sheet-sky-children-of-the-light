from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())
# ====基礎準備完畢====


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
# ===== 以上像素點分析 =====

_temp = output_sheet_path / './native_sheet.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _analysis_from_video = f.read()




track = 9
ironman = np.linspace(0, len(kb_list[track]), len(kb_list[track]))
fig = plt.figure()  # 定義一個圖像窗口
plt.plot(ironman[0:1000], kb_list[track][0:1000], '.')
plt.plot(ironman[180:220], kb_list[track][180:220], '.')
plt.plot(ironman[180:280], kb_list[track][180:280], '.')
plt.plot(ironman[240:280], kb_list[track][240:280], '.')
plt.plot(ironman[240:260], kb_list[track][240:260], '.')
plt.plot(ironman[247:260], kb_list[track][247:260], '.')
plt.plot(ironman[280:400], kb_list[track][280:400], '.')
plt.plot(ironman[:500], kb_list[track][:500], '.')
plt.plot(ironman[500:1000], kb_list[track][500:1000], '.')
plt.plot(ironman[1000:1500], kb_list[track][1000:1500], '.')
plt.plot(ironman[1350:1400], kb_list[track][1350:1400], '.')
plt.plot(ironman[1500:2000], kb_list[track][1500:2000], '.')
plt.plot(ironman[2000:2500], kb_list[track][2000:2500], '.')
plt.plot(ironman[:], kb_list[track][:], '.')


#
