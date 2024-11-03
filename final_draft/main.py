import cv2
from sign_distance import proccess_stop_sign
from obstacle import obstacle_avoidance
import car_controller as cc

# get the system to check if we are windows or raspberry pi and import the correct libraries
import platform
from utils import ocv_camera as stopCam
from utils import pi_camera as camera

if platform.system() == "Windows":
    from utils import led_controller_fake as led
else:
    from utils import gpio_controller as led

# all we want to do is walk straight untill we see a stop sign we stop
frameWidth = 640
frameHeight = 480
FORWARD_PIN = 17

camera.initCamera(frameWidth, frameHeight)
stopCam.initCamera(frameWidth, frameHeight)

# Main loop
while True:
    img = camera.captureFrame()
    img2 = stopCam.captureFrame()
    if img is None:
        print("No frame")
        continue

    signFrame, signDistance = proccess_stop_sign(img2)

    forward = 1

    if signDistance < 200:
        forward = 0
    else:

        direction = obstacle_avoidance(img)

        if direction == 0:
            cc.forward()
        elif direction == -1:
            cc.left()
        elif direction == 1:
            cc.right()

    led.SetVoltage(FORWARD_PIN, forward)

    # show the image
    cv2.imshow("Stop Sign", signFrame)
    cv2.imshow("Obstacle Avoidance", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()
