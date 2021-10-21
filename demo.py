import cv2
import mediapipe as mp
from Eye import *
from Head import *

webcam = cv2.VideoCapture(0)

# set webcam capture resolution
def change_res(width, height):
    webcam.set(3, width)
    webcam.set(4, height)

change_res(1280, 720)

# mp facial landmark detection
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

# create head and eye objects
head = Head()
left_eye = Eye("left")
right_eye = Eye("right")

while True:
    # new frame from the webcam
    _, frame = webcam.read()

    # MediaPipe facial landmark detection
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:

        # get one face only
        landmarks = results.multi_face_landmarks[0].landmark

        if(landmarks):

            """ Head angle detection in relation to the camera """
            head.calcAngles(frame, landmarks, visualize=False)

            # draw values of roll, yaw and pitch angles
            cv2.putText(frame, "roll: " + str(head.roll), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "yaw: " + str(head.yaw), (50, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "pitch: " + str(head.pitch), (50, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Exctract eyes using face mesh landmarks """

            left_eye.setLandmarks([(landmarks[463].x, landmarks[359].x, landmarks[257].x, landmarks[253].x), \
                            (landmarks[463].y, landmarks[359].y, landmarks[257].y, landmarks[253].y)])

            right_eye.setLandmarks([(landmarks[130].x, landmarks[243].x, landmarks[27].x, landmarks[23].x), \
                            (landmarks[130].y, landmarks[243].y, landmarks[27].y, landmarks[23].y)])

            left_eye.getEye(frame)
            right_eye.getEye(frame)


            """ Find pupils """

            left_eye.findPupil()
            right_eye.findPupil()

            # draw predicted pupil centers on the frame
            cv2.circle(frame, (int(left_eye.avg_coords[0]), int(left_eye.avg_coords[1])), 1, (0, 0, 255), 1)
            cv2.circle(frame, (int(right_eye.avg_coords[0]), int(right_eye.avg_coords[1])), 1, (0, 0, 255), 1)


            """ Blink detection """

            left_eye.detectBlink([landmarks[362], landmarks[263], landmarks[386], landmarks[374]])
            right_eye.detectBlink([landmarks[33], landmarks[133], landmarks[159], landmarks[145]]) 
        
            # draw text if blinking yes/no
            if(left_eye.opened == True and right_eye.opened == True):
                blink = "no"
            else: 
                blink = "yes"

            cv2.putText(frame, "blinking: " + blink, (50, 140), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # esc key to exit
        break
