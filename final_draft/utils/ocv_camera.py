import cv2
import platform

if platform.system() == "Windows":
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
frame = None


def initCamera(width, height):
    cap.set(3, width)
    cap.set(4, height)


def captureFrame():
    global frame
    success, img = cap.read()
    if success:
        frame = img
    return img


def getFrame():
    global frame
    return frame

def stop():
    cap.release()