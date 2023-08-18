import os
import cv2
import face_recognition
import pickle

    # Import student image into list
facePath = 'Images'
facePathList = os.listdir(facePath) # list of name.file
faceList = []
studentIDList = []
for path in facePathList:
    faceList.append(cv2.imread(os.path.join(facePath, path)))
    studentIDList.append(os.path.splitext(path)[0]) # split name and .file, fill name(ID) into list

# covert face to number (keep it in array, 128 measure point identify the face)
def findEncoding(imagesList):
    encodeLit = []
    for image in imagesList:
        # change color BGR(openCV) to RGB(faceRecognition)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # encoding tha image of face (128 measure)
        encode = face_recognition.face_encodings(image)[0]
        encodeLit.append(encode)
    return  encodeLit

print("Encoding Started...")
encodeFaceList = findEncoding(faceList)
encodeListAndID = [encodeFaceList, studentIDList] # storage data by list (keep array encoding with ID)
print("Encoding Complete")
# Create file .p and write(w) with binary(b) mode (suitable for picture)
file = open("EncodeFace.p", 'wb')
# Write (pickle) data list of array encoding and ID (Data = Object of python that can save and recall to use)
pickle.dump(encodeListAndID, file)
# Close file (After that can not write)
file.close()
print("File Save")