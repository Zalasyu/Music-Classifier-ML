import os
# import cv2 as cv
import numpy as np

REBUILD_DATA = True


class MusicData():
    RAWDATA = "/raw-data"
    training_data = []

    def make_training_data(self):
        for f in os.listdir(self.RAWDATA):
            path = os.path.join(self.RAWDATA, f)
            # img = cv.imread(path, cv.IMREAD_GRAYSCALE)
            # call Librosa function

            # Need way to create genre dictionary so a one-hot vector can be returned
            # self.training_data.append()

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)


if REBUILD_DATA:
    musicdata = MusicData()
    musicdata.make_training_data()

