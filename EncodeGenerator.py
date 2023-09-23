import os
import cv2
import face_recognition
import pickle

    # IMPORT STUDENT IMAGE INTO LIST #
facePath = 'Images'
facePathList = os.listdir(facePath) # list of facename.file
faceList = []
studentIDList = []
    
for path in facePathList:
    if path == ".DS_Store":
        continue
    # keep path of mode
    image = cv2.imread(os.path.join(facePath, path))
    if image is not None:
        faceList.append(image)
        # split name and .file, fill name(ID) into list
        studentIDList.append(os.path.splitext(path)[0])
    else:
        print(f"Unable to read image: {path}")
    
    # TRANSFORM OBJECT TO BIT #
def findEncoding(imagesList):
    encodeLit = []
    for image in imagesList:
        # change color BGR(openCV) to RGB(faceRecognition)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # encoding the image of face (128 measure point identify)
        encode = face_recognition.face_encodings(image)[0]
        encodeLit.append(encode)
    return  encodeLit

print("Encoding Started...")
# call method for encoding
encodeFaceList = findEncoding(faceList)
# storage data by list (keep array encoding with ID)
encodeListAndID = [encodeFaceList, studentIDList]
print("Encoding Complete")

    # CREATE FILE FOR ENCODDING OBJECT PYTHON #
# write(w) with binary(b) mode (suitable for picture)
file = open("EncodeFace.p", 'wb')
# write data list of array encoding and ID
pickle.dump(encodeListAndID, file)
# close file (After that can not write)
file.close()
print("File Save")