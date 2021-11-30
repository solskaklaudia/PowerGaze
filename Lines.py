import math

def lineLength(pt1, pt2):
    """ Calculates length between two points """
    len = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)
    return len 