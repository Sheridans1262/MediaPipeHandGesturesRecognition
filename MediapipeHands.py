import math
import time

import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
from mediapipe.python.solutions.hands import HandLandmark

from Actions import doAssociatedAction
from Classifier import getGesture
from DataClasses import Finger, Dot

from AnglesExtencion import getAngles


class MediapipeHands:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

    def processHandsFromImage(self, filename):
        with self.mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.5) as hands:
            # Read an image, flip it around y-axis for correct handedness output (see
            # above).
            image = cv2.flip(cv2.imread(filename), 1)
            # Convert the BGR image to RGB before processing.
            result = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not result.multi_hand_world_landmarks:
                return

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    angles = getAngles(hand_landmarks)
                    # self.plotDots(dots)
                    # for angle in angles:
                    #     print((angle * 180) / math.pi)
                    self.showImageFromVideo(image, result)
            for hand_world_landmarks in result.multi_hand_world_landmarks:
                mp.solutions.drawing_utils.plot_landmarks(
                    hand_world_landmarks, self.mp_hands.HAND_CONNECTIONS, azimuth=5)
            return result

    def processHandsFromVideo(self):
        cap = cv2.VideoCapture(0)

        current_gesture = 1
        current_gesture_counter = 0
        previous_action = 0

        with self.mp_hands.Hands(
                model_complexity=0,
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        angles = getAngles(hand_landmarks)
                        #print((angles[3] * 180) / math.pi)
                    next_gesture, next_gesture_name = getGesture(angles)
                    if next_gesture == current_gesture:
                        current_gesture_counter += 1
                    else:
                        current_gesture_counter = 0

                    current_gesture = next_gesture

                    if current_gesture_counter > 15:
                        if previous_action != current_gesture:
                            previous_action = current_gesture
                            doAssociatedAction(next_gesture)
                        print(next_gesture_name)
                        current_gesture_counter = 0

                self.showImageFromVideo(image, results)

                if cv2.waitKey(1) == ord('q'):
                    break
        cap.release()

    def showImageFromVideo(self, image, results):
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    def plotDots(self, dots):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        markers = ["thumb", "index", "middle", "ring", "pinky"]
        for index, dot in enumerate(dots):
            ax.scatter(dot.x,dot.y, dot.z, label=markers[index])

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        ax.legend(loc="best")

        plt.show()
