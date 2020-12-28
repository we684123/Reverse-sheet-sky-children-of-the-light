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
_temp = output_sheet_path / './sort_sheet.json'

with open(_temp, mode='r', encoding='utf-8') as f:
    _sort_sheet = f.read()

sort_sheet = json.loads(_sort_sheet)

# 基本設定讀取
sheet_formats = rc['sheet_formats'][rc['output_sheet_format']]
sync_area_time = rc['sync_area_time']
sync_symbol = rc['sync_symbol']
blank_symbol = rc['blank_symbol']

original_sheet = sort_sheet['original_sheet']


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
        for k in range(i, get_in_area(i, 15, osl)):
            if k == (osl - 1):  # 防止 out of range
                break
            if 'index' in original_sheet[k]:
                if original_sheet[k]['index'] == index_st:
                    _a = original_sheet[k]['keyboard']
                    _text_2 += str(sheet_formats[_a]) + blank_symbol
                else:
                    break
        note = f"{sync_symbol[0]}{_text_2[:-1]}{sync_symbol[1]}"
    else:
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
    f.write(json.dumps(original_sheet))

logger.info('save data done.')
logger.info('Please proceed to the next action.')
input('input any key to exit. 輸入任意值離開.')


#
