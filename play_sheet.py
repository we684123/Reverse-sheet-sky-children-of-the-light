from pathlib import Path
import json
import time

import pygame

from library import logger_generate
from config import base

reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generator(base.logger_config())

# load 聲音路徑
note_songs_path = Path('./note_songs')
sounds_path = []
for i in range(0, 15):
    sounds_path.append(note_songs_path / f"{i}.ogg")

# 載入聲音
pygame.mixer.init()
sounds = []
for p in sounds_path:
    sounds.append(pygame.mixer.Sound(p))

# sounds[0].play()

# 讀取譜面
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path /
                     Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './original_sheet.json'
with open(_temp, mode='r', encoding='utf-8') as f:
    _original_sheet = f.read()
original_sheet = json.loads(_original_sheet)


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
    sounds[sound_number].play()
    time.sleep(sleep_time)
#
