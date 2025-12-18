import json
from datetime import datetime
from pathlib import Path
import statistics


def shape_json(rows):
    shaped_rows = []

    last_motion = None
    last_sound = None

    for row in rows:
        distance = row["Sensor_Ultra"] or 2.0
        motion = row["Sensor_PIR"] or 0.0
        sound = row["Sensor_Sound"] or 0.0
        timestamp = datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S.%f")

        if last_motion is None or motion:
            last_motion = timestamp

        if last_sound is None or sound:
            last_sound = timestamp

        since_last_motion = (timestamp - last_motion).total_seconds()
        since_last_sound = (timestamp - last_sound).total_seconds()
        shaped_rows.append({'distance': float(distance),
                            'motion': float(motion),
                            'sound': float(sound),
                            'since_last_motion': since_last_motion,
                            'since_last_sound': since_last_sound
                            })
    return shaped_rows


def windowify(rows, window_size):
    num_windows = len(rows) - window_size + 1
    window_data = []

    for w in range(num_windows):
        window = rows[w:w+window_size]
        avg_dist = sum([row["distance"] for row in window]) / window_size
        stdev_dist = statistics.stdev([row["distance"] for row in window])
        num_motion = len([1 for row in window if row["motion"]])
        num_sound = len([1 for row in window if row["sound"]])
        motion_min = min([row["since_last_motion"] for row in window])
        sound_min = min([row["since_last_sound"] for row in window])

        window_data.append({
            'avg_distance': avg_dist,
            'stdev_distance': stdev_dist,
            'num_motion': num_motion,
            'num_sound': num_sound,
            'motion_min': motion_min,
            'sound_min': sound_min
        })

    return window_data


def shape_all():
    for path in Path("training_data").rglob("*.almost_json"):
        if path.is_file():
            input = str(path)
            output = input.replace("almost_json", "json")
            print(f"shaping: {input} -> {output}")

            with open(input, 'r') as raw:
                lines = raw.readlines()
                rows = [json.loads(line) for line in lines]
                windows = windowify(shape_json(rows), 30)

            with open(output, 'w') as processed:
                processed.write(json.dumps(windows, indent=4))
