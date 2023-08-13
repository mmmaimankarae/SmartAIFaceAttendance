import os

import cv2

    # Start the Camera
cap = cv2.VideoCapture(0) # Open Camera (Order of cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

backGround = cv2.imread('Interface/background.png') # import background

modePath = 'Interface/Modes'
modePathList = os.listdir(modePath)
modeList = []
#for path in modePathList:
    #modeList.append(cv2.imread(os.path.join(modePath, path)))
print(modePathList)

while True:
    success, image = cap.read() # Capture from camera by frame:frame
    backGround[162:(162 + 480), 55:(55 + 640)] = image
    cv2.imshow("Face Attendance", backGround) # Display(GUI)

    cv2.waitKey(1)