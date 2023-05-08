import socket
import cv2
import numpy as np
import mss
import pyautogui

sct = mss.mss()


def doAssociatedAction(gesture: int):
    match gesture:
        case -1:
            return
        case 0:
            action0()
        case 1:
            action1()
        case 2:
            action2()
        case 3:
            action3()


def action0():
    pass
    # pressButton(1)


def action1():
    pass
    # pressButton(2)


def action2():
    pass
    # pressButton(3)


def action3():
    pass
    # pressButton(4)


def sendSignalThroughTCP(signal):
    try:
        host = socket.gethostname()
        port = 5001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        if signal == 1:
            s.sendall(b'D')
        else:
            s.sendall(b'A')
        s.close()
    except ConnectionRefusedError:
        print("Connection refused")


def pressButton(buttonId):
    try:
        if buttonId == 1:
            template = cv2.imread("control images/yandex player controls/playYandex.png")
        if buttonId == 2:
            template = cv2.imread("control images/yandex player controls/pauseYandex.png")
        if buttonId == 3:
            template = cv2.imread("control images/yandex player controls/nextYandex.png")
        if buttonId == 4:
            template = cv2.imread("control images/yandex player controls/prevYandex.png")

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)

        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        screenshot = cv2.Canny(screenshot, 50, 200)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if maxVal > 0.8:
            clickPos = (maxLoc[0] + (template.shape[1] / 2), maxLoc[1] + (template.shape[0] / 2))
            print(clickPos)

            mousePreviousPos = pyautogui.position()
            pyautogui.click(clickPos)
            pyautogui.moveTo(mousePreviousPos)
    except ValueError:
        print("Cannot read icon image")
