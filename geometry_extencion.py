from extencions import Dot
import numpy as np
from math import sqrt, pow
from plane import Plane


# Dot projection on plane computing part
def getDotProjectionOnPlane(dot_A: Dot, plane: Plane):
    """ Get dot_A projection on given plane,
        using cramer method to solve linear equations """
    x, y, z = cramerMethod(dot_A, plane.a, plane.b, plane.c, plane.d)
    return Dot(x, y, z)


def cramerMethod(dot_A: Dot, a, b, c, d):
    """ Cramer method to solve linear equations """
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

    x, y, z = det_Ai / det_A, det_Aj / det_A, det_Ak / det_A
    return x, y, z


# Dot projection on line computing part
def getDotProjectionOnLine(dot_A: Dot, dot_line_a, dot_line_b):
    """ Get dot_A projection on a line, defined by dot_line_a and dot_line_b """
    a_top, a_bot, b_top, b_bot, c_top, c_bot = computeLineCoefficients(dot_line_a, dot_line_b)
    x, y, z = dotProjectionOnLine(dot_A, a_top, a_bot, b_top, b_bot, c_top, c_bot)
    return Dot(x, y, z)


def dotProjectionOnLine(dot_A: Dot, a_top, a_bot, b_top, b_bot, c_top, c_bot):
    """ Get coordinates of a dot_A projection on a line, given by top-bot coefficients"""
    pl = Plane()
    pl.computePlaneCoefficientsWithNormalVector(dot_A, a_bot, b_bot, c_bot)

    a, b, c, d = pl.a, pl.b, pl.c, pl.d
    # a*-a_top + a*a_bot*lam + b*-b_top + b*b_bot*lam + c*-c_top + c*c_bot*lam + d=0
    lam = (a * a_top + b * b_top + c * c_top - d) / (a * a_bot + b * b_bot + c * c_bot)
    x = -1 * a_top + a_bot * lam
    y = -1 * b_top + b_bot * lam
    z = -1 * c_top + c_bot * lam
    return x, y, z


# Line computing part
def computeLineCoefficients(dot_A: Dot, dot_B: Dot):
    """ Compute line equation in (x-x1)/(x2-x1) = (y-y1)/(y2-y1) = (z-z1)/(z2-z1) format, where:
        -x1 = a_top, x2-x1 = a_bot etc. """
    a_top, a_bot = -1 * dot_A.x, dot_B.x - dot_A.x
    b_top, b_bot = -1 * dot_A.y, dot_B.y - dot_A.y
    c_top, c_bot = -1 * dot_A.z, dot_B.z - dot_A.z
    return a_top, a_bot, b_top, b_bot, c_top, c_bot


def getDistanceBetweenDots(dot_A: Dot, dot_B: Dot):
    """ Calculate euclidean distance between dot_A and dot_B in 3-dimensional space """
    return sqrt(pow(dot_B.x - dot_A.x, 2) + pow(dot_B.y - dot_A.y, 2) + pow(dot_B.z - dot_A.z, 2))
