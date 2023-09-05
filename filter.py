import numpy as np
import math as m


class Filter:
    bandwidth = 100e6  # 10 MHz
    df = 0
    point_start = point_end = 0  # index values of signal slice
    dimension = 0
    dataarray = None

    def __init__(self, data, f0):
        self.f0 = f0
        self.calc_filter(data, self.bandwidth/1e6)

    def calc_df(self, data):
        self.df = data.fs / data.points

    def calc_dimension(self):
        self.dimension = round(self.bandwidth / self.df)
        if self.dimension % 2:
            self.dimension += 1

    def calc_points(self):
        self.point_start = m.floor((self.f0 - self.bandwidth/2) / self.df)
        self.point_end = m.ceil((self.f0 + self.bandwidth/2) / self.df)

        if self.point_start % 2:
            self.point_start += 1

        if self.point_end % 2:
            self.point_end -= 1

        if self.point_start > self.point_end - self.dimension:
            self.point_end = self.point_start + self.dimension
        elif self.point_start < self.point_end - self.dimension:
            self.point_start = self.point_end - self.dimension

    def calc_filter(self, data, band):
        self.bandwidth = band * 1e6  # Hz
        self.calc_df(data)
        self.calc_dimension()
        self.calc_points()
        self.dataarray = np.zeros(data.points)
        self.dataarray[self.point_start:self.point_end] = np.hanning(self.dimension)
