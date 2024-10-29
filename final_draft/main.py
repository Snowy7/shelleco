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
    else:
        from utils import pi_camera as camera
        from utils import led_controller

# Constants
frameWidth = 640
frameHeight = 480

camera.initCamera(frameWidth, frameHeight)

# Main loop
while True:
    img = camera.captureFrame()
    if img is not None:
        # Process the road
        imgStages, imgFinal = proccessRoad(img, frameWidth, frameHeight)
        
        cv2.imshow('Input', img)
    else:
        break    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.stop()
cv2.destroyAllWindows()