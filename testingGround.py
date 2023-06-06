import time

import cv2
import keras
import numpy as np
import mss
import pyautogui

# sct = mss.mss()
#
# template = cv2.imread("control images/minimize.png")
# template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# template = cv2.Canny(template, 50, 200)
#
# monitor = sct.monitors[1]
# screenshot = sct.grab(monitor)
# screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
# screenshot = cv2.Canny(screenshot, 50, 200)
#
# result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
# (minVal, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
# if maxVal > 0.7:
#     clickPos = (maxLoc[0] + (template.shape[1] / 2), maxLoc[1] + (template.shape[0] / 2))
#     print(clickPos)

    # mousePreviousPos = pyautogui.position()
    # pyautogui.click(clickPos)
    # pyautogui.moveTo(mousePreviousPos)

from sklearn.model_selection import train_test_split

from DatasetUtils import extractDatasetFromDirectory

import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adagrad
import numpy as np


def trainMultilayerPerceptron():
    x, y, yLabels = extractDatasetFromDirectory("Gestures")
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)

    # inputs = keras.Input(shape=(10,))
    # x = layers.Dense(8, activation='relu')(inputs)
    # x = layers.Dense(6, activation='relu')(x)
    # outputs = layers.Dense(len(yLabels))(x)
    #
    # model = keras.Model(inputs=inputs, outputs=outputs, name='simple_classifier')
    #
    # model.summary()
    #
    # model.compile(
    #     loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #     optimizer=keras.optimizers.RMSprop(),
    #     metrics=['accuracy']
    # )
    #
    # xTrain = np.array(xTrain).reshape(6905, 10).astype('float32') / 255
    # xTest = np.array(xTest).reshape(1727, 10).astype('float32') / 255
    #
    # yTrain = np.array(yTrain)
    # yTest = np.array(yTest)

    # history = model.fit(xTrain, yTrain, batch_size=64, epochs=50, validation_split=0.2)
    #
    # testScores = model.evaluate(xTest, yTest)
    #
    # print('Test loss: ', testScores[0])
    # print('Test accuracy: ', testScores[1])
    # keras.utils.plot_model(model, 'simple_classifier_plotted_graph.png', show_shapes=True)

    xTrain = np.array(xTrain).reshape(int(len(xTrain)), 10).astype('float32')
    xTest = np.array(xTest).reshape(int(len(xTest)), 10).astype('float32')

    yTrain = np.array(yTrain)
    yTest = np.array(yTest)

    model = Sequential(
        [
            layers.Dense(units=26, input_shape=(10,), activation='relu'),
            # layers.Dense(units=10, activation='relu'),
            layers.Dense(units=len(yLabels) - 1, activation='softmax')
        ]
    )

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(xTrain, yTrain, batch_size=10, epochs=10, shuffle=True, verbose=1)

    scores = model.evaluate(xTest, yTest)

    print(scores)
    model.summary()


trainMultilayerPerceptron()