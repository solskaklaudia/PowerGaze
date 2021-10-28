import cv2
import mediapipe as mp
from Eye import *
from Head import *
import autopy

webcam = cv2.VideoCapture(0)

# set webcam capture resolution
def change_res(width, height):
    webcam.set(3, width)
    webcam.set(4, height)

change_res(1280, 720)

# mp facial landmark detection
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(refine_landmarks=True)

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

            # draw face mesh
            # for faceLms in results.multi_face_landmarks:
            #     mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS)

            """ Head angle detection in relation to the camera """

            head.calcAngles(frame, landmarks, visualize=False)

            # draw values of roll, yaw and pitch angles
            cv2.putText(frame, "roll: " + str(head.roll), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "yaw: " + str(head.yaw), (50, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "pitch: " + str(head.pitch), (50, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Set pupil centers as iris centers from mediapipe landmarks """

            left_eye.setPupil([landmarks[473].x*frame.shape[1], landmarks[473].y*frame.shape[0]])
            right_eye.setPupil([landmarks[468].x*frame.shape[1], landmarks[468].y*frame.shape[0]])

            # draw smoothed pupil centers on the frame
            cv2.circle(frame, (int(left_eye.avg_coords[0]), int(left_eye.avg_coords[1])), 1, (0, 0, 255), 2)
            cv2.circle(frame, (int(right_eye.avg_coords[0]), int(right_eye.avg_coords[1])), 1, (0, 0, 255), 2)


            """ Blink detection """

            left_eye.detectBlink([landmarks[362], landmarks[263], landmarks[386], landmarks[374]])
            right_eye.detectBlink([landmarks[33], landmarks[133], landmarks[159], landmarks[145]]) 
        
            # draw text if blinking yes/no
            if(left_eye.opened == True and right_eye.opened == True):
                blink = "no"
            else: 
                blink = "yes"

            cv2.putText(frame, "blinking: " + blink, (50, 140), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Estimate distance from camera """

            head.calcDistance(landmarks)
            cv2.putText(frame, "camera distance: " + str(head.camera_distance), (50, 170), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Calculate middle of the eyes """

            left_eye.calcMiddle(frame, [(landmarks[362].x, landmarks[362].y), (landmarks[263].x, landmarks[263].y)])
            right_eye.calcMiddle(frame, [(landmarks[133].x, landmarks[133].y), (landmarks[33].x, landmarks[33].y)])
            
            # draw eye middle points on the frame
            cv2.circle(frame, (int(left_eye.avg_middle[0]), int(left_eye.avg_middle[1])), 1, (255, 0, 0), 2)
            cv2.circle(frame, (int(right_eye.avg_middle[0]), int(right_eye.avg_middle[1])), 1, (255, 0, 0), 2)


            """ Calculate sight angles """

            left_eye.calcAngle()
            right_eye.calcAngle()

            cv2.putText(frame, "right eye angle x: " + str(right_eye.sight_angle[0]), (50, 230), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "right eye angle y: " + str(right_eye.sight_angle[1]), (50, 260), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Move cursor """
            cursor_x = right_eye.avg_cursor[0]
            cursor_y = right_eye.avg_cursor[1]

            # draw cursor coordinates
            cv2.putText(frame, "cursor x: " + str(cursor_x), (50, 290), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "cursor y: " + str(cursor_y), (50, 320), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) 

            # edge cases
            width, height = autopy.screen.size()

            if(cursor_x < 0.0):
                cursor_x = 0.0
            if (cursor_x >= width):
                cursor_x = width-1
            if(cursor_y < 0.0):
                cursor_y = 0.0
            if (cursor_y >= height):
                cursor_y = height-1
            
            autopy.mouse.move(cursor_x, cursor_y)
    
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # esc key to exit
        break
