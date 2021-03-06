from lines import *
import math

class Head:

    camera_distance = 0             # estimated distance change from the camera
    eyes_distance = 0               # normalized distance between eyes

    def calcDistance(self, landmarks):
        """ Estimates change in distance of a person from camera """

        # Landmark points needed for calculation
        r_eye = (landmarks[133].x, landmarks[133].y, landmarks[133].z)      # right eye corner point
        l_eye = (landmarks[362].x, landmarks[362].y, landmarks[362].z)      # left eye corner point

        # Distance between eyes
        dist = lineLength(r_eye, l_eye)
        if (self.eyes_distance == 0):
            self.eyes_distance = dist
            self.camera_distance = 1
        else:    
            self.camera_distance = self.eyes_distance / dist * self.camera_distance
            self.eyes_distance = dist


    def calcAngles(self, landmarks):
        """ Calculates head position angles in 3D space relative to the camera """

        # Landmark points needed for calculation
        r_eye = (landmarks[33].x, landmarks[33].y, landmarks[33].z)     # right eye corner point
        l_eye = (landmarks[263].x, landmarks[263].y, landmarks[263].z)  # left eye corner point
        b_nose = [(landmarks[64].x+landmarks[294].x)/2, \
                (landmarks[64].y+landmarks[294].y)/2, \
                    (landmarks[64].z+landmarks[294].z)/2 ]              # mean point from two symmetric nose wings landmarks
        t_nose = [landmarks[1].x, landmarks[1].y, landmarks[1].z]       # nose tip point

        # Line lengths
        eyes_len = lineLength(r_eye, l_eye)
        nose_len = lineLength(b_nose, t_nose)

        # Angle calculations
        self.roll = math.asin((r_eye[1] - l_eye[1]) / eyes_len) * 180 / math.pi
        self.yaw = math.asin((b_nose[0] - t_nose[0]) / nose_len) * 180 / math.pi
        self.pitch = math.asin((b_nose[1] - t_nose[1]) / nose_len) * 180 / math.pi
