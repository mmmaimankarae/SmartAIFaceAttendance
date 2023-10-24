import os
import cv2
import face_recognition
import pickle

base_directory = 'Train'
person_directories = [os.path.join(base_directory, directory_name) for directory_name in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, directory_name))]

all_encodings = []
all_student_ids = []
print("Encoding Started...")
for person_directory in person_directories:
    person_name = os.path.basename(person_directory)  # คุณสามารถใช้ชื่อของโฟลเดอร์เป็นชื่อของคน

    person_image_list = os.listdir(person_directory)
    person_encodings = []

    for image_filename in person_image_list:
        if image_filename == ".DS_Store":
            continue
        image = cv2.imread(os.path.join(person_directory, image_filename))
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(image, num_jitters=100, model="cnn")
            if len(face_encodings) > 0:
                encode = face_encodings[0]
                person_encodings.append(encode)
            else:
                print(image_filename)

    all_encodings.extend(person_encodings)
    all_student_ids.extend([person_name] * len(person_encodings))


encodeListAndID = [all_encodings, all_student_ids]
# call method for encoding
#encodeFaceList = findEncoding(faceList)
# storage data by list (keep array encoding with ID)
#encodeListAndID = [encodeFaceList, studentIDList]
print("Encoding Complete")

    # CREATE FILE FOR ENCODDING OBJECT PYTHON #
# write(w) with binary(b) mode (suitable for picture)
file = open("EncodeFace.p", 'wb')
# write data list of array encoding and ID
pickle.dump(encodeListAndID, file)
# close file (After that can not write)
file.close()
print("File Save")