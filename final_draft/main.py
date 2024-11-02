import cv2
from sign_distance import proccess_stop_sign

# get the system to check if we are windows or raspberry pi and import the correct libraries
import platform

if platform.system() == "Windows":
    from utils import ocv_camera as camera
    from utils import led_controller_fake as led
else:
    from utils import pi_camera as camera
    from utils import gpio_controller as led

# all we want to do is walk straight untill we see a stop sign we stop
frameWidth = 640
frameHeight = 480
FORWARD_PIN = 17

camera.initCamera(frameWidth, frameHeight)

# Main loop
while True:
    img = camera.captureFrame()
    if img is None:
        print("No frame")
        continue
    
    signFrame, signDistance = proccess_stop_sign(img)
    
    forward = 1
    
    if signDistance < 100:
        forward = 0
        print("Stop sign detected")
    
    led.SetVoltage(FORWARD_PIN, forward)
    
    # show the image
    cv2.imshow('Input', signFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.stop()
cv2.destroyAllWindows()
