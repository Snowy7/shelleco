import cv2

cap = cv2.VideoCapture(0)
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