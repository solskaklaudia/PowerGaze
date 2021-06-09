import cv2
import mediapipe as mp
import numpy as np
import math

webcam = cv2.VideoCapture(0)

## mp facial landmark detection
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

while True:
    # new frame from the webcam
    _, frame = webcam.read()

    ## mp facial landmark detection
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame,faceLms,mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)
        landmarks = results.multi_face_landmarks[0].landmark

        r_eye = (landmarks[33].x, landmarks[33].y, landmarks[33].z) # right eye corner point
        l_eye = (landmarks[263].x, landmarks[263].y, landmarks[263].z) # left eye corner point
        
        # drawing line between the eyes
        cv2.line(frame, (int(r_eye[0]*frame.shape[1]),int(r_eye[1]*frame.shape[0])), (int(l_eye[0]*frame.shape[1]),int(l_eye[1]*frame.shape[0])), (255,0,0), 2)
        # calculating distance between the eyes
        eyes_len = math.sqrt((r_eye[0] - l_eye[0])**2 + (r_eye[1] - l_eye[1])**2 + (r_eye[2] - l_eye[2])**2)

        # calculating roll
        roll = math.asin((r_eye[1] - l_eye[1]) / eyes_len) * 180 / math.pi

        b_nose = [(landmarks[64].x+landmarks[294].x)/2, \
            (landmarks[64].y+landmarks[294].y)/2, \
                (landmarks[64].z+landmarks[294].z)/2 ] # mean point from two symmetric nose wings landmarks
        t_nose = [landmarks[1].x, landmarks[1].y, landmarks[1].z] # nose tip point
             
        # drawing line from below the nose to the nose tip
        cv2.line(frame, (int(b_nose[0]*frame.shape[1]),int(b_nose[1]*frame.shape[0])), (int(t_nose[0]*frame.shape[1]),int(t_nose[1]*frame.shape[0])), (255,0,255), 2)
        # calculating length of the nose line
        nose_len = math.sqrt((b_nose[0] - t_nose[0])**2 + (b_nose[1] - t_nose[1])**2 + (b_nose[2] - t_nose[2])**2)

        # calculating yaw and pitch
        yaw = math.asin((b_nose[0] - t_nose[0]) / nose_len) * 180 / math.pi
        pitch = math.asin((b_nose[1] - t_nose[1]) / nose_len) * 180 / math.pi
        
        # drawing values of roll, yaw and pitch angles
        cv2.putText(frame, "roll: " + str(roll), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "yaw: " + str(yaw), (50, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "pitch: " + str(pitch), (50, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27: # esc key to exit
        break
