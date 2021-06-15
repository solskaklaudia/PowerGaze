from Lines import *
import math

def calcAngles(frame, landmarks, visualize = False):

    # landmark points needed for calculation
    r_eye = (landmarks[33].x, landmarks[33].y, landmarks[33].z) # right eye corner point
    l_eye = (landmarks[263].x, landmarks[263].y, landmarks[263].z) # left eye corner point
    b_nose = [(landmarks[64].x+landmarks[294].x)/2, \
            (landmarks[64].y+landmarks[294].y)/2, \
                (landmarks[64].z+landmarks[294].z)/2 ] # mean point from two symmetric nose wings landmarks
    t_nose = [landmarks[1].x, landmarks[1].y, landmarks[1].z] # nose tip point

    # line lengths
    eyes_len = lineLength(r_eye, l_eye)
    nose_len = lineLength(b_nose, t_nose)

    #angle calculations
    roll = math.asin((r_eye[1] - l_eye[1]) / eyes_len) * 180 / math.pi
    yaw = math.asin((b_nose[0] - t_nose[0]) / nose_len) * 180 / math.pi
    pitch = math.asin((b_nose[1] - t_nose[1]) / nose_len) * 180 / math.pi

    if(visualize):
        drawLine(frame, r_eye, l_eye) # drawing line connecting eyes
        drawLine(frame,b_nose, t_nose, color = (255,0,255)) # drawing nose line

    return roll, yaw, pitch