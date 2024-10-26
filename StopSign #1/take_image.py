import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()


while(True):
    
    frame = picam2.capture_array()
    cv2.imshow('img1',frame) #display the captured image

    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('images/og.png',frame)
        cv2.destroyAllWindows()
        break

picam2.close()