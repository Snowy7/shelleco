import cv2
stop_sign = cv2.CascadeClassifier("cascade_stop_sign.xml")

def GetStopSigns(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stop_sign_detected = stop_sign.detectMultiScale(grayFrame, 1.3, 5)
    return stop_sign_detected

    # Detect the stop sign, x,y = origin points, w = width, h = height
    #for (x, y, w, h) in stop_sign_detected:
    #    # Draw rectangle around the stop sign
    #    stop_sign_rectangle = cv2.rectangle(frame, (x,y),
    #                                        (x+w, y+h),
    #                                        (0, 255, 0), 3)
    #    # Write "Stop sign" on the bottom of the rectangle
    #    stop_sign_text = cv2.putText(img=stop_sign_rectangle,
    #                                 text="Stop Sign",
    #                                 org=(x, y+h+30),
    #                                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                                 fontScale=1, color=(0, 0, 255),
    #                                 thickness=2, lineType=cv2.LINE_4)

def GetFirstStopSignWidth(frame):
    sign_width = 0.001

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stop_sign_detected = stop_sign.detectMultiScale(grayFrame, 1.1, 5)
    
    # looping through the signs detect in the image 
    # getting coordinates x, y , width and height 
    for (x, y, h, w) in stop_sign_detected: 
  
        # draw the rectangle on the sign 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 
  
        # getting sign width in the pixels 
        sign_width = w 
  
    # return the sign width in pixel 
    return sign_width 