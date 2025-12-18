import matplotlib.pyplot as plt
import csv
from datetime import datetime
import matplotlib.dates as mdates
import os
from modules.config import DATA_FILE_PATH

def generate_plots():
    times = []
    people = []
    cars = []

    file_path = DATA_FILE_PATH
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dt = datetime.strptime(row['Timestamp'], "%Y-%m-%d %H:%M:%S")
                    times.append(dt)
                    people.append(int(row['Personas']))
                    cars.append(int(row['Autos']))
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if not times:
        print("No data to plot.")
        return

    plt.figure(figsize=(12, 6))
    
    plt.plot(times, cars, label='Cars', color='blue', marker='o', linestyle='-')
    plt.plot(times, people, label='People', color='green', marker='x', linestyle='--')

    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.title('Traffic Detection Over Time')
    plt.legend()
    plt.grid(True)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    
    output_file = os.path.join('data', 'grafico_trafico.png')
    plt.savefig(output_file)
    print(f"Plot saved to '{output_file}'")
    
    plt.show()

if __name__ == "__main__":
    generate_plots()
