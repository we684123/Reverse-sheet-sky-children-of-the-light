from pathlib import Path
import json

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

sounds[0].play()
