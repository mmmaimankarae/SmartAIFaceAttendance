    # WRITE BY JAVASCRIPTS SYNTAX #
# manage database realtime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# manage storage image
from firebase_admin import storage

# read data
import csv
import numpy as np
import os

    # SETTING DATABASE TO LINK WITH LOCAL DATA #
# create default data for database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    # realtime database url
    'databaseURL': "https://facerecognition-41dc8-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "facerecognition-41dc8.appspot.com"
})

    # CREATE DATABASE REFERENCE #
ref = db.reference('Students') # create directory

    # READ DATA FILE #
f = open("AIsec1List.csv","r")
with open('AIsec1List.csv', newline='') as csvfile: # next data by newline
    arr = list(csv.reader(csvfile))

arr = arr[1:] # delete first line (header)

    # ADD DATA (key, value) #
data = {}
for i in arr:
    studentID = i[0]
    data[studentID] = {
        "name": i[1],
        "degree": i[3],
        "major": i[4],
        "year": i[2],
        "total attendance": i[5],
        "rate attendance": i[6],
        "day": i[7],
        "check the time": i[8]
    }

    # IMPORT IMAGE INTO DATABASE #
facePath = 'showFace'
facePathList = os.listdir(facePath) # list of facename.file
faceList = []
studentIDList = []
    
for path in facePathList:
    if path == ".DS_Store":
        continue
    # upload image into the floder
    image = f'{facePath}/{path}'
    # referance to bucket Google Cloud Storage
    bucket = storage.bucket()
    # manage image
    blob = bucket.blob(image)
    # upload image, that managed
    blob.upload_from_filename(image)

    # UPLOAD DATA INTO DATABASE REALTIME #
for key,value in data.items():
   ref.child(key).set(value)
