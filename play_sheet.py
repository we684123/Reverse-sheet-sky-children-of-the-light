from pathlib import Path
import json
import time

import pygame

from library import reverse_utilities as ru
from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())


sounds = ru.get_sounds()
# sounds[0].play()

# 讀取譜面
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './native_sheet.json'
with open(_temp, mode='r', encoding='utf-8') as f:
    _original_sheet = f.read()
original_sheet = json.loads(_original_sheet)['original_sheet']


# 先生出時間差
for j in range(0, len(original_sheet)):
    if j == len(original_sheet) - 1:
        original_sheet[j]['time_area'] = 0
        break
    original_sheet[j]['time_area'] =\
        original_sheet[j + 1]['time'] - original_sheet[j]['time']

# 來播放
for note in original_sheet:
    # k = 0
    sleep_time = note['time_area']
    sound_number = note['keyboard']
    # print(f"channels = {pygame.mixer.get_num_channels()}")

    points_channel = sounds[sound_number].play()
    logger.debug(f"find_channel = {pygame.mixer.find_channel()}")
    logger.debug(f"points_channel = {points_channel}")
    logger.debug(sound_number + 1)
    time.sleep(sleep_time)
#
