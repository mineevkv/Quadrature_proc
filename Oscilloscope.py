
import numpy as np
import os.path
import logging


class Oscilloscope:
    datafolder = 'data'
    data = 0  # general data array
    ch1 = ch2 = ch3 = ch4 = 0  # voltages
    time = 0  # seconds
    index_start = index_end = 0  # index values of signal slice
    points = 0
    fs = 0  # Sampling Frequency
    status = {'CH1': True, 'CH2': True, 'CH3': False, 'CH4': True}

    def __init__(self, filename):
        self.filename = filename
        self.open_file(filename)
        self.read_data()
        self.index_end = len(self.time) - 1
        self.fs = 1 / (self.time[1] - self.time[0])

    def open_file(self, filename):
        if os.path.exists(f'np{filename}.npy'):
            self.data = np.load(f'np{filename}.npy')
            logging.info(f'Load file "np{filename}.npy"')
        else:
            with open(f'{self.datafolder}/{filename}.csv', newline='') as csvfile:
                self.data = np.genfromtxt(csvfile, delimiter=',', skip_header=1, usecols=(0, 1, 2, 3, 4))
                logging.info(f'Load file "{filename}.csv"')
                np.save(f'np{filename}.npy', self.data, allow_pickle=True, fix_imports=True)
                logging.info(f'Save file "np{filename}.npy"')

    def read_data(self):
        self.time, self.ch1, self.ch2, self.ch3, self.ch4 = self.data.T  # format of oscilloscope Rigol

    def calc_index_start(self, time_start):
        for i in range(len(self.time)):
            if self.time[i] > time_start:
                self.index_start = i
                break
        self.calc_points()

    def calc_index_end(self, time_end):
        for i in range(len(self.time[self.index_start:])):
            if self.time[self.index_start + i] > time_end:
                self.index_end = self.index_start + i
                break
        self.calc_points()

    def calc_points(self):
        if (self.index_end - self.index_start)%2:
            if self.index_start%2:
               self.index_start -= 1
            elif self.index_end%2:
               self.index_end += 1
        self.points = self.index_end - self.index_start
