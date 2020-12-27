import json

import matplotlib.pyplot as plt

import numpy as np


with open('./output/analysis_from_video.txt', mode='r', encoding='utf-8') as f:
    _frame_keyboards = f.read()

frame_keyboards = json.loads(json.loads(_frame_keyboards)['notes'])

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

track = 4
ironman = np.linspace(0, len(kb_list[track]), len(kb_list[track]))
fig = plt.figure()  # 定義一個圖像窗口
plt.plot(ironman[0:1000], kb_list[track][0:1000], '.')
plt.plot(ironman[200:230], kb_list[track][200:230], '.')
plt.plot(ironman[500:1000], kb_list[track][500:1000], '.')
plt.plot(ironman[1000:1500], kb_list[track][1000:1500], '.')
plt.plot(ironman[1350:1400], kb_list[track][1350:1400], '.')
plt.plot(ironman[1500:2000], kb_list[track][1500:2000], '.')
plt.plot(ironman[2000:2500], kb_list[track][2000:2500], '.')
plt.plot(ironman[:], kb_list[track][:], '.')


# 狀態器初始化
refractory_time = 35  # 單位 偵數
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
    trigger_valve.append(mean/2)


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
        refractory_timeout = after_time > refractory_time
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
