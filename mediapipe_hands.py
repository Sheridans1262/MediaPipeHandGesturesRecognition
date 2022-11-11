import time

import cv2
import mediapipe as mp
from mediapipe.python.solutions.hands import HandLandmark
from plane import Plane


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

            for hand_world_landmarks in result.multi_hand_world_landmarks:
                mp.solutions.drawing_utils.plot_landmarks(
                    hand_world_landmarks, self.mp_hands.HAND_CONNECTIONS, azimuth=5)
            return result

    def processHandsFromVideo(self):
        cap = cv2.VideoCapture(0)

        with self.mp_hands.Hands(
                model_complexity=0,
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
                start = time.perf_counter()
                results = hands.process(image)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        pl = Plane(hand_landmarks.landmark[HandLandmark.WRIST],
                                   hand_landmarks.landmark[HandLandmark.INDEX_FINGER_MCP],
                                   hand_landmarks.landmark[HandLandmark.PINKY_MCP])
                        for i in range(20):
                            A_proj = pl.getDotProjectionOnPlane(hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP])
                    print(time.perf_counter() - start)

                    self.showImageFromVideo(image, results)

                if cv2.waitKey(1) == ord('q'):
                    break
        cap.release()

    def showImageFromVideo(self, image, results):
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))