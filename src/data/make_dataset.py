import os
import numpy as np

REBUILD_DATA = True


class MusicData:
    RAWDATA = "raw-data"
    training_data = []
    genre_dict = {}

    def make_training_data(self):
        self.__create_genre_dictionary()
        # Iterate through all genres
        for genre in self.genre_dict:
            # For each file in a genre
            for f in os.listdir(self.RAWDATA + "/" + genre):
                # Use Librosa to create a spectrograph - Midhun's code
                img = []
                # Add image and label to training data
                self.training_data.append([np.array(img), np.eye(len(self.genre_dict))[self.genre_dict[genre]]])

        # Shuffle and save dataset
        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)

    def __create_genre_dictionary(self):
        self.genre_dict = {}
        genre_count = 0
        for g in os.listdir(self.RAWDATA):
            self.genre_dict[g] = genre_count
            genre_count += 1


if REBUILD_DATA:
    musicdata = MusicData()
    musicdata.make_training_data()

