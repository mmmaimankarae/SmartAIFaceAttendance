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

# simple math method
import numpy as np

# day and time
from datetime import datetime

# manage database realtime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# manage storage image
from firebase_admin import storage

    # SETTING DATABASE TO LINK WITH LOCAL DATA #
# create default data for database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    # realtime database url
    'databaseURL': "https://facerecognition-41dc8-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "facerecognition-41dc8.appspot.com"
})
bucket = storage.bucket() # call data(image) from storage
imageStudent = [] # store the image

    # START THE CAMERA #
cap = cv2.VideoCapture(0)  # open Camera (order of cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

backGround = cv2.imread('Interface/background.png')  # import background

    # IMPORT MODE OF CHECK ATTENDANCE IN THE LIST #
modePath = 'Interface/modes'
modePathList = os.listdir(modePath)  # list of modename.file
modeList = []

    # SETTING MODE #
# 0 (onTime), 1 (alraedy), 2 (notFound), 3 (mark), 4 (default), 5 (late)
modeType = 4
counter = 0 # count fram for change mode
id = -1
checkMatche = 0

# SETTING TIME #
late = True
alreadyCheck = False
now = datetime.now()
# morning class
mr0900 = now.replace(hour = 9, minute = 0, second = 0)
mr0915 = now.replace(hour = 9, minute = 15, second = 59)
endClass1 = now.replace(hour = 12, minute = 00, second = 00)
# afternoon class
af1300 = now.replace(hour = 13, minute = 0, second = 0)
af1315 = now.replace(hour = 13, minute = 15, second = 59)
mid = now.replace(hour = 23, minute = 59, second = 59)


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
global idG
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
    encodeNewface = face_recognition.face_encodings(imageResize, faceCurrent, num_jitters=10, model="cnn")

    # define start point and end point on GUI (start y: end y, start x: end x)
    backGround[168:(168 + 480), 70:(70 + 640)] = image  # point of Camera
    backGround[0:(0 + 800), 780:(780 + 500)] = modeList[modeType]  # point of modes

        # COMPARE ENCODING OF UNKNOW FACE AND KNOW FACE #
    # make loop of both together
    for encodeFace, faceLocation in zip(encodeNewface, faceCurrent):
        # compare if match, that return True
        matches = face_recognition.compare_faces(encodeFaceList, encodeFace, tolerance = 0.4)
        
        # calculate distance on both of face and return float of different
        faceDistance = face_recognition.face_distance(encodeFaceList, encodeFace)
        
        # choose match ID, that differance distance are min
        matchIndex = np.argmin(faceDistance)
        
            # CRATE RECTAGLE TO DETECT FACE #
        if matches[matchIndex]:
            #print(studentIDList[matchIndex])
            # points of face dectection
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            # setting point for frame dectect
            bbox = 45 + x1, 162 + y1, x2 - x1, y2 - y1
            backGround = cvzone.cornerRect(backGround, bbox, rt=0, colorC=(13, 100, 255))
            id = studentIDList[matchIndex]

            studentInfo = db.reference(f'Students/{id}').get()
            if studentInfo['day'] != '0':
                beforeDay = datetime.strptime(studentInfo['day'], "%d/%m/%Y")
                lastChecking = datetime.strptime(studentInfo['check the time'], "%H:%M")
                today = now.strftime("%d/%m/%Y")
                if (beforeDay.strftime("%d/%m/%Y") == today and 
                    (mr0900.strftime("%H:%M") <= lastChecking.strftime("%H:%M")  <= endClass1.strftime("%H:%M") 
                    or af1300.strftime("%H:%M") <= lastChecking.strftime("%H:%M") <= mid.strftime("%H:%M"))):
                    modeType = 1
                    checkMatche = 0
                    counter = 1
            
                # CHANGE MODE #
            if counter == 0:
                modeType = 0
                counter = 1
                checkMatche = 1
        else:
            modeType = 2
            checkMatche = 0
            counter = 0
        backGround[0:(0 + 800), 780:(780 + 500)] = modeList[modeType]
                
        # DOWNLOAD & UPLOAD INFORMATION OF STUDENTS WHO HAS ATTENDANCE #
    if counter != 0 and checkMatche != 0:
        if counter == 1:
            # GET all information of the student
            #studentInfo = db.reference(f'Students/{id}').get()
            #print(studentInfo)
            
            # GET image of the student 
            blob = bucket.get_blob(f'showFace/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imageStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            
            # UPDATE data of attendance
            ref = db.reference(f'Students/{id}')
                # the day on attendance
            day = datetime.now().strftime("%d/%m/%Y")
            ref.child('day').set(day)
                
                # time on attendance
            now = datetime.now()
            checkingTime = now.strftime("%H:%M")
            ref.child('check the time').set(checkingTime)
            
            if mr0900 <= now <= mr0915 or af1300 <= now <= af1315:
                late = False
            
                # count attendance
            studentInfo['total attendance'] = str(int(studentInfo['total attendance']) + 1)
            ref.child('total attendance').set(studentInfo['total attendance'])
            if 'rate attendance' not in studentInfo:
                studentInfo['rate attendance'] = 0
            if late == True:
                studentInfo['rate attendance'] = str(int(studentInfo['rate attendance']) + 1)
                ref.child('rate attendance').set(studentInfo['rate attendance'])
        
        if 15 < counter < 25:
            modeType = 3

        backGround[0:(0 + 800), 780:(780 + 500)] = modeList[modeType]  # point of modes   
            
        if counter <= 15 and late == False:
                # SHOW INFORMATION OF THE STUDENT #
            cv2.putText(backGround, str(studentInfo['name']),(905, 415),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(id),(985, 443),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['degree']),(920, 486),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['major']),(920, 513),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['year']),(935, 540),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(day),(877, 596),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)
            cv2.putText(backGround, str(checkingTime),(1100, 596),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['total attendance']),(1037, 736),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            
            backGround[184:184+175, 943:943+175] = imageStudent
        elif counter <= 15 and late == True:
            modeType = 5
            # SHOW INFORMATION OF THE STUDENT #
            cv2.putText(backGround, str(studentInfo['name']),(905, 415),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(id),(985, 443),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['degree']),(920, 486),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['major']),(920, 513),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['year']),(935, 540),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            cv2.putText(backGround, str(day),(877, 596),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)
            cv2.putText(backGround, str(checkingTime),(1100, 596),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)
            cv2.putText(backGround, str(studentInfo['total attendance']),(1037, 736),cv2.FONT_HERSHEY_DUPLEX, 0.625, (0, 0, 0), 1)
            
            backGround[184:184+175, 943:943+175] = imageStudent
            
        counter += 1
        
        if counter >= 30:
            counter = 0
            modeType = 4
            studentInfo = []
            imageStudent = []
    idG = id
            
    cv2.imshow("Face Attendance", backGround)  # create GUI (display)
    #print(idG)

    # receive action from User on GUI
    key = cv2.waitKey(1)
    # exit when key q, Q, Esc
    #if key == ord('q') or key == ord('Q') or key == 27:
        #break

# CLOSE THE GUI #
cap.release()
cv2.destroyAllWindows()