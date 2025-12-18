import api
from pathlib import Path
from datetime import datetime, timedelta

if input("Train model? [y/n]").lower() in ["y", "yes"]:
    api.train_model(True, True)

api.load_model()


data_example_timestamp = datetime.now()
data_example_present = {"Sensor_PIR": 0, "Sensor_Ultra": "0.40411913989632464", "Sensor_Sound": 0, "Time": str(data_example_timestamp)}

for i in range(30):
    data = data_example_present.copy()
    data["Time"] = str(data_example_timestamp + i * timedelta(seconds=0.5))
    api.push_data(data)

print(api.estimate_current_state())
print(api.detect_anomalies(0.7, timedelta(days=3)))
