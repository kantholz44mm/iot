from datetime import datetime, timedelta

def generate_not_present_data(filename, num_rows, interval):
    start_timestamp = datetime.now()
    with open(filename, "w") as file:
        for i in range(num_rows):
            timestamp = str(start_timestamp + i * interval)
            file.write(f'{{"Sensor_PIR":0,"Sensor_Ultra":"2.0","Sensor_Sound":0,"Time":"{timestamp}"}}\n')

generate_not_present_data("training_data/not_present/data_not_present_v2.almost_json", 10000, timedelta(seconds=0.5))