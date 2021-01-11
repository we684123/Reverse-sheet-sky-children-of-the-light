from pathlib import Path

import cv2

from library import reverse_utilities as ru
from library import logger_generate
from config import base
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())


video_path = Path(rc['video_path'])  # "./sky.mkv"
if not video_path.exists():
    logger.warning('video_path is not exist!')
    exit()
cap = cv2.VideoCapture(str(video_path))

frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
fps = int(cap.get(cv2.CAP_PROP_FPS))
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

duration = count / fps
minute = int(duration / 60)
seconds = int(duration % 60)

print(f'frame_count = {frame_count}')
print(f'fps = {fps}')
print(f'count= {count}')
print(f'duration= {duration}')
print(f'minute= {minute}')
print(f'seconds= {seconds}')

specify_minute = input('plz input specify "minute" = ')
specify_seconds = input('plz input specify "seconds" = ')

specify_count = int(specify_minute) * 60 * fps + int(specify_seconds) * fps
for i in range(0, specify_count):
    ret, frame = cap.read()
mask, res = ru.get_keyboard_by_hsv(frame)

_temp = Path(rc['aims_folder_path']) / Path(rc['output_sheet_path'])
temp = _temp / "boundary.png"

cv2.imwrite(str(temp), mask)
print(temp)
print('===已生成 done.===')
input('input any key to exit. 輸入任意值離開.')
