import cv2
import time
import os
import datetime
import threading
from modules.config import ROJO, VERDE, VIDEO_PATH
from modules.detectors import Detector
from modules.tracker import Tracker
from modules.data_manager import save_data
from modules.notifications import send_speeding_alert

VIOLATION_DIR = "infracciones"
if not os.path.exists(VIOLATION_DIR):
    os.makedirs(VIOLATION_DIR)

def main():
    try:
        detector = Detector()
        tracker = Tracker()
    except IOError as e:
        print(e)
        return

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"Error opening video: {VIDEO_PATH}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 30

    traffic_light_state = VERDE
    state_start_time = time.time()
    last_person_check_time = time.time()
    last_save_time = time.time()
    
    last_printed_state = ""
    last_people_count = 0
    last_car_count = 0
    last_violation_time = 0

    # Set to keep track of vehicles that have already been reported for speeding
    reported_speeding_ids = set()
    last_email_sent_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        people_rects = detector.detect_people(frame)
        car_rects = detector.detect_cars(frame)
        
        people_count = len(people_rects)
        car_count = len(car_rects)
        
        # Track cars
        video_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        objects, speeds = tracker.update(car_rects, video_timestamp)
        
        current_time = time.time()

        for (object_id, centroid) in objects.items():
            speed = speeds.get(object_id, 0)
            
            # Check for speeding (> 45 km/h) and send alert if not already reported
            if speed > 45 and object_id not in reported_speeding_ids:
                if current_time - last_email_sent_time >= 4:
                    print(f"¡ALERTA! Vehículo {object_id} excediendo límite de velocidad ({speed:.1f} km/h)")
                    # Send email in a separate thread to avoid freezing the video
                    threading.Thread(target=send_speeding_alert, args=(object_id, speed)).start()
                    reported_speeding_ids.add(object_id)
                    last_email_sent_time = current_time
            
            text = f"ID {object_id}: {speed:.1f} km/h"
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        
        if current_time - last_save_time >= 1.0:
            save_data(people_count, car_count)
            last_save_time = current_time

        if traffic_light_state == ROJO and car_count > 0:
            if current_time - last_violation_time >= 2.0:
                print("Un automovil se ha cruzado en rojo")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(VIOLATION_DIR, f"violation_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Screenshot guardado en {filename}")
                last_violation_time = current_time

        # Traffic light logic: 10 seconds per color
        elapsed_time = current_time - state_start_time
        remaining_time = 10 - int(elapsed_time)
        
        if remaining_time <= 0:
            if traffic_light_state == VERDE:
                traffic_light_state = ROJO
            else:
                traffic_light_state = VERDE
            state_start_time = current_time
            remaining_time = 10

        if traffic_light_state == ROJO:
            if last_printed_state != ROJO or people_count != last_people_count or car_count != last_car_count or remaining_time % 5 == 0:
                print(f"State: {traffic_light_state}, Time Left: {remaining_time}s, People: {people_count}, Cars: {car_count}")
                last_printed_state = ROJO
                last_people_count = people_count
                last_car_count = car_count
        else:
            if last_printed_state != VERDE or people_count != last_people_count or car_count != last_car_count or remaining_time % 5 == 0:
                 print(f"State: {traffic_light_state}, Time Left: {remaining_time}s, People: {people_count}, Cars: {car_count}")
                 last_printed_state = VERDE
                 last_people_count = people_count
                 last_car_count = car_count

        cv2.imshow("Smart Traffic Light", frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
