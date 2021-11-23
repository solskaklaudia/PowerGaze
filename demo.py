import cv2
import mediapipe as mp
from Eye import *
from Head import *
from Cursor import *
import autopy
from subprocess import Popen
import time

webcam = cv2.VideoCapture(0)

# Set webcam capture resolution
def changeRes(width, height):
    webcam.set(3, width)
    webcam.set(4, height)

changeRes(1280, 720)

# MediaPipe facial landmark detection
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(refine_landmarks=True)

# Create objects
head = Head()
left_eye = Eye("left")
right_eye = Eye("right")
cursor = Cursor()

functions_menu = None
mouse_menu = None
keyboard_opened = False

# Calibration variables
calibrated = False
calibration_finished = False
offset = 4 

p1r, p2r, p3r, p4r, p5r, p6r, p7r, p8r, p9r = ([] for i in range(9))
p1l, p2l, p3l, p4l, p5l, p6l, p7l, p8l, p9l = ([] for i in range(9))

screen_width, screen_height = autopy.screen.size()

margin = 0.15 * screen_height

Eye.screen_px_matrix = [[[margin,margin],[screen_width/2,margin],[screen_width-margin,margin]],
                        [[margin,screen_height/2],[screen_width/2,screen_height/2],[screen_width-margin,screen_height/2]],
                        [[margin,screen_height-margin],[screen_width/2, screen_height-margin],[screen_width-margin, screen_height-margin]]]

# Counters
top_counter = 0
bottom_counter = 0
left_counter = 0
right_counter = 0
                   

while True:

    # Read new frame from the webcam
    _, frame = webcam.read()

    # MediaPipe facial landmark detection
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:

        # Get one face only
        landmarks = results.multi_face_landmarks[0].landmark

        if(landmarks):

            # Draw face mesh
            # for faceLms in results.multi_face_landmarks:
            #     mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS)


            """ Calculate head and sight parameters """

            # Head angle detection in relation to the camera
            head.calcAngles(frame, landmarks, visualize=False)

            # Set pupil centers as iris centers from mediapipe landmarks
            left_eye.setPupil([landmarks[473].x*frame.shape[1], landmarks[473].y*frame.shape[0]])
            right_eye.setPupil([landmarks[468].x*frame.shape[1], landmarks[468].y*frame.shape[0]])

            # Blink detection
            left_eye.detectBlink([landmarks[362], landmarks[263], landmarks[386], landmarks[374]])
            right_eye.detectBlink([landmarks[33], landmarks[133], landmarks[159], landmarks[145]]) 

            # Estimate change in distance from camera
            head.calcDistance(landmarks)
            
            # Calculate middle of the eyes
            left_eye.calcMiddle(frame, [(landmarks[362].x, landmarks[362].y), (landmarks[263].x, landmarks[263].y)])
            right_eye.calcMiddle(frame, [(landmarks[133].x, landmarks[133].y), (landmarks[33].x, landmarks[33].y)])

            # Calculate sight angles
            left_eye.calcAngle()
            right_eye.calcAngle()

            # Estimate cursor position
            left_eye.calcCursorPos()
            right_eye.calcCursorPos()


            """ Calibration """

            if(calibrated == False):
                Popen('python calibration.py')
                calibration_start = time.time()
                calibrated = True

            t = time.time() - calibration_start

            if(int(t) == offset+1):
                p1r.append(right_eye.sight_angle.copy())
                p1l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+3):
                p2r.append(right_eye.sight_angle.copy())
                p2l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+5):
                p3r.append(right_eye.sight_angle.copy())
                p3l.append(left_eye.sight_angle.copy())

            elif(int(t) == offset+7):
                p4r.append(right_eye.sight_angle.copy())
                p4l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+9):
                p5r.append(right_eye.sight_angle.copy())
                p5l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+11):
                p6r.append(right_eye.sight_angle.copy())
                p6l.append(left_eye.sight_angle.copy())

            elif(int(t) == offset+13):
                p7r.append(right_eye.sight_angle.copy())
                p7l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+15):
                p8r.append(right_eye.sight_angle.copy())
                p8l.append(left_eye.sight_angle.copy())
            elif(int(t) == offset+17):
                p9r.append(right_eye.sight_angle.copy())
                p9l.append(left_eye.sight_angle.copy())
            

            if(t > offset+21 and calibration_finished == False):

                right_eye.calibrate(p1r, p2r, p3r, p4r, p5r, p6r, p7r, p8r, p9r)
                left_eye.calibrate(p1l, p2l, p3l, p4l, p5l, p6l, p7l, p8l, p9l)

                calibration_finished = True


            """ Move cursor when calibration is finished """

            if(calibration_finished == True):

                cursor_x = (right_eye.avg_cursor[0] + left_eye.avg_cursor[0]) / 2
                cursor_y = (right_eye.avg_cursor[1] + left_eye.avg_cursor[1]) / 2

                cursor.setCursorPosition(cursor_x, cursor_y, screen_width, screen_height)

                # Perform a left mouse button click if cursor is stationary for long enough
                # and is located roughly on the screen area
                cursor.stationary_counter += 1
                if(cursor.stationary_counter > 30 
                and cursor_x > 0-100 and cursor_x < screen_width+100 and cursor_y > 0-100 and cursor_y < screen_height+100):
                    autopy.mouse.click()
                    cursor.stationary_counter = 0

                # Open functions menu if looking below the screen for long enough
                if(cursor_y > screen_height+200 and cursor_x > 0 and cursor_x < screen_width):  
                    
                    bottom_counter += 1
                
                    if(bottom_counter == 30):      
                        if(functions_menu is None):
                            functions_menu = Popen('python functions_menu.py')
                        else:
                            poll = functions_menu.poll()
                            if(poll is not None):
                                functions_menu = Popen('python functions_menu.py')
                    
                    elif(bottom_counter > 30):
                        bottom_counter = 0
                else:
                    bottom_counter = 0

                # Open mouse menu if looking above the screen for long enough
                if(cursor_y < 0-200 and cursor_x > 0.1*screen_width and cursor_x < 0.9*screen_width):   

                    top_counter += 1
                    
                    if(top_counter == 30):     
                        if(mouse_menu is None):
                            mouse_menu = Popen('python mouse_menu.py')
                        else:
                            poll = mouse_menu.poll()
                            if(poll is not None):
                                mouse_menu = Popen('python mouse_menu.py')

                    elif(top_counter > 30):
                        top_counter = 0
                else:
                    top_counter = 0

                # Open or close keyboard if looking to the left of the screen for long enough
                if(cursor_x < 0-200 and cursor_y > 0.1*screen_height and cursor_y < 0.9*screen_height):   

                    left_counter += 1

                    if(left_counter == 30):
                        if(keyboard_opened == False):                               
                            Popen("osk.exe", shell = True)
                            keyboard_opened = True
                        else:
                            Popen("wmic process where name='osk.exe' delete", shell = True)
                            keyboard_opened = False 
                    
                    elif(left_counter > 30):
                        left_counter = 0
                else:
                    left_counter = 0

                # Redo calibration if looking to the right of the screen for long enough
                if(cursor_x > screen_width+200 and cursor_y > 0.1*screen_height and cursor_y < 0.9*screen_height): 

                    right_counter += 1

                    if(right_counter == 30):
                        calibrated = False
                        calibration_finished = False
                        p1r, p2r, p3r, p4r, p5r, p6r, p7r, p8r, p9r = ([] for i in range(9))
                        p1l, p2l, p3l, p4l, p5l, p6l, p7l, p8l, p9l = ([] for i in range(9))

                    elif(right_counter > 30):
                        right_counter = 0
                        
                else:
                    right_counter = 0

                autopy.mouse.move(cursor.coordinates[0], cursor.coordinates[1])
            

            """ Draw calculated values on frame """

            # draw smoothed pupil centers on the frame
            cv2.circle(frame, (int(left_eye.avg_coords[0]), int(left_eye.avg_coords[1])), 1, (0, 0, 255), 2)
            cv2.circle(frame, (int(right_eye.avg_coords[0]), int(right_eye.avg_coords[1])), 1, (0, 0, 255), 2)

            # draw eye middle points on the frame
            cv2.circle(frame, (int(left_eye.avg_middle[0]), int(left_eye.avg_middle[1])), 1, (255, 0, 0), 2)
            cv2.circle(frame, (int(right_eye.avg_middle[0]), int(right_eye.avg_middle[1])), 1, (255, 0, 0), 2)

            # draw values of roll, yaw and pitch angles
            cv2.putText(frame, "roll: " + str(head.roll), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "yaw: " + str(head.yaw), (50, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "pitch: " + str(head.pitch), (50, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # draw estimated camera distance change
            cv2.putText(frame, "camera distance: " + str(head.camera_distance), (50, 170), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # draw text if blinking yes/no
            if(left_eye.opened == True and right_eye.opened == True):
                blink = "no"
            else: 
                blink = "yes"

            cv2.putText(frame, "blinking: " + blink, (50, 140), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # draw sight angles values
            cv2.putText(frame, "right eye angle x: " + str(right_eye.sight_angle[0]), (50, 230), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "right eye angle y: " + str(right_eye.sight_angle[1]), (50, 260), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "left eye angle x: " + str(left_eye.sight_angle[0]), (50, 290), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "left eye angle y: " + str(left_eye.sight_angle[1]), (50, 320), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # draw cursor coordinates
            cv2.putText(frame, "cursor x: " + str(cursor.coordinates[0]), (50, 350), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "cursor y: " + str(cursor.coordinates[1]), (50, 380), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) 

    
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:  # esc key to exit
        break
