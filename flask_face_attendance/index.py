#!/usr/bin/python
# -*- coding: utf-8 -*

from flask import Flask, render_template

import cv2
import numpy as np

app = Flask(__name__)

check_attendance=set([])
@app.route('/')
def index():
    return render_template('check.html')


@app.route('/face_recognition')
def check():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    # iniciate id counter
    id = 0

    # names related to ids: example ==> loze: id=1,  etc
    # 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
    names = ['None', 'eunjeong', 'jihwan', 'cheonshil', 'minjin']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    
    while True:
        ret, img = cam.read()
        img = cv2.flip(img, -1)  # Flip vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                id = names[id]
                print('id=',id)
                                   
                            
                confidence_print = "  {0}%".format(round(100 - confidence))
            if (confidence < 70):
                print('under 80')
                check_attendance.add(id)
            
                print('check result=',check_attendance)
            else:
                id = "unknown"
                confidence_print = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence_print), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()


    return render_template('face_recognition.html',check_attendance=check_attendance)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# 실습1. login.html파일을 style.css 파일과 연결해서 body 의 background-color 변경하기
