import cv2

# get the system to check if we are windows or raspberry pi and import the correct libraries
import platform

if platform.system() == "Windows":
    from utils import ocv_camera as camera
    from utils import led_controller_fake as led
else:
    from utils import pi_camera as camera
    from final_draft.utils import gpio_controller as led

# all we want to do is walk straight untill we see a stop sign we stop
frameWidth = 640
frameHeight = 480

camera.initCamera(frameWidth, frameHeight)

while(True):
    
    frame = camera.captureFrame()
    cv2.imshow('img1',frame) #display the captured image

    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('images/og.png',frame)
        cv2.destroyAllWindows()
        break

camera.stop()