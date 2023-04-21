def getGesture(angles: list):
    current_gesture = 0

    if angles[1] < 2:
        current_gesture = 1

    if angles[3] < 2:
        current_gesture = 2

    if angles[5] < 2:
        current_gesture = 3

    if angles[9] < 2:
        current_gesture = 4

    return current_gesture
