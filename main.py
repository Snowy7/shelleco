from picamera2 import PiCamera2, Preview
from time import sleep

picam2 = PiCamera2()

# Start preview
picam2.start_preview(Preview.QTGL)
picam2.start()

sleep(10)
picam2.close()