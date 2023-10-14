import cv2
import numpy as np
import os
import mediapipe
import HandTrackingModule as htm
imgCanvas=np.zeros((480,680,3),np.uint8)
imgCanvas=cv2.flip(imgCanvas,1)
folderpath = "PaintImages"
drawColor=(255,0,255)
brushThickness=15
eraserThickness = 50
xp,yp=0,0
myList = os.listdir(folderpath)
print(myList)
Overlaylist=[]
for imPath in myList:
    image=cv2.imread(f'{folderpath}/{imPath}')
    Overlaylist.append(image)
print(len(Overlaylist))
header=Overlaylist[0]
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=htm.handDetector(detectionCon=0.85)
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList,_ = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmlist)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        #print(fingers)
        if fingers[1] and fingers[2]:
            if y1<170:
                if 315<x1<550:
                    header=Overlaylist[0]
                    drawColor=(0,0,255)
                elif 580<x1<815:
                    header=Overlaylist[1]
                    drawColor=(0,128,0)
                elif 845<x1<1080:
                    header=Overlaylist[2]
                    drawColor=(0,255,255)
                elif 1140<x1<1280:
                    header=Overlaylist[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), drawColor, cv2.FILLED)
            #print("Selection Mode")
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15 ,(255,0,255),cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)


    img[0:170,0:1280]=header
    cv2.imshow("Image",img)
    cv2.imshow("ImageCanvas", imgCanvas)
    cv2.waitKey(1)