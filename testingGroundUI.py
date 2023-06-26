import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QComboBox, QFormLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import mediapipe as mp

from Actions import doAssociatedAction
from AnglesExtencion import getAngles
from Classifier import getGesture


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    mp_hands = mp.solutions.hands

    def run(self):
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

                image = self.showImageFromVideo(image, results)

                h, w, ch = image.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if cv2.waitKey(1) == ord('q'):
                    break

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

                self.showImageFromVideo(image, results)

                if cv2.waitKey(1) == ord('q'):
                    break
        cap.release()

    def showImageFromVideo(self, image, results):
        image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS)
        image = cv2.flip(image, 1)
        return image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 200
        self.top = 200
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(900, 500)

        # create a label
        self.main_layout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.move(10, 10)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        self.main_layout.addWidget(self.label)

        self.control_group_layout = QFormLayout()
        self.main_layout.addLayout(self.control_group_layout)

        self.combobox1_label = QLabel("Fist - ")
        self.combobox1 = QComboBox()
        self.combobox1.addItems(["Play", "Pause", "Next", "Previous", "None"])
        self.control_group_layout.addRow(self.combobox1_label, self.combobox1)

        self.combobox2_label = QLabel("FlatPalm - ")
        self.combobox2 = QComboBox()
        self.combobox2.addItems(["Pause", "Play", "Next", "Previous", "None"])
        self.control_group_layout.addRow(self.combobox2_label, self.combobox2)

        self.combobox3_label = QLabel("PeaceSign - ")
        self.combobox3 = QComboBox()
        self.combobox3.addItems(["Next", "Previous", "Play", "Pause", "None"])
        self.control_group_layout.addRow(self.combobox3_label, self.combobox3)

        self.combobox4_label = QLabel("PointingIndexFinger - ")
        self.combobox4 = QComboBox()
        self.combobox4.addItems(["Previous", "Next", "Play", "Pause", "None"])
        self.control_group_layout.addRow(self.combobox4_label, self.combobox4)

        self.combobox5_label = QLabel("PointingPinky- ")
        self.combobox5 = QComboBox()
        self.combobox5.addItems(["None", "Play", "Pause", "Next", "Previous"])
        self.control_group_layout.addRow(self.combobox5_label, self.combobox5)

        self.label6 = QLabel("FlatPalm")
        self.control_group_layout.addWidget(self.label6)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
