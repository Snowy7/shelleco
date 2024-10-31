import cv2
from utils.stop_sign import GetFirstStopSignWidth
from utils.stablizer import ExponentialMovingAverage, MovingAverage


Measured_Distance = 112
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

ma = MovingAverage(window_size=2)
ma2 = ExponentialMovingAverage(alpha=0.8)

def proccess_stop_sign(frame):
    width = GetFirstStopSignWidth(frame)

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
    
    return frame, est_d2
