from lines import *
import numpy as np
import cv2

class Eye:

    max_samples = 5                 # max amount of pupil coordinates samples for smoothing
    sight_angle = [0,0]             # predicted angle of sight
    max_cursor_samples = 10

    def __init__(self,name):

        self.name = name
        self.pupil_coords = []       # array of calculated raw pupil coordinates (x,y)
        self.avg_coords = [0,0]      # averaged out pupil coordinates for smoother movement
        self.middle = [0,0]

        self.middle_coords = []
        self.avg_middle = [0,0]

        self.cursor_coords = []
        self.avg_cursor = [0,0]

        self.sight_angle_matrix = [[[0.62, 5.04],[3.52, 4.84],[5.28, 5.39]],
                                    [[0.74, 4.38],[3.57,3.84],[5.43, 4.26]],
                                    [[0.83, 2.61],[3.39, 2.63],[5.74, 3.68]]]

        self.screen_px_matrix = [[[128,110],[970,110],[1810,110]],
                                    [[128,550],[970,550],[1810,550]],
                                    [[128,980],[970, 980],[1810, 980]]]


    def setLandmarks(self, landmarks):
        self.landmarks = landmarks


    def smoothPupilMovement(self, c_coords):
        """ Smooths pupil movement using weighed moving average """

        self.pupil_coords.append(c_coords)

        if len(self.pupil_coords) > self.max_samples:
            self.pupil_coords.pop(0)

        avg_x = 0
        avg_y = 0
        weighs_sum = 0

        for i in range(len(self.pupil_coords)):
            avg_x += (i+1)*self.pupil_coords[i][0]
            avg_y += (i+1)*self.pupil_coords[i][1]
            weighs_sum += (i+1)

        self.avg_coords[0] = avg_x/weighs_sum
        self.avg_coords[1] = avg_y/weighs_sum

    
    def smoothMiddleMovement(self, c_coords):
        """ Smooths middle of the eye movement using weighed moving average """

        self.middle_coords.append(c_coords)

        if len(self.middle_coords) > self.max_samples:
            self.middle_coords.pop(0)

        avg_x = 0
        avg_y = 0
        weighs_sum = 0

        for i in range(len(self.middle_coords)):
            avg_x += (i+1)*self.middle_coords[i][0]
            avg_y += (i+1)*self.middle_coords[i][1]
            weighs_sum += (i+1)

        self.avg_middle[0] = avg_x/weighs_sum
        self.avg_middle[1] = avg_y/weighs_sum


    def smoothCursorMovement(self, c_coords):
        """ Smooths cursor movement using weighed moving average """

        # append the sample when less than max cursor samples and calculate average
        if len(self.cursor_coords) <= self.max_cursor_samples:
            self.cursor_coords.append(c_coords)
            avg_x = 0
            avg_y = 0
            weighs_sum = 0

            for i in range(len(self.cursor_coords)):
                avg_x += (i+1)*self.cursor_coords[i][0]
                avg_y += (i+1)*self.cursor_coords[i][1]
                weighs_sum += (i+1)

            self.avg_cursor[0] = avg_x/weighs_sum
            self.avg_cursor[1] = avg_y/weighs_sum

        # when max samples reached, accept only those which differ more than given number of pixels
        diff_x = abs(self.cursor_coords[len(self.cursor_coords)-1][0] - c_coords[0])
        diff_y = abs(self.cursor_coords[len(self.cursor_coords)-1][1] - c_coords[1])

        if(diff_x > 100 and diff_y > 100):

            self.cursor_coords.append(c_coords)

            if len(self.cursor_coords) > self.max_cursor_samples:
                self.cursor_coords.pop(0)

            avg_x = 0
            avg_y = 0
            weighs_sum = 0

            for i in range(len(self.cursor_coords)):
                avg_x += (i+1)*self.cursor_coords[i][0]
                avg_y += (i+1)*self.cursor_coords[i][1]
                weighs_sum += (i+1)

            self.avg_cursor[0] = avg_x/weighs_sum
            self.avg_cursor[1] = avg_y/weighs_sum


    def setPupil(self, point):
        """ Sets pupil center point"""
        self.smoothPupilMovement(point)
    

    def calcMiddle(self, frame, landmarks):
        """ Calculates eye middle point coordinates"""

        self.middle[0] = ((landmarks[0][0] + landmarks[1][0]) / 2 ) * frame.shape[1]
        self.middle[1] = ((landmarks[0][1] + landmarks[1][1]) / 2 ) * frame.shape[0]
        
        self.eye_width = abs(landmarks[0][0] - landmarks[1][0]) * frame.shape[1]

        self.smoothMiddleMovement(self.middle)


    def calcAngle(self):
        """ Calculates angle od the sight in x and y directions """

        # distance between middle and pupil center in x and y directions
        pup_dist_x = self.avg_middle[0] - self.avg_coords[0]
        pup_dist_y = self.avg_middle[1] - self.avg_coords[1]

        # calculates sight angle
        self.sight_angle[0] = math.atan(pup_dist_x / self.eye_width) * 180 / math.pi
        self.sight_angle[1] = math.atan(pup_dist_y / self.eye_width) * 180 / math.pi

        # calculates cursor coordinates
        train_pts = np.float32(self.screen_px_matrix).reshape(-1,1,2)
        query_pts = np.float32(self.sight_angle_matrix).reshape(-1,1,2)

        matrix, _ = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)

        pts = np.float32([self.sight_angle]).reshape(-1,1,2)

        self.cursor = cv2.perspectiveTransform(pts,matrix).flatten()
        self.smoothCursorMovement(self.cursor)


    def detectBlink(self, landmarks):
        """ Detects eye blinking using height to width ratio """

        # eye height to width ratio threshold considered as blink
        blink_ratio = 0.4

        # calculate eye width and height using eye landmarks - left corner, right corner, top, bottom
        eye_width = lineLength([(landmarks[0].x),(landmarks[0].y),(landmarks[0].z)] , [(landmarks[1].x),(landmarks[1].y),(landmarks[1].z)])
        eye_height = lineLength([(landmarks[2].x),(landmarks[2].y),(landmarks[2].z)] , [(landmarks[3].x),(landmarks[3].y),(landmarks[3].z)])

        # calculate eye height to width ratio
        eye_ratio = eye_height / eye_width

        # check for eye blinks
        if(eye_ratio <= blink_ratio):
            self.opened = False
        else:
            self.opened = True

       