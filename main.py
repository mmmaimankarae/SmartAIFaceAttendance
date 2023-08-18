import os
import pickle

import cv2

    # Start the Camera
cap = cv2.VideoCapture(0) # Open Camera (Order of cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

backGround = cv2.imread('Interface/background.png') # import background

    # Import mode of check attendance in the list
modePath = 'Interface/Modes'
modePathList = os.listdir(modePath) # list of name.file
modeList = []

for path in modePathList:
    modeList.append(cv2.imread(os.path.join(modePath, path)))

    # Lode the encoding file
print("Loading Encode File...")
# Read(r) file .p that data is binary mode
file = open('EncodeFace.p', 'rb')
# Open (Unpickle) to load data into variable
encodeListAndID = pickle.load(file)
# Close file (After that can not read)
file.close()
# Separate data is 128 measure point and ID
encodeFaceList, studentIDList = encodeListAndID
print("Encode File Loaded")


while True:
    success, image = cap.read() # 1. Capture from camera by frame:frame

    # Define start point and end point on GUI >> start y: end y, start x: end x
    backGround[162:(162 + 480), 55:(55 + 640)] = image # point of Camera
    backGround[0:(0 + 800), 780:(780 + 500)] = modeList[0] # point of Modes

    cv2.imshow("Face Attendance", backGround) # 2. Create display(GUI)

    # 3. receive action from User on GUI
    cv2.waitKey(1)