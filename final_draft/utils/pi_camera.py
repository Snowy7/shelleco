from picamera2 import Picamera2

picam2 = Picamera2()
frame = None

def initCamera(width, height):
    picam2.configure(
        picam2.create_preview_configuration(main={"format": "BGR888", "size": (width, height)})
    )
    picam2.start()


def getCam():
    global picam2
    return picam2


def captureFrame():
    global frame
    frame = picam2.capture_array()
    return frame


def getFrame():
    global frame
    return frame

def stop():
    picam2.stop()