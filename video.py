# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-mjpeg-streaming-web-server-picamera2/

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:7123
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import logging
import socketserver
from http import server
from threading import Condition
import threading
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import time
import datetime
import cv2
import os
PAGE = """\
<html>
<head>
<title>Caveracer Video Stream</title>
</head>
<body>
<h1 style="text-align:center;">Caveracer Video Stream</h1>
<img style="display:block; margin-left:auto; margin-right:auto;" src="stream.mjpg"/>
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())
picam2.set_controls({
    "ExposureTime": 20000,  # Exposure time in microseconds (adjust as needed)
    "AnalogueGain": 0.5,    # Gain multiplier (1.0 is no gain, 2.0 is double the gain, etc.)
})
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

def capture_frames():
    counter = 0
    with open("screen_shot/rgb.txt", "w") as f:
        while counter < 900:
            counter +=1
            time.sleep(0.066)  # Capture every 10 seconds
            frame = picam2.capture_array()
            timestamp = time.time()
            
            cv2.imwrite(f"screen_shot/{counter:06d}.jpg", frame)
            
            f.write(f"{timestamp} {counter:06d}.jpg\n")
threading.Thread(target=capture_frames, daemon=True).start()
try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print("\nInterrupted by user. Stopping camera and server.")
finally:
    picam2.stop_recording()
