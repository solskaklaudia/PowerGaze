import cv2
import numpy as np
from scipy import ndimage
from Eye import *

class Eyes:

    def __init__(self, frame, landmarks):

        self.frame = frame

        self.left_eye = Eye("left", [(landmarks[463].x, landmarks[359].x, landmarks[257].x, landmarks[253].x), \
                    (landmarks[463].y, landmarks[359].y, landmarks[257].y, landmarks[253].y)])

        self.right_eye = Eye("right", [(landmarks[130].x, landmarks[243].x, landmarks[27].x, landmarks[23].x), \
                     (landmarks[130].y, landmarks[243].y, landmarks[27].y, landmarks[23].y)])


    def getEyes(self, show=True):

        self.show = show

        self.getEye(self.left_eye)
        self.getEye(self.right_eye)


    def getEye(self, eye):

        y1 = int(min(eye.landmarks[1]) * self.frame.shape[0])
        y2 = int(max(eye.landmarks[1]) * self.frame.shape[0])
        x1 = int(min(eye.landmarks[0]) * self.frame.shape[1])
        x2 = int(max(eye.landmarks[0]) * self.frame.shape[1])

        image = self.frame[y1:y2, x1:x2]
        image = cv2.resize(image, (150,100), interpolation = cv2.INTER_LINEAR)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = hsv[:,:,2]

        gray = cv2.equalizeHist(gray)
        
        gray = cv2.medianBlur(gray, 3)          

        # pupil detection
        threshold_pupil = 5

        kernel = np.ones((5,5),np.uint8)

        imagebinary_pupil=cv2.inRange(gray, 0, threshold_pupil)

        invbinimg_pupil=cv2.bitwise_not(imagebinary_pupil)
        erosion_pupil = cv2.morphologyEx(invbinimg_pupil, cv2.MORPH_OPEN, kernel, iterations = 3) #erosion with dilation

        inv=cv2.bitwise_not(erosion_pupil)

        # Finding center of mass
        cent = ndimage.measurements.center_of_mass(inv)

        if(not np.isnan(cent[1])):
            eye.average(cent)
            cv2.circle(image, (int(eye.avg_coords[1]),int(eye.avg_coords[0])), 10, (0, 0, 255), 1)
            
            if(self.show):
                cv2.imshow("Gray " + eye.name, gray)
                cv2.imshow("Eye " + eye.name, image)
                cv2.imshow("Pupil " + eye.name, erosion_pupil)
        
        pup_x = x1 + int(eye.avg_coords[1]/150 * (x2-x1))
        pup_y = y1 + int(eye.avg_coords[0]/100 * (y2-y1))

        cv2.circle(self.frame, (pup_x,pup_y), 1, (0, 0, 255), 1)