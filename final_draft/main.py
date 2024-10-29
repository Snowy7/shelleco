import cv2
from road_detection import proccessRoad
useVide = False

if useVide:
    from utils import video_camera as camera
else:
    # get the system to check if we are windows or raspberry pi and import the correct libraries
    import platform
    if platform.system() == 'Windows':
        from utils import ocv_camera as camera
        from utils import led_controller_fake as led
    else:
        from utils import pi_camera as camera
        from utils import led_controller as led

# Constants
turnThreshold = 15
LEFT_LED_PIN = 17
RIGHT_LED_PIN = 27
frameWidth = 640
frameHeight = 480

camera.initCamera(frameWidth, frameHeight)

# Main loop
while True:
    img = camera.captureFrame()
    if img is not None:
        # Process the road
        imgFinal, turnAmount, turnDir = proccessRoad(img, frameWidth, frameHeight)
        if turnAmount > turnThreshold:
            # check if the target midpoint is on the left or right of the midpoint
            if turnDir < 0:
                #print("Turn left")
                led.TurnOnLED(LEFT_LED_PIN)
                led.TurnOffLED(RIGHT_LED_PIN)
            else:
                #print("Turn right")
                led.TurnOnLED(RIGHT_LED_PIN)
                led.TurnOffLED(LEFT_LED_PIN)
        else:
            led.TurnOffLED(LEFT_LED_PIN)
            led.TurnOffLED(RIGHT_LED_PIN)
        #cv2.imshow('Input', img)
    else:
        break    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.stop()
cv2.destroyAllWindows()