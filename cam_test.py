import platform
if platform.system() == "Windows":
    from final_draft.utils import ocv_camera as camera
else:
    from final_draft.utils import pi_camera as camera
    
import cv2

# just distplay the camera feed
camera.initCamera(640, 480)

while True:
    img = camera.captureFrame()
    if img is None:
        print("No frame")
        continue
    
    cv2.imshow('Input', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.stop()
cv2.destroyAllWindows()