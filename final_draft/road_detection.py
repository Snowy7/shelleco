import numpy as np
import cv2
from utils import utils

intialTracbarVals = [24,55,12,100]   #wT,hT,wB,hB
count = 0
noOfArrayValues = 10
global arrayCurve, arrayCounter
arrayCounter = 0
arrayCurve = np.zeros([noOfArrayValues])
myVals=[]

utils.initializeTrackbars(intialTracbarVals)

def proccessRoad(img, frameWidth, frameHeight, turnThreshold):
    global arrayCurve, arrayCounter, noOfArrayValues, intialTracbarVals, myVals, count
    imgWarpPoints = img.copy()
    imgFinal = img.copy()
    imgCanny = img.copy()

    imgUndis = utils.undistort(img)
    imgThres,imgCanny,imgColor = utils.thresholding(imgUndis)
    src = utils.valTrackbars()
    imgWarp = utils.perspective_warp(imgThres, dst_size=(frameWidth, frameHeight), src=src)
    imgWarpPoints = utils.drawPoints(imgWarpPoints, src)
    imgSliding, curves, lanes, ploty = utils.sliding_window(imgWarp, draw_windows=True)

    try:
        curverad =utils.get_curve(imgFinal, curves[0], curves[1])
        lane_curve = np.mean([curverad[0], curverad[1]])
        imgFinal = utils.draw_lanes(img, curves[0], curves[1],frameWidth,frameHeight,src=src)

        ## Average
        currentCurve = lane_curve // 50
        if  int(np.sum(arrayCurve)) == 0:averageCurve = currentCurve
        else:
            averageCurve = np.sum(arrayCurve) // arrayCurve.shape[0]
        if abs(averageCurve-currentCurve) >200: arrayCurve[arrayCounter] = averageCurve
        else :arrayCurve[arrayCounter] = currentCurve
        arrayCounter +=1
        if arrayCounter >=noOfArrayValues : arrayCounter=0

    except:
        lane_curve=00
        pass

    imgFinal = utils.drawLines(imgFinal,lane_curve)
    targetMidPoint = (int(lane_curve // 100) + img.shape[1] // 2, img.shape[0])
    midPoint = (img.shape[1] // 2, img.shape[0])
    
    # draw the target midpoint  
    cv2.circle(imgFinal, targetMidPoint, 5, (0, 0, 255), -1)
    # draw the midpoint
    cv2.circle(imgFinal, midPoint, 5, (0, 255, 0), -1)
    
    # draw a threshold zone (blue square)
    cv2.rectangle(imgFinal, (midPoint[0] - turnThreshold, midPoint[1] - turnThreshold), (midPoint[0] + turnThreshold, midPoint[1] + turnThreshold), (255, 0, 0), 2)
    
    turnAmount = abs(targetMidPoint[0] - midPoint[0])
    turnDir = -1 if targetMidPoint[0] < midPoint[0] else 1
    
    """ if turnAmount > turnThreshold:
        # check if the target midpoint is on the left or right of the midpoint
        if targetMidPoint[0] < midPoint[0]:
            #print("Turn left")
            TurnOnLED(LEFT_LED_PIN)
            TurnOffLED(RIGHT_LED_PIN)
        else:
            #print("Turn right")
            TurnOnLED(RIGHT_LED_PIN)
            TurnOffLED(LEFT_LED_PIN)
    else:
        TurnOffLED(LEFT_LED_PIN)
        TurnOffLED(RIGHT_LED_PIN) """


    imgThres = cv2.cvtColor(imgThres,cv2.COLOR_GRAY2BGR)
    imgBlank = np.zeros_like(img)
    # picam fix array dimensions
    #stacking
    #imgStacked = utils.stackImages(0.4, ([imgUndis, imgUndis, imgWarpPoints],
    #                                     [imgColor, imgCanny, imgThres],
    #                                     [imgWarp,imgSliding,imgFinal]
    #                                     ))
    
    #cv2.imshow("PipeLine",imgStacked)
    cv2.imshow("Result", imgFinal)
    return imgFinal, turnAmount