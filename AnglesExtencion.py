import math

import numpy as np

from DataClasses import Dot
from mediapipe.python.solutions.hands import HandLandmark as HL


def getAngles(dots):
    thumb_1, _, thumb_3 = computeAnglesForFinger(dots.landmark[HL.WRIST],
                                                 dots.landmark[HL.THUMB_CMC],
                                                 dots.landmark[HL.THUMB_MCP],
                                                 dots.landmark[HL.THUMB_IP],
                                                 dots.landmark[HL.THUMB_TIP])

    index_finger_1, index_finger_2, _ = computeAnglesForFinger(dots.landmark[HL.WRIST],
                                                               dots.landmark[HL.INDEX_FINGER_MCP],
                                                               dots.landmark[HL.INDEX_FINGER_PIP],
                                                               dots.landmark[HL.INDEX_FINGER_DIP],
                                                               dots.landmark[HL.INDEX_FINGER_TIP])

    middle_finger_1, middle_finger_2, _ = computeAnglesForFinger(dots.landmark[HL.WRIST],
                                                                 dots.landmark[HL.MIDDLE_FINGER_MCP],
                                                                 dots.landmark[HL.MIDDLE_FINGER_PIP],
                                                                 dots.landmark[HL.MIDDLE_FINGER_DIP],
                                                                 dots.landmark[HL.MIDDLE_FINGER_TIP])

    ring_finger_1, ring_finger_2, _ = computeAnglesForFinger(dots.landmark[HL.WRIST],
                                                             dots.landmark[HL.RING_FINGER_MCP],
                                                             dots.landmark[HL.RING_FINGER_PIP],
                                                             dots.landmark[HL.RING_FINGER_DIP],
                                                             dots.landmark[HL.RING_FINGER_TIP])

    pinky_1, pinky_2, _ = computeAnglesForFinger(dots.landmark[HL.WRIST],
                                                 dots.landmark[HL.PINKY_MCP],
                                                 dots.landmark[HL.PINKY_PIP],
                                                 dots.landmark[HL.PINKY_DIP],
                                                 dots.landmark[HL.PINKY_TIP])

    return [thumb_1, thumb_3,
            index_finger_1, index_finger_2,
            middle_finger_1, middle_finger_2,
            ring_finger_1, ring_finger_2,
            pinky_1, pinky_2]


def computeAnglesForFinger(dot_A, dot_B, dot_C, dot_D, dot_E):
    vec_AB = computeVector(dot_A, dot_B)
    vec_BC = computeVector(dot_B, dot_C)
    vec_CD = computeVector(dot_C, dot_D)
    vec_DE = computeVector(dot_D, dot_E)

    vec_AB_length = vectorLength(vec_AB)
    vec_BC_length = vectorLength(vec_BC)
    vec_CD_length = vectorLength(vec_CD)
    vec_DE_length = vectorLength(vec_DE)

    angle_1 = math.acos(-vectorsMultiplication(vec_AB, vec_BC) / (vec_AB_length * vec_BC_length))
    angle_2 = math.acos(-vectorsMultiplication(vec_BC, vec_CD) / (vec_BC_length * vec_CD_length))
    angle_3 = math.acos(-vectorsMultiplication(vec_CD, vec_DE) / (vec_CD_length * vec_DE_length))

    # print("Angle 1:", (angle_1 * 180) / math.pi, "Cos 1:", vectorsMultiplication(vec_AB, vec_BC) / (vec_AB_length * vec_BC_length))
    # print("Angle 2:", (angle_2 * 180) / math.pi, "Cos 2:", vectorsMultiplication(vec_BC, vec_CD) / (vec_BC_length * vec_CD_length))
    # print("Angle 3:", (angle_3 * 180) / math.pi, "Cos 3:", vectorsMultiplication(vec_CD, vec_DE) / (vec_CD_length * vec_DE_length))

    return angle_1, angle_2, angle_3


def computeVector(dot_A, dot_B):
    return dot_B.x - dot_A.x, dot_B.y - dot_A.y, dot_B.z - dot_A.z


def vectorsMultiplication(vec_AB, vec_BC):
    return vec_AB[0]*vec_BC[0] + vec_AB[1]*vec_BC[1] + vec_AB[2]*vec_BC[2]


def vectorLength(vec):
    return math.sqrt(math.pow(vec[0], 2) + math.pow(vec[1], 2) + math.pow(vec[2], 2))
