import json
import uuid

# Input file
input_file = "native_sheet.json"

# Output file
output_file = "converted_song.txt"

# Read the original JSON from file
with open(input_file, 'r') as f:
    original_json = f.read()

# Parse the JSON
data = json.loads(original_json)

# Extract the original_sheet
original_sheet = data["original_sheet"]

# Calculate BPM based on original file: 60 * fps / frame_diff_per_beat
# From the data, initial frame diff between indices is 11 frames
frame_diff_per_beat = 11
fps = data["fps"]
bpm = round(60 * fps / frame_diff_per_beat)

# Beat length in ms
beat_ms = 60 / bpm * 1000

# Convert notes to songNotes format
songNotes = []
column_notes = {}  # Dict to group notes by column index

for note in original_sheet:
    time_ms = int(note["time"] * 1000)
    key = f"1Key{note['keyboard']}"
    songNotes.append({"key": key, "time": time_ms})
    
    # Calculate column index
    column_index = round(time_ms / beat_ms)
    if column_index not in column_notes:
        column_notes[column_index] = []
    column_notes[column_index].append([note["keyboard"], "1"])

# Find the maximum column index
if column_notes:
    max_column = max(column_notes.keys())
else:
    max_column = 0

# Create columns list
columns = []
for i in range(max_column + 1):
    if i in column_notes:
        columns.append([0, column_notes[i]])
    else:
        columns.append([0, []])

# Generate a random ID
song_id = str(uuid.uuid4())

# Create the full target object
target_object = {
    "name": "Converted Song",
    "type": "composed",
    "bpm": bpm,
    "pitch": "C",
    "version": 3,
    "folderId": None,
    "data": {
        "isComposed": True,
        "isComposedVersion": True,
        "appName": "Sky"
    },
    "reverb": False,
    "breakpoints": [0],
    "instruments": [
        {
            "name": "Piano",
            "volume": 100,
            "pitch": "",
            "visible": True,
            "icon": "circle",
            "alias": "",
            "muted": False,
            "reverbOverride": None
        }
    ],
    "columns": columns,
    "id": song_id,
    "pitchLevel": 0,
    "isComposed": True,
    "bitsPerPage": 16,
    "isEncrypted": False,
    "songNotes": songNotes
}

# Output the converted object as JSON to file
with open(output_file, 'w') as f:
    json.dump([target_object], f, indent=4)

print(f"Conversion complete. Output saved to {output_file}. Calculated BPM: {bpm}")
