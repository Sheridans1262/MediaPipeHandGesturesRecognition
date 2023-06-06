from sklearn.ensemble import RandomForestClassifier
from DatasetUtils import extractDatasetFromDirectory
import time


def trainRandomForest():
    pTime = time.time()
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)

    clf = RandomForestClassifier()
    clf.fit(xTrain, yTrain)
    print(clf.score(xTest, yTest))
    print(f"{time.time() - pTime} seconds")

    return clf


from tensorflow import keras
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adagrad
import numpy as np
from sklearn.model_selection import train_test_split


def trainMultilayerPerceptron():
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)
    xTrain = np.array(xTrain).reshape(int(len(xTrain)), 10).astype('float32')
    xTest = np.array(xTest).reshape(int(len(xTest)), 10).astype('float32')

    yTrain = np.array(yTrain)
    yTest = np.array(yTest)

    model = Sequential(
        [
            layers.Dense(units=26, input_shape=(10,), activation='relu'),
            # layers.Dense(units=6, activation='relu'),
            layers.Dense(units=len(yLabels) - 1, activation='softmax')
        ]
    )

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(xTrain, yTrain, batch_size=15, epochs=15, shuffle=True, verbose=2)

    scores = model.evaluate(xTest, yTest)

    print(scores)
    model.summary()

    return model



x, y, yLabels = extractDatasetFromDirectory("Gestures")

clf = trainMultilayerPerceptron()
# clf = trainRandomForest()

def getGesture(angles: list):
    # SEQUENTIAL MODELS
    gesturesProbs = clf.predict([angles], verbose=0)[0]

    # RANDOM FOREST
    # gesturesProbs = clf.predict_proba([angles])[0]

    print(gesturesProbs)
    current_gesture = gesturesProbs.argmax() if max(gesturesProbs) > 0.8 else -1

    return current_gesture, yLabels[current_gesture]

