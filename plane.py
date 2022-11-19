import typing
import numpy as np
from math import sqrt, pow


class Dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Plane:
    def __init__(self, dot_wrist, dot_index_mcp, dot_pinky_mcp):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.computePlaneCoefficents(dot_wrist, dot_index_mcp, dot_pinky_mcp)

    def computePlaneCoefficents(self, dot_wrist, dot_index_mcp, dot_pinky_mcp):
        c1 = np.linalg.det(np.array([
            [dot_index_mcp.y - dot_wrist.y, dot_pinky_mcp.y - dot_wrist.y],
            [dot_index_mcp.z - dot_wrist.z, dot_pinky_mcp.z - dot_wrist.z]
        ]))
        c2 = np.linalg.det(np.array([
            [dot_index_mcp.x - dot_wrist.x, dot_pinky_mcp.x - dot_wrist.x],
            [dot_index_mcp.z - dot_wrist.z, dot_pinky_mcp.z - dot_wrist.z]
        ]))
        c3 = np.linalg.det(np.array([
            [dot_index_mcp.x - dot_wrist.x, dot_pinky_mcp.x - dot_wrist.x],
            [dot_index_mcp.y - dot_wrist.y, dot_pinky_mcp.y - dot_wrist.y]
        ]))

        self.a = c1
        self.b = -1 * c2
        self.c = c3
        self.d = c1 * (- dot_wrist.x) - c2 * (- dot_wrist.y) + c3 * (- dot_wrist.z)

    def getDotProjectionOnPlane(self, dot_A):
        x, y, z = self.cramerMethod(dot_A)
        return Dot(x, y, z)

    def cramerMethod(self, dot_A):
        a_normal_to_plane = np.array([self.a, self.b, self.c])

        det_A = np.linalg.det(np.array([
            [a_normal_to_plane[1], -1 * a_normal_to_plane[0], 0],
            [a_normal_to_plane[2], 0, -1 * a_normal_to_plane[0]],
            [self.a, self.b, self.c]
        ]))

        free_coefficent_1 = dot_A.x * a_normal_to_plane[1] - dot_A.y * a_normal_to_plane[0]
        free_coefficent_2 = dot_A.x * a_normal_to_plane[2] - dot_A.z * a_normal_to_plane[0]
        free_coefficent_3 = -1 * self.d

        det_Ai = np.linalg.det(np.array([
            [free_coefficent_1, -1 * a_normal_to_plane[0], 0],
            [free_coefficent_2, 0, -1 * a_normal_to_plane[0]],
            [free_coefficent_3, self.b, self.c]
        ]))

        det_Aj = np.linalg.det(np.array([
            [a_normal_to_plane[1], free_coefficent_1, 0],
            [a_normal_to_plane[2], free_coefficent_2, -1 * a_normal_to_plane[0]],
            [self.a, free_coefficent_3, self.c]
        ]))

        det_Ak = np.linalg.det(np.array([
            [a_normal_to_plane[1], -1 * a_normal_to_plane[0], free_coefficent_1],
            [a_normal_to_plane[2], 0, free_coefficent_2],
            [self.a, self.b, free_coefficent_3]
        ]))

        return det_Ai / det_A, det_Aj / det_A, det_Ak / det_A

    def getLengthBetweenDots(self, dot_A, dot_B):
        return sqrt(pow(dot_B.x - dot_A.x, 2) + pow(dot_B.y - dot_A.y, 2) + pow(dot_B.z - dot_A.z, 2))

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"
