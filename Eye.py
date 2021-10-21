from lines import *

class Eye:

    max_samples = 5                 # max amount of pupil coordinates samples for smoothing

    def __init__(self,name):

        self.name = name
        self.pupil_coords = []       # array of calculated raw pupil coordinates (x,y)
        self.avg_coords = [0,0]      # averaged out pupil coordinates for smoother movement


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


    def getEye(self, frame):
        """ Gets eye image using eye landmarks, converts to grayscale and equalizes its histogram """

        y1 = int(min(self.landmarks[1]) * frame.shape[0])
        y2 = int(max(self.landmarks[1]) * frame.shape[0])
        x1 = int(min(self.landmarks[0]) * frame.shape[1])
        x2 = int(max(self.landmarks[0]) * frame.shape[1])

        self.roi_pos = ((x1, y1), (x2, y2))

        image = frame[y1:y2, x1:x2]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = hsv[:,:,2]

        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        gray = cv2.equalizeHist(gray)

        gray = cv2.resize(gray, (150,100), interpolation = cv2.INTER_LINEAR)

        self.eye_image = gray

    
    def findPupil(self, show = True):
        """ Finds pupil center coordinates (x,y) """

        threshold_p = 10
        
        _, binarized_p = cv2.threshold(self.eye_image, threshold_p, 255, cv2.THRESH_BINARY_INV)

        # morphological opening to get rid of noise
        gray = cv2.morphologyEx(binarized_p, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
        
        # find most external contours
        cnts, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if cnts:

            if len(cnts) > 1:
                # find contour centers
                cnt_centers = []

                for c in cnts :
                    cX, cY = c.mean(axis=0)[0]
                    cnt_centers.append((cX, cY))

                # find contour closest to the image center
                img_center = [75, 50]
                min_dist_cnt = [cnts[0], 200]

                for i in range(len(cnt_centers)):
                    dist = (img_center[0] - cnt_centers[i][0])**2 + (img_center[1] - cnt_centers[i][1])**2
                    if (dist < min_dist_cnt[1]):
                        min_dist_cnt = [cnts[i], dist]

                c = min_dist_cnt[0]

            else:
                c = cnts[0]
        
            # fit an ellipse
            result = self.eye_image.copy()
            ((centx,centy), (width,height), angle) = cv2.fitEllipse(c)
            res = cv2.ellipse(result, (int(centx),int(centy)), (int(width/2),int(height/2)), angle, 0, 360, (255,255,255), 1)

            # calculate pupil coordinates in original frame
            self.pup_x = self.roi_pos[0][0] + (centx/150 * (self.roi_pos[1][0]-self.roi_pos[0][0]))
            self.pup_y = self.roi_pos[0][1] + (centy/100 * (self.roi_pos[1][1]-self.roi_pos[0][1]))


            self.smoothPupilMovement([self.pup_x, self.pup_y])

            # display eye and predicted pupil
            if(show):
                cv2.imshow("Eye " + self.name, res)
                cv2.imshow("Pupil " + self.name, gray)


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

       