import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

#Importing images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    full_path = os.path.join(folderModePath, path)
    imgModeList.append(cv2.imread(full_path))

#load the encoding file
print("Loading Encode File...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, CriminalIds = encodeListKnownWithIds
#print(CriminalIds)
print("Encode File Loaded")


while True:
    success, img = cap.read()
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]
    
    
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print("matches", matches)
        #print("FaceDis", faceDis)
        
        matchIndex = np.argmin(faceDis)
        #print("Match Index", matchIndex)
        
        if matches[matchIndex]:
            #print("Wanted Criminal Detected")
            #print(CriminalIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, y2 - y1, x2 - x1  # Swap h and w
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
    
    cv2.imshow("Criminal", imgBackground)
    cv2.waitKey(1)

