import cv2

cap = cv2.VideoCapture(0)

stop_sign = cv2.CascadeClassifier("cascade_stop_sign.xml")

while cap.isOpened():
    _, frame = cap.read()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    stop_sign_detected = stop_sign.detectMultiScale(grayFrame, 1.3, 5)

        # Detect the stop sign, x,y = origin points, w = width, h = height
    for (x, y, w, h) in stop_sign_detected:
        # Draw rectangle around the stop sign
        stop_sign_rectangle = cv2.rectangle(frame, (x,y),
                                            (x+w, y+h),
                                            (0, 255, 0), 3)
        # Write "Stop sign" on the bottom of the rectangle
        stop_sign_text = cv2.putText(img=stop_sign_rectangle,
                                     text="Stop Sign",
                                     org=(x, y+h+30),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale=1, color=(0, 0, 255),
                                     thickness=2, lineType=cv2.LINE_4)


    cv2.imshow('Overview', frame)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

exit()