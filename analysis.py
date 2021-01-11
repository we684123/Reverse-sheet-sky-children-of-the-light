from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())
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

# =====讀譜用以畫線=====
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './native_sheet.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _native_sheet = f.read()
native_sheet = json.loads(_native_sheet)
original_sheet = native_sheet['original_sheet']
trigger_valve = native_sheet['trigger_valve']
len_track = int(rc['keyboards_X_format']) * int(rc['keyboards_y_format'])
# ===== 準備完畢 =====


def generate_pixel_force():
    # 因為 np.shape(kb_list) 結果會一樣，故直接用 0 取代
    pixel_force = np.linspace(0, len(kb_list[0]), len(kb_list[0]))
    return pixel_force


def generate_note_st_ed():
    # 生出起始觸發時間 + 冷卻時間
    note_st_ed_list = []
    for track in range(0, len_track):
        def is_note_from_track(x):
            if x['keyboard'] == track and x['type'] == 'note':
                return x

        rt = filter(is_note_from_track, original_sheet.copy())
        rt = list(rt)
        note_st_ed = np.zeros(len(kb_list[track]))
        for _i in rt:
            _index = _i['frame']
            _cd = _index + cool_down_frame
            note_st_ed[_index:_cd] = trigger_valve[track]
        note_st_ed_list.append(note_st_ed)
    return note_st_ed_list


# horizon_range = [280, 400]
# now_frame = 300
# index_height = 800
def check_graph(pixel_force, kb_list, note_st_ed,
                track, horizon_range, now_frame, index_height):
    hr = horizon_range

    now_index = np.zeros(len(kb_list[track]))
    now_index[now_frame] = index_height

    fig = plt.figure(f'track{track}')
    plt.plot(
        pixel_force[hr[0]:hr[1]], kb_list[track][hr[0]:hr[1]],
        color='#48D1CC', linestyle='solid', marker='.'
    )
    plt.plot(
        pixel_force[hr[0]:hr[1]], note_st_ed[track][hr[0]:hr[1]],
        color='orange', linestyle='solid', marker='|'
    )
    plt.plot(
        pixel_force[hr[0]:hr[1]], now_index[hr[0]:hr[1]],
        color='red', linestyle='solid', marker='v'
    )
    fig.show()
    # input('1')


# len(pixel_force)
# len(kb_list[0])
# len(note_st_ed_list)
if __name__ == '__main__':
    index_height = 800
    pixel_force = generate_pixel_force()
    note_st_ed_list = generate_note_st_ed()
    now_frame = 600

    horizon_range = [280, 400]
    track = 9
    image = check_graph(pixel_force, kb_list, note_st_ed_list,
                        track, horizon_range, now_frame, index_height)
    track = 3
    image = check_graph(pixel_force, kb_list, note_st_ed_list,
                        track, horizon_range, now_frame, index_height)

#
