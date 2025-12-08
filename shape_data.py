import json
from datetime import datetime

# time since last [motion, sound]

rows = []
shaped_rows = []

with open('data_present.almost_json', 'r') as raw:
    lines = raw.readlines()
    rows = [json.loads(line) for line in lines]

last_motion = None
last_sound = None

for row in rows:
    distance = row["Sensor_Ultra"] or 2.0
    motion = row["Sensor_PIR"] or 0.0
    sound = row["Sensor_Sound"] or 0.0
    unfucked_timestamp = datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S.%f")

    if last_motion is None or unfucked_timestamp < last_motion:
        last_motion = unfucked_timestamp

    if last_sound is None or unfucked_timestamp < last_sound:
        last_sound = unfucked_timestamp

    since_last_motion = unfucked_timestamp - last_motion
    since_last_sound = unfucked_timestamp - last_sound
    shaped_rows.append({'distance': distance,
                        'motion': motion,
                        'sound': sound,
                        'since_last_motion': str(since_last_motion),
                        'since_last_sound': str(since_last_sound)
                        })

with open('data_present.json', 'w') as shaped:
    shaped.write(json.dumps(shaped_rows, indent=4))

