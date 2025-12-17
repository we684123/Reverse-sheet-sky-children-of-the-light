from pathlib import Path
import json
import time
import pyautogui
import sys
from collections import defaultdict

# Your existing imports
import pygame
from library import reverse_utilities as ru
from library import logger_generate
from config import base

# Your existing setup
reverse_config = base.reverse_config()
rc = reverse_config
logger = logger_generate.generate(base.logger_config())

# Load native_sheet.json (your existing code)
aims_folder_path = Path(rc['aims_folder_path'])
output_sheet_path = (aims_folder_path / Path(rc['output_sheet_path'])).resolve()
_temp = output_sheet_path / './native_sheet.json'
with open(_temp, mode='r', encoding='utf-8') as f:
    _original_sheet = f.read()
original_sheet = json.loads(_original_sheet)['original_sheet']

# PyAutoGUI setup
pyautogui.FAILSAFE = True  # Move mouse to corner to emergency stop
pyautogui.PAUSE = 0       # No delay between actions

# Click positions (adjust these if your game window is different)
click_positions = {
    '.': (1517, 500),  # Safe/blank position
    'Q': (591, 587),
    'W': (693, 588),
    'E': (799, 593),
    'R': (901, 588),
    'T': (1000, 593),
    'A': (588, 695),
    'S': (686, 698),
    'D': (796, 696),
    'F': (900, 691),
    'G': (1000, 696),
    'Z': (582, 796),
    'X': (687, 805),
    'C': (803, 800),
    'V': (896, 797),
    'B': (1002, 798)
}

# PERFECT mapping: keyboard 0=Q, 1=W, 2=E, 3=R, 4=T, 5=A, 6=S, 7=D, etc.
def get_key_from_keyboard_idx(idx):
    mapping = {
        0: 'Q', 1: 'W', 2: 'E', 3: 'R', 4: 'T',
        5: 'A', 6: 'S', 7: 'D', 8: 'F', 9: 'G',
        10: 'Z', 11: 'X', 12: 'C', 13: 'V', 14: 'B'
    }
    return mapping.get(idx, '.')

# FRAME-BASED GROUPING (PERFECT chord detection)
groups = defaultdict(list)
for note in original_sheet:
    if note['type'] == 'note':
        frame_key = note['frame']  # EXACT frame = perfect simultaneous notes
        key_idx = note['keyboard']
        key_letter = get_key_from_keyboard_idx(key_idx)
        groups[frame_key].append(key_letter)

# Convert to time-sorted groups (calculate time from first note in frame)
time_groups = []
for frame, keys in sorted(groups.items()):
    # Get time from first note in this frame
    frame_notes = [n for n in original_sheet if n.get('frame') == frame and n['type'] == 'note']
    if frame_notes:
        time_pos = frame_notes[0]['time']
        time_groups.append((time_pos, keys))

print(f"Loaded {len(original_sheet)} notes, {len(time_groups)} frame-groups")
print("First 5 frame-groups:")
for i, (t, keys) in enumerate(time_groups[:5]):
    print(f"  Frame {frame}: {t:.3f}s: {keys}")

# 3-Second Countdown
print("\nStarting screen clicks in...")
for i in range(3, 0, -1):
    sys.stdout.write(f"\r{i} seconds...".ljust(20))
    sys.stdout.flush()
    time.sleep(1)
print("\rStarting NOW!      \n")

# PERFECT timing playback using frame-based grouping
prev_time = 0
try:
    for time_pos, keys in time_groups:
        # Exact timing between frames
        sleep_time = time_pos - prev_time
        if sleep_time > 0:
            time.sleep(max(0.01, sleep_time))
        
        # ULTRA-FAST chord clicks (<10ms total) - ALL notes in same frame
        print(f"[{time_pos:.3f}] Frame chord: {keys}")
        for key in keys:
            x, y = click_positions.get(key, click_positions['.'])
            pyautogui.moveTo(x, y, duration=0)  # Instant move
            pyautogui.click(duration=0)         # Instant click
        
        # Safe reset position after chord
        pyautogui.click(1517, 500)
        prev_time = time_pos
        
except KeyboardInterrupt:
    print("\n\nStopped by user (Ctrl+C)!")
except Exception as e:
    print(f"\nError: {e}")

print("Playback complete!")
