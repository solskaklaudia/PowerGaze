import numpy as np

class Eye:
    
    pupil_coords = [[50],[50]]
    avg_coords = [50,50]
    max_samples = 5

    def __init__(self,name,landmarks):

        self.name = name
        self.landmarks = landmarks

    def average(self, cent):

        x = cent[0]
        y = cent[1]
         
        # smoothing the movement with moving average
        self.pupil_coords[0].append(x)
        self.pupil_coords[1].append(y)

        if len(self.pupil_coords[0]) == self.max_samples:
            self.pupil_coords[0].pop(0)
            self.pupil_coords[1].pop(0)

        self.avg_coords[0] = int(np.mean(self.pupil_coords[0]))
        self.avg_coords[1] = int(np.mean(self.pupil_coords[1]))
