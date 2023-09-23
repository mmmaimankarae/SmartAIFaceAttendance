# manage about os (computer directory)
import os

# transform object to bit (serializing), bit to object (de-serializing)
import pickle

# manage about image
import cv2

# detect object
import cvzone

# face detection
import face_recognition
import numpy as np

# START THE CAMERA #
cap = cv2.VideoCapture(0)  # open Camera (order of cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

backGround = cv2.imread('Interface/background.JPG')  # import background

# IMPORT MODE OF CHECK ATTENDANCE IN THE LIST #
modePath = 'Interface/Modes'
modePathList = os.listdir(modePath)  # list of modename.file
modeList = []

for path in modePathList:
    # keep path of mode
    modeList.append(cv2.imread(os.path.join(modePath, path)))

    # LODE THE ENCODING FILE #
print("Loading Encode File...")
# read(r) file .p that data is binary mode(b)
file = open('EncodeFace.p', 'rb')
# open (unpickle) to load data into variable
encodeListAndID = pickle.load(file)
# close file (after that can not read)
file.close()
# separate data is 128 measure point and ID
encodeFaceList, studentIDList = encodeListAndID
print("Encode File Loaded")

while True:
    success, image = cap.read()  # capture from camera by frame:frame

        # RESIZE THE IMAGE TO ITS SMALLER 25% #
    imageResize = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    # change color RGB(faceRecognition) to BGR(openCV)
    imageResize = cv2.cvtColor(imageResize, cv2.COLOR_BGR2RGB)

    # DETECT FACE ON THE CAMARE #
    # return list pixel points of face (top, right, bottom, left)
    faceCurrent = face_recognition.face_locations(imageResize)

        # ENCODING UNKNOW NEW FACE #
    encodeNewface = face_recognition.face_encodings(imageResize, faceCurrent)

    # define start point and end point on GUI (start y: end y, start x: end x)
    backGround[162:(162 + 480), 55:(55 + 640)] = image  # point of Camera
    backGround[0:(0 + 800), 780:(780 + 500)] = modeList[0]  # point of modes

        # COMPARE ENCODING OF UNKNOW FACE AND KNOW FACE #
    # make loop of both together
    for encodeFace, faceLocation in zip(encodeNewface, faceCurrent):
        # compare if match, that return True
        matches = face_recognition.compare_faces(encodeFaceList, encodeFace)
        # calculate distance on both of face and return float of different
        faceDistance = face_recognition.face_distance(encodeFaceList, encodeFace)
        print("matches", matches)
        print("faceDis", faceDistance)

        #matchIndex = np.argmin(faceDistance)
        # print("match index ", matchIndex)

        #if matches[matchIndex]:
            # print("known face detected")
            # print(studentIDList)

            #y1, x2, y2, x1 = faceLocation
            #y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            #bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            #backGround = cvzone.cornerRect(backGround, bbox, rt=0)

    cv2.imshow("Face Attendance", backGround)  # create GUI (display)

    # receive action from User on GUI
    cv2.waitKey(1)