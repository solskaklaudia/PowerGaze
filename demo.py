import cv2
import mediapipe as mp
from Eye import *
from Head import *
from Menu import *
import autopy
from subprocess import Popen
import time
import statistics as st

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

# create objects
head = Head()
left_eye = Eye("left")
right_eye = Eye("right")
functions_menu = Menu("functions menu")

calibrated = False
calibration_finished = False

p1r, p2r, p3r, p4r, p5r, p6r, p7r, p8r, p9r = ([] for i in range(9))
p1l, p2l, p3l, p4l, p5l, p6l, p7l, p8l, p9l = ([] for i in range(9))

screen_width, screen_height = autopy.screen.size()

margin = 0.15 * screen_height

Eye.screen_px_matrix = [[[margin,margin],[screen_width/2,margin],[screen_width-margin,margin]],
                        [[margin,screen_height/2],[screen_width/2,screen_height/2],[screen_width-margin,screen_height/2]],
                        [[margin,screen_height-margin],[screen_width/2, screen_height-margin],[screen_width-margin, screen_height-margin]]]
                        

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
            cv2.putText(frame, "left eye angle x: " + str(left_eye.sight_angle[0]), (50, 290), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "left eye angle y: " + str(left_eye.sight_angle[1]), (50, 320), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


            """ Move cursor """

            cursor_x = (right_eye.avg_cursor[0] + left_eye.avg_cursor[0]) / 2
            cursor_y = (right_eye.avg_cursor[1] + left_eye.avg_cursor[1]) / 2

            # draw cursor coordinates
            cv2.putText(frame, "cursor x: " + str(cursor_x), (50, 350), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "cursor y: " + str(cursor_y), (50, 380), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) 

            # edge cases
            if(cursor_x < 0.0):
                cursor_x = 0.0
            if (cursor_x >= screen_width):
                cursor_x = screen_width-1
            if(cursor_y < 0.0):
                # if(functions_menu.visible == False):
                #     Popen('python functions_menu.py')
                #     functions_menu.visible = True
                cursor_y = 0.0
            if (cursor_y >= screen_height):
                cursor_y = screen_height-1


            """ Calibration """

            if(calibrated == False):
                Popen('python calibration.py')
                calibration_start = time.time()
                calibrated = True

            t = time.time() - calibration_start

            if(int(t) == 3):
                p1r.append(right_eye.sight_angle.copy())
                p1l.append(left_eye.sight_angle.copy())
            elif(int(t) == 5):
                p2r.append(right_eye.sight_angle.copy())
                p2l.append(left_eye.sight_angle.copy())
            elif(int(t) == 7):
                p3r.append(right_eye.sight_angle.copy())
                p3l.append(left_eye.sight_angle.copy())

            elif(int(t) == 9):
                p4r.append(right_eye.sight_angle.copy())
                p4l.append(left_eye.sight_angle.copy())
            elif(int(t) == 11):
                p5r.append(right_eye.sight_angle.copy())
                p5l.append(left_eye.sight_angle.copy())
            elif(int(t) == 13):
                p6r.append(right_eye.sight_angle.copy())
                p6l.append(left_eye.sight_angle.copy())

            elif(int(t) == 15):
                p7r.append(right_eye.sight_angle.copy())
                p7l.append(left_eye.sight_angle.copy())
            elif(int(t) == 17):
                p8r.append(right_eye.sight_angle.copy())
                p8l.append(left_eye.sight_angle.copy())
            elif(int(t) == 19):
                p9r.append(right_eye.sight_angle.copy())
                p9l.append(left_eye.sight_angle.copy())
            

            if(t > 20 and calibration_finished == False):

                right_eye.calibrate(p1r, p2r, p3r, p4r, p5r, p6r, p7r, p8r, p9r)
                left_eye.calibrate(p1l, p2l, p3l, p4l, p5l, p6l, p7l, p8l, p9l)

                print("right eye:")
                print(right_eye.sight_angle_matrix)

                print("left eye:")
                print(left_eye.sight_angle_matrix)

                calibration_finished = True

            autopy.mouse.move(cursor_x, cursor_y)
    
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # esc key to exit
        break
