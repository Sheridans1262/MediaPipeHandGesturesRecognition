# import numpy as np
# from DataClasses import Dot
#
#
# class Plane:
#     def __init__(self):
#         self.a = 0
#         self.b = 0
#         self.c = 0
#         self.d = 0
#
# # Plane computing part
#     def computePlaneCoefficientsWithThreeDots(self, dot_A: Dot, dot_B: Dot, dot_C: Dot):
#         """ Compute plane equation Ax+By+Cz+D=0 coefficients by given 3 dots """
#         c1 = np.linalg.det(np.array([
#             [dot_B.y - dot_A.y, dot_C.y - dot_A.y],
#             [dot_B.z - dot_A.z, dot_C.z - dot_A.z]
#         ]))
#         c2 = np.linalg.det(np.array([
#             [dot_B.x - dot_A.x, dot_C.x - dot_A.x],
#             [dot_B.z - dot_A.z, dot_C.z - dot_A.z]
#         ]))
#         c3 = np.linalg.det(np.array([
#             [dot_B.x - dot_A.x, dot_C.x - dot_A.x],
#             [dot_B.y - dot_A.y, dot_C.y - dot_A.y]
#         ]))
#
#         self.a = c1
#         self.b = -1 * c2
#         self.c = c3
#         self.d = c1 * (- dot_A.x) - c2 * (- dot_A.y) + c3 * (- dot_A.z)
#         # return self.a, self.b, self.c, self.d
#
#     def computePlaneCoefficientsWithDotAndLine(self, dot_A: Dot, dot_line_a, dot_line_b):
#         """ Compute plane equation Ax+By+Cz+D=0 coefficients by given dot
#             and dots of line, using normal vector to plane """
#         _, a, _, b, _, c = self.computeLineCoefficients(dot_line_a, dot_line_b)
#         normal_vector = np.array([a, b, c])
#         self.a = normal_vector[0]
#         self.b = normal_vector[1]
#         self.c = normal_vector[2]
#         self.d = -1 * dot_A.x * normal_vector[0] + -1 * dot_A.y * normal_vector[1] + -1 * dot_A.z * normal_vector[2]
#         # return self.a, self.b, self.c, self.d
#
#     def computePlaneCoefficientsWithNormalVector(self, dot_A: Dot, a, b, c):
#         """ Compute plane equation Ax+By+Cz+D=0 coefficients by given dot
#             and normal vector to plane """
#         normal_vector = np.array([a, b, c])
#         self.a = normal_vector[0]
#         self.b = normal_vector[1]
#         self.c = normal_vector[2]
#         self.d = -1 * dot_A.x * normal_vector[0] + -1 * dot_A.y * normal_vector[1] + -1 * dot_A.z * normal_vector[2]
#         # return self.a, self.b, self.c, self.d
#
#     def computeLineCoefficients(self, dot_A: Dot, dot_B: Dot):
#         """ Compute line equation in (x-x1)/(x2-x1) = (y-y1)/(y2-y1) = (z-z1)/(z2-z1) format, where:
#             -x1 = a_top, x2-x1 = a_bot etc. """
#         a_top, a_bot = -1 * dot_A.x, dot_B.x - dot_A.x
#         b_top, b_bot = -1 * dot_A.y, dot_B.y - dot_A.y
#         c_top, c_bot = -1 * dot_A.z, dot_B.z - dot_A.z
#         return a_top, a_bot, b_top, b_bot, c_top, c_bot
#
#     def getPlaneEquation(self, dot_A: Dot):
#         """ Get number, which represents position of dot related to given plane:
#             positive/negative number - dot is on one of the sides of a plane,
#             zero - dot belongs to a plane """
#         return dot_A.x * self.a + dot_A.y * self.b + dot_A.z * self.c + self.d
#
#     def __str__(self):
#         return f"a = {self.a} b = {self.b} c = {self.c} d = {self.d}"
