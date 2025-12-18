import math
import time
import cv2
import numpy as np

class Tracker:
    def __init__(self, max_disappeared=50, max_distance=50, pixels_per_meter=30):
        self.next_object_id = 0
        self.objects = {}  # ID -> centroid (x, y)
        self.disappeared = {}  # ID -> number of frames disappeared
        self.positions = {} # ID -> list of (timestamp, centroid)
        self.speeds = {} # ID -> current speed in km/h
        
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.pixels_per_meter = pixels_per_meter

    def register(self, centroid, timestamp):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.positions[self.next_object_id] = [(timestamp, centroid)]
        self.speeds[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
        del self.positions[object_id]
        if object_id in self.speeds:
            del self.speeds[object_id]

    def update(self, rects, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects, self.speeds

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (x, y, w, h)) in enumerate(rects):
            cX = int(x + w / 2.0)
            cY = int(y + h / 2.0)
            input_centroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i], timestamp)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            # Calculate distance matrix
            D = []
            for i in range(len(object_centroids)):
                row = []
                for j in range(len(input_centroids)):
                    dist = math.sqrt((object_centroids[i][0] - input_centroids[j][0])**2 + (object_centroids[i][1] - input_centroids[j][1])**2)
                    row.append(dist)
                D.append(row)
            D = np.array(D)

            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                if D[row, col] > self.max_distance:
                    continue

                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                # Update speed
                self.positions[object_id].append((timestamp, input_centroids[col]))
                
                # Keep only last few positions
                if len(self.positions[object_id]) > 5:
                    self.positions[object_id].pop(0)
                
                if len(self.positions[object_id]) >= 2:
                    # Calculate speed based on last two points
                    (t1, p1) = self.positions[object_id][-2]
                    (t2, p2) = self.positions[object_id][-1]
                    
                    time_diff = t2 - t1
                    if time_diff > 0:
                        dist_pixels = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                        dist_meters = dist_pixels / self.pixels_per_meter
                        speed_mps = dist_meters / time_diff
                        speed_kmh = speed_mps * 3.6
                        self.speeds[object_id] = speed_kmh

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            for col in unused_cols:
                self.register(input_centroids[col], timestamp)

        return self.objects, self.speeds
