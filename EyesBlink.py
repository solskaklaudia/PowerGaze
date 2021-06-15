from Lines import lineLength

def eyeRatio(l1, l2, l3, l4):
    # using eye landmarks - left corner, right corner, top, bottom
    eye_width = lineLength([(l1.x),(l1.y),(l1.z)] , [(l2.x),(l2.y),(l2.z)])
    eye_height = lineLength([(l3.x),(l3.y),(l3.z)] , [(l4.x),(l4.y),(l4.z)])

    return eye_height/eye_width


def isBlink(ratio, threshold):

    if(ratio <= threshold):
        return True
    else:
        return False


def eyesBlink(landmarks):
    """ Works poorly due to landmarks not tracking eyelids - other method shall be implemented."""
    # eye height to width ratio threshold considered as blink
    blink_ratio = 0.4

    # checking eyes height to width ratio
    r_eye_ratio = eyeRatio(landmarks[33], landmarks[133], landmarks[159], landmarks[145]) 
    l_eye_ratio = eyeRatio(landmarks[362], landmarks[263], landmarks[386], landmarks[374])

    # checks for both eye blinks
    r_blink = isBlink(r_eye_ratio, blink_ratio)
    l_blink = isBlink(l_eye_ratio, blink_ratio)

    # returns information which eye is closed
    if(not(r_blink) and not(l_blink)):
        return "none"
    elif(r_blink and l_blink):
        return "both"
    elif(r_blink):
        return "right"
    else:
        return "left"
