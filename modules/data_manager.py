import csv
import os
from datetime import datetime
from modules.config import DATA_FILE_PATH

def save_data(people_count, car_count):
    file_exists = os.path.isfile(DATA_FILE_PATH)
    with open(DATA_FILE_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Personas', 'Autos'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), people_count, car_count])
