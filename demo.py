from EyesBlink import eyesBlink
from HeadAngle import calcAngles, drawLine, lineLength
import cv2
import mediapipe as mp
from Eyes import *

webcam = cv2.VideoCapture(0)

def change_res(width, height):
    webcam.set(3, width)
    webcam.set(4, height)

change_res(1280, 720)

# mp facial landmark detection
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

pupil_coords = [[50],[50]]
max_samples = 5
avg_coords = [50,50]

while True:
    # new frame from the webcam
    _, frame = webcam.read()

    gray = frame[0:1, 0:1]
    image = frame[0:1, 0:1]
    erosion_pupil = frame[0:1, 0:1]

    # mp facial landmark detection
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        # for faceLms in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(frame,faceLms,mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec) # draw face mesh
        landmarks = results.multi_face_landmarks[0].landmark

        """ Head angle detection in relation to the camera """

        roll, yaw, pitch = calcAngles(frame, landmarks, visualize=False)

        # drawing values of roll, yaw and pitch angles
        cv2.putText(frame, "roll: " + str(roll), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "yaw: " + str(yaw), (50, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "pitch: " + str(pitch), (50, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        """ Exctract eyes """

        if(landmarks[464] or landmarks[33]):
            eyes = Eyes(frame, landmarks)
            eyes.getEyes(show=True)

        """ Blink detection """
        
        cv2.putText(frame, "blinking: " + eyesBlink(landmarks), (50, 140), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # esc key to exit
        break
