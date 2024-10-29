import cv2

videoPath = '../Road/project_video.mp4'
cap = cv2.VideoCapture(videoPath)
frame = None
size = (640, 480)

def initCamera(width, height):
    size = (width, height)

def captureFrame():
    global frame
    success, img = cap.read()
    # resize the frame
    img = cv2.resize(img, size, None)
    if success:
        frame = img
    return img


def getFrame():
    global frame
    return frame

def stop():
    cap.release()