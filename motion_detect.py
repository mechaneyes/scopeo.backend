#!/usr/bin/python3
import time, os
from dotenv import load_dotenv
from datetime import datetime

import numpy as np

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

load_dotenv()
os.getenv('NAS_PATH')

time_format = "%Y-%m-%d-%H-%M-%S"
frame_rate = 30

lsize = (320, 240)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"}, lores={
                                                    "size": lsize, "format": "YUV420"})
picam2.configure(video_config)
picam2.start_preview()
encoder = H264Encoder(2000000, repeat=True)
encoder.output = CircularOutput()
picam2.encoder = encoder
picam2.start()
picam2.start_encoder(encoder)

w, h = lsize
prev = None
encoding = False
ltime = 0

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and
        # previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not encoding:
                filename = datetime.now().strftime(time_format)
                encoder.output.fileoutput = f"./captures/{filename}.h264"
                encoder.output.start()
                encoding = True
                print("New Motion", mse)
            ltime = time.time()
        else:
            if encoding and time.time() - ltime > 5.0:
                encoder.output.stop()
                encoding = False
                time.sleep(1)
                os.system(f"ffmpeg -r {frame_rate} -i ./captures/{filename}.h264 -vcodec copy {os.getenv('NAS_PATH')}{filename}.mp4")
                os.system(f"rm ./captures/{filename}.h264")
    prev = cur

picam2.stop_encoder()