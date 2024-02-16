#!/usr/bin/python3
import time, os
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
import cv2  # If using OpenCV to save images

load_dotenv()
nas_path = f"{os.getenv('NAS_PATH')}/stills"

# Create the folder if it doesn't exist
os.makedirs(nas_path, exist_ok=True)

time_format = "%Y-%m-%d_%H-%M-%S"
photos_per_second = 8
photo_interval = 1.0 / photos_per_second

lsize = (320, 240)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (1920, 1080), "format": "XRGB8888"},
    lores={"size": lsize, "format": "YUV420"}
)
picam2.configure(video_config)
picam2.start_preview()
picam2.start()

w, h = lsize
prev = None
capturing = False
ltime = 0

counter = 1

def save_image(image, filename):
    filename_with_path = f"{nas_path}/{filename}.jpg"
    cv2.imwrite(filename_with_path, image)  # Save using OpenCV

def save_image_local(image, filename):
    filename_with_path = f"./captures/{filename}.jpg"
    cv2.imwrite(filename_with_path, image)  # Save using OpenCV

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[: w * h].reshape(h, w)

    if prev is not None:
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not capturing:
                capturing = True
                print("Motion detected", mse)
            ltime = time.time()
        elif capturing and (time.time() - ltime > 5.0):
            capturing = False
            print("Motion stopped")
        
        # If motion is ongoing, take photos
        if capturing:
            main_image = picam2.capture_array("main")
            counter_str = str(counter).zfill(3)
            timestamp = datetime.now().strftime(time_format) + "_" + counter_str
            save_image_local(main_image, timestamp)
            save_image(main_image, timestamp)
            time.sleep(photo_interval)
            counter += 1
    else:
        counter = 0
        time.sleep(photo_interval)
        
    prev = cur

picam2.stop()