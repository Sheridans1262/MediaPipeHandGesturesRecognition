import typing
import numpy as np
from math import sqrt, pow
from extencions import Dot


class Plane:
    def __init__(self, dot_wrist: Dot, dot_index_mcp: Dot, dot_pinky_mcp: Dot):
        self.dot_wrist = dot_wrist
        self.dot_index_mcp = dot_index_mcp
        self.dot_pinky_mcp = dot_pinky_mcp

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

        self.a, self.b, self.c, self.d = self.computePlaneCoefficientsWithThreeDots(dot_wrist, dot_index_mcp, dot_pinky_mcp)

    def computeXYZofDot(self):
        ...

# Plane computing part
    def computePlaneCoefficientsWithThreeDots(self, dot_A: Dot, dot_B: Dot, dot_C: Dot):
        """ Compute plane equation Ax+By+Cz+D=0 coefficients by given 3 dots """
        c1 = np.linalg.det(np.array([
            [dot_B.y - dot_A.y, dot_C.y - dot_A.y],
            [dot_B.z - dot_A.z, dot_C.z - dot_A.z]
        ]))
        c2 = np.linalg.det(np.array([
            [dot_B.x - dot_A.x, dot_C.x - dot_A.x],
            [dot_B.z - dot_A.z, dot_C.z - dot_A.z]
        ]))
        c3 = np.linalg.det(np.array([
            [dot_B.x - dot_A.x, dot_C.x - dot_A.x],
            [dot_B.y - dot_A.y, dot_C.y - dot_A.y]
        ]))

        a = c1
        b = -1 * c2
        c = c3
        d = c1 * (- dot_A.x) - c2 * (- dot_A.y) + c3 * (- dot_A.z)
        return a, b, c, d

    def getPlaneEquation(self, dot_A: Dot, a, b, c, d):
        """ Get number, which represents position of dot related to given plane:
            positive/negative number - dot is on one of the sides of a plane,
            zero - dot belongs to a plane """
        return dot_A.x * a + dot_A.y * b + dot_A.z * c + d

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"
