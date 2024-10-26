import cv2
from detection.stop_sign import GetFirstStopSignWidth
from utils.stablizer import ExponentialMovingAverage, MovingAverage
from picamera2 import Picamera2


Measured_Distance = 122
Known_Width = 0.28

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
  
# defining the fonts 
fonts = cv2.FONT_HERSHEY_COMPLEX

# focal length finder function 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 
  
    # finding the focal length 
    focal_length = (width_in_rf_image * measured_distance) / real_width 
    return focal_length 
  
# distance estimation function 
def Distance_finder(Focal_Length, real_width, width_in_frame): 
  
    distance = (real_width * Focal_Length)/width_in_frame 
  
    # return the distance 
    return distance

# reading reference_image from directory 
ref_image = cv2.imread("images/og.png") 
ref_image_sign_width = GetFirstStopSignWidth(ref_image)

Focal_Length = Focal_Length_Finder(Measured_Distance, Known_Width, ref_image_sign_width)

print(ref_image_sign_width, Focal_Length)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

ma = MovingAverage(window_size=2)
ma2 = ExponentialMovingAverage(alpha=0.8)
while True:
    frame = picam2.capture_array()

    width = GetFirstStopSignWidth(frame)
    print(width)

    Distance = Distance_finder(Focal_Length, Known_Width, width)
    est_d = ma2.add_value(Distance)
    est_d2 = ma.add_value(est_d)

    # draw line as background of text 
    cv2.line(frame, (30, 30), (230, 30), RED, 32) 
    cv2.line(frame, (30, 30), (230, 30), BLACK, 28) 
  
    # Drawing Text on the screen 
    cv2.putText( 
        frame, f"Distance: {round(est_d2,2)} CM", (30, 35),  
      fonts, 0.6, GREEN, 2) 
    
    cv2.imshow('Overview', frame)

    if cv2.waitKey(1) == ord('q'):
        picam2.release()
        cv2.destroyAllWindows()
        break

exit()