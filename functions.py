import numpy as np
import math as m
from scipy.fft import fft, ifft

def mfilter(filter_data, f0, band, fs, points):
    df = fs / points
    dimension = round(band / df)
    if dimension % 2:
        dimension += 1

    print(dimension)
    window = np.hanning(dimension)
    point_start = m.floor((f0 - band / 2) / df)
    point_end = m.ceil((f0 + band / 2) / df)

    if point_start % 2:
        point_start += 1

    if point_end % 2:
        point_start -= 1

    if point_start > point_end - dimension:
        point_end = point_start + dimension
    elif point_start < point_end - dimension:
        point_start = point_end - dimension

    filter_data[point_start:point_end] = window
    return

def phase_calc(scope, myfilter):
    # myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V):
    # mfilter(myfilter, f0, band, fs, points)

    Op = scope.voltage['CH1'][scope.index_start:scope.index_end]
    Ch = scope.voltage['CH2'][scope.index_start:scope.index_end]

    Op = Op - np.mean(Op)
    Ch = Ch - np.mean(Ch)

    spOp = fft(Op)
    spCh = fft(Ch)

    spOp = np.multiply(spOp, myfilter.dataarray)
    spCh = np.multiply(spCh, myfilter.dataarray)

    Op = ifft(spOp)
    Ch = ifft(spCh)
    Interferogramm = np.multiply(Op, np.conj(Ch))
    Phi = np.angle(Interferogramm)
    return Phi*180/np.pi

def calc_center_freq(scope):
    fourier = fft(scope.voltage['CH1'])
    timestep = scope.time[1] - scope.time[0]

    freq = np.fft.fftfreq(scope.voltage['CH1'].size, d=timestep)
    max_element = abs(fourier)[0]
    for i in range(1, len(fourier)):  # iterate over array
        if abs(fourier[i]) > max_element:  # to check max value
            max_element = abs(fourier[i])
            ind = i

    return freq[ind]