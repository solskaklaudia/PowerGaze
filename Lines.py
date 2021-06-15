import cv2
import math

def drawLine(frame, pt1, pt2, color = (255,0,0)):
    cv2.line(frame, (int(pt1[0]*frame.shape[1]),int(pt1[1]*frame.shape[0])), (int(pt2[0]*frame.shape[1]),int(pt2[1]*frame.shape[0])), color, 2)

def lineLength(pt1, pt2):
    len = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)
    return len 