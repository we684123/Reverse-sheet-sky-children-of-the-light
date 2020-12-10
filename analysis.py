import numpy as np
import json

import matplotlib.pyplot as plt

with open('./frame_keyboards.txt', mode='r', encoding='utf-8') as f:
    frame_keyboards = f.read()

frame_keyboards = json.loads(frame_keyboards)

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
        pass

for i in frame_keyboards:
    for j in range(0, len(i)):
        kb_list[j].append(max_pixel_len - i[j][0])

len(kb_list[0])
len(kb_list[14])


ironman = np.linspace(0, len(kb_list[0]), len(kb_list[0]))
fig = plt.figure()  # 定義一個圖像窗口
plt.plot(ironman[0:500], kb_list[0][0:500], '.')
plt.plot(ironman[500:1000], kb_list[0][500:1000], '.')
plt.plot(ironman[1000:1500], kb_list[0][1000:1500], '.')
plt.plot(ironman[1350:1400], kb_list[0][1350:1400], '.')
plt.plot(ironman[0:500], kb_list[0][0:500], '.')
plt.plot(ironman[0:500], kb_list[0][0:500], '.')


# 狀態器初始化
refractory_time = 35  # 單位 偵數
temp_state_list = []  # 狀態器陣列
for i in range(0, len(frame_keyboards[0])):
    temp_state = {
        "st_frame": 0,
        "refractory": False
    }
    temp_state_list.append(temp_state)


# 譜面生成
#
sheet = []
for m in range(0,len(frame_keyboards)):
    frame_keyboards[m]



#