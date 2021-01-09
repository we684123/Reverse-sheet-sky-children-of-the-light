from pathlib import Path
import json

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())

# 從檔案獲取上一階段資料
logger.info('generated  sheet ing...')
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './native_sheet.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _data = f.read()

data = json.loads(_data)
fps = data['fps']

# 基本設定讀取
sheet_formats = rc['sheet_formats'][rc['output_sheet_format']]
sync_area_time = rc['sync_area_time']
sync_symbol = rc['sync_symbol']
blank_symbol = rc['blank_symbol']

original_sheet = data['original_sheet']


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
original_sheet

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
            if k == (osl - 1):  # 防止 out of range
                break
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

logger.info('generated  sheet done.')

logger.info('now to save data...')

# 先存 output_sheet
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / rc['output_file_name']
with open(_temp, mode='w', encoding='utf-8') as f:
    f.write(str(sheet))

# 再存 original_sheet
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / 'original_sheet.json'
with open(_temp, mode='w', encoding='utf-8') as f:
    new_data = {
        "original_sheet": original_sheet,
        "frame_end": data['frame_end'],
        "fps": data['fps'],
        "duration": data['duration'],
        "minute": data['minute'],
        "seconds": data['seconds'],
        "st_specify_count": data['st_specify_count'],
        "ed_specify_count": data['ed_specify_count'],
    }
    f.write(json.dumps(new_data))

logger.info('save data done.')
logger.info('Please proceed to the next action.')
input('input any key to exit. 輸入任意值離開.')


#
