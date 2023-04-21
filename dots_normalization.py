import math

import numpy as np

from extencions import Dot
from geometry_extencion import getDotProjectionOnLine, getDotProjectionOnPlane, getDistanceBetweenDots
from plane import Plane
from mediapipe.python.solutions.hands import HandLandmark as HL


def getNormalizedDots(dot_wrist, dot_index_mcp, dot_pinky_mcp,
                      dot_thumb, dot_index, dot_middle, dot_ring, dot_pinky):
    """Get new dot coordinates for thumb-pinky dots"""
    # Create main plain
    main_pl = Plane()
    main_pl.computePlaneCoefficientsWithThreeDots(dot_wrist, dot_index_mcp, dot_pinky_mcp)

    # Create "counter" plane to main plane
    counter_pl = Plane()
    pinky_mcp_projection = getDotProjectionOnLine(dot_pinky_mcp, dot_index_mcp, dot_wrist)
    counter_pl.computePlaneCoefficientsWithDotAndLine(dot_index_mcp, pinky_mcp_projection, dot_pinky_mcp)

    # Debug info
    print(f"Main plane: {main_pl}")
    print(f"Counter plane: {counter_pl}\n")
    # Debug info

    # Compute sign on left side of the counter_plane
    if counter_pl.getPlaneEquation(dot_pinky_mcp) >= 0:
        sign_on_left_side_of_counter_pl = 1
    else:
        sign_on_left_side_of_counter_pl = -1

    input_dots = [dot_thumb, dot_index, dot_middle, dot_ring, dot_pinky]
    output_dots = [None, None, None, None, None]

    # TODO: create class Line to store line coefficients,
    #       now they are computed 5 times in getProjectionOnLine function
    # Compute new coordinates of given dots
    for index, dot in enumerate(input_dots):
        print(f"Input dot: {dot}")

        projection_on_main_plane = getDotProjectionOnPlane(dot, main_pl)

        # Debug info
        print(f"Dot projection on plane: {projection_on_main_plane}")
        # Debug info

        projection_on_line = getDotProjectionOnLine(projection_on_main_plane, dot_wrist, dot_index_mcp)

        # Debug info
        print(f"Dot projection on line: {projection_on_line}")
        # Debug info

        x = getDistanceBetweenDots(dot_wrist, projection_on_line)

        y = getDistanceBetweenDots(projection_on_line, projection_on_main_plane)
        sign_of_x = counter_pl.getPlaneEquation(projection_on_main_plane)
        if sign_on_left_side_of_counter_pl * sign_of_x <= 0:
            y *= -1

        z = getDistanceBetweenDots(projection_on_main_plane, dot)

        output_dots[index] = Dot(x, y, z)

        # Debug info
        print(f"Output dot projection: {output_dots[index]}")
        # Debug info

    return output_dots


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
