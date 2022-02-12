from pathlib import Path
import json
import sys
import os

import cv2
import numpy as np

from library import reverse_utilities as ru
from library import logger_generate
from library import input_then_exit as ite
from config import base

"""
☆    　  ∧＿∧
  　　 (´・ω・｀)
　　　 /つ¶つ¶
( ((　／￣￣￣￣＼
　    |) ○ ○ ○ (|
　  ／″ 　　ν.　　＼
  ／＿＿＿＿＿＿＿＿＼
    ＼＿＼＿_／＿／
"""

# ↓=====先處理設定檔=====↓
# ↓↓ 先把基本的東西訂好，並且從 base 中取基本的 config、logger
this_py_path = Path().absolute()
config = base.config()
logger = logger_generate.generate(
    base.logger_config(),
    name='reverse_sheet_log'
)
# ↓↓ 再從 config 取得預設參數
hsv = config['hsv']
binarization = config['binarization']
closing = config['closing']

# ↓↓ 處理被拖到這個程式的影片
if sys.argv[1] == '-f':
    # 如果是在 IDE(Hydrogen)下的話則自動覆蓋 sys.argv
    # ps'影片如果改了的話，請記得改下面的影片名稱
    sys.argv = [
        str(this_py_path / './test.py'),
        str(this_py_path / '能看見海的街道.mp4')
    ]
# sys.argv = [
#     str(this_py_path / './test.py'),
#     str(this_py_path / 'requirements.txt')
# ]
# print(sys.argv)
if len(sys.argv) == 0:
    # 代表是直接點執行檔
    logger.info((
        "🔎🈚Did not drag videon to here,"
        "📗so will use tmp effect_config_parameter"
    ))
    pass
if len(sys.argv) == 2:
    # 代表是拖影片檔到執行檔，此時需要驗證是否為影片
    aims_video_file = sys.argv[1]
    logger.debug(sys.argv)
    try:
        cap = cv2.VideoCapture(str(aims_video_file))
        # 如果是影片那應該可以直接跑 read 而不出錯
        for i in range(0, 2):
            ret, frame = cap.read()
        if not ret:
            logger.error(f'🎞️❌ "{str(aims_video_file)}" not a Video.')
            ite.input_then_exix()
        logger.info(f'🎞️✅ "{str(aims_video_file)}" is a video, and can use.')
    except Exception:
        logger.error(f'🎞️❌ "{str(aims_video_file)}" not a Video.')
        ite.input_then_exix()
if len(sys.argv) > 2:
    logger.error(
        "🈵 sorry, but you only can drag a video to here, can't too more😅")
    ite.input_then_exix()
# ↓↓之後從 effect_config 中找到調好的臨時設定檔，並從裡面取值覆蓋
effect_config_path = f"{this_py_path}/config/effect_config_parameter.json"
if Path(effect_config_path).exists():
    logger.info(f'📝✅ "{str(effect_config_path)}" exists.')
else:
    logger.
