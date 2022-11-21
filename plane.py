import typing
import numpy as np
from math import sqrt, pow, cos


class Dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class Plane:
    def __init__(self, dot_wrist, dot_index_mcp, dot_pinky_mcp):
        self.dot_wrist = dot_wrist
        self.dot_index_mcp = dot_index_mcp
        self.dot_pinky_mcp = dot_pinky_mcp

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

        self.a, self.b, self.c, self.d = self.computePlaneCoefficents(dot_wrist, dot_index_mcp, dot_pinky_mcp)

    def computeXYZofDot(self):
        ...

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

        a = c1
        b = -1 * c2
        c = c3
        d = c1 * (- dot_wrist.x) - c2 * (- dot_wrist.y) + c3 * (- dot_wrist.z)
        return a, b, c, d


    def getDotProjectionOnPlane(self, dot_A, a, b, c, d):
        x, y, z = self.cramerMethod(dot_A, a, b, c, d)
        return Dot(x, y, z)


    def getDotProjectionOnLine(self, dot_A, dot_line_a, dot_line_b):
        a_top, a_bot, b_top , b_bot, c_top, c_bot = self.computeLineCoefficents(dot_line_a, dot_line_b)
        print(a_top, a_bot, b_top , b_bot, c_top, c_bot)
        x, y, z = self.dotProjectionOnLine(dot_A, a_top, a_bot, b_top , b_bot, c_top, c_bot)
        return Dot(x, y, z)

    def computeLineCoefficents(self, dot_A, dot_B):
        return -1 * dot_A.x, dot_B.x - dot_A.x, -1 * dot_A.y, dot_B.y - dot_A.y, -1 * dot_A.z, dot_B.z - dot_A.z

    def dotProjectionOnLine(self, dot_A, a_top, a_bot, b_top , b_bot, c_top, c_bot):
        normal_vector = np.array([a_bot, b_bot, c_bot])
        a = normal_vector[0]
        b = normal_vector[1]
        c = normal_vector[2]
        d = -1 * dot_A.x * normal_vector[0] + -1 * dot_A.y * normal_vector[1] + -1 * dot_A.z * normal_vector[2]
        # a*-a_top + a*a_bot*lam + b*-b_top + b*b_bot*lam + c*-c_top + c*c_bot*lam + d=0
        lam = (a * a_top + b * b_top + c * c_top - d)/(a * a_bot + b * b_bot + c * c_bot)
        x = -1 * a_top + a_bot * lam
        y = -1 * b_top + b_bot * lam
        z = -1 * c_top + c_bot * lam
        return x, y, z


    def cramerMethod(self, dot_A, a, b, c, d):
        a_normal_to_plane = np.array([a, b, c])

        det_A = np.linalg.det(np.array([
            [a_normal_to_plane[1], -1 * a_normal_to_plane[0], 0],
            [a_normal_to_plane[2], 0, -1 * a_normal_to_plane[0]],
            [a, b, c]
        ]))

        free_coefficent_1 = dot_A.x * a_normal_to_plane[1] - dot_A.y * a_normal_to_plane[0]
        free_coefficent_2 = dot_A.x * a_normal_to_plane[2] - dot_A.z * a_normal_to_plane[0]
        free_coefficent_3 = -1 * d

        det_Ai = np.linalg.det(np.array([
            [free_coefficent_1, -1 * a_normal_to_plane[0], 0],
            [free_coefficent_2, 0, -1 * a_normal_to_plane[0]],
            [free_coefficent_3, b, c]
        ]))

        det_Aj = np.linalg.det(np.array([
            [a_normal_to_plane[1], free_coefficent_1, 0],
            [a_normal_to_plane[2], free_coefficent_2, -1 * a_normal_to_plane[0]],
            [a, free_coefficent_3, c]
        ]))

        det_Ak = np.linalg.det(np.array([
            [a_normal_to_plane[1], -1 * a_normal_to_plane[0], free_coefficent_1],
            [a_normal_to_plane[2], 0, free_coefficent_2],
            [a, b, free_coefficent_3]
        ]))

        return det_Ai / det_A, det_Aj / det_A, det_Ak / det_A


    def getLengthBetweenDots(self, dot_A, dot_B):
        return sqrt(pow(dot_B.x - dot_A.x, 2) + pow(dot_B.y - dot_A.y, 2) + pow(dot_B.z - dot_A.z, 2))

    # def cosAngle(self):
    #     cos((pow(0.5, 2) + pow(0.7, 2) + pow(0.35, 2)) / 2 * 0.5 * 0.7)

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"
