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

def phase_calc(myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V):
    mfilter(myfilter, f0, band, fs, points)

    Op = CH1V[index_start:index_end]
    Ch = CH2V[index_start:index_end]

    Op = Op - np.mean(Op)
    Ch = Ch - np.mean(Ch)

    spOp = fft(Op)
    spCh = fft(Ch)

    spOp = np.multiply(spOp, myfilter)
    spCh = np.multiply(spCh, myfilter)

    Op = ifft(spOp)
    Ch = ifft(spCh)
    Interferogramm = np.multiply(Op, np.conj(Ch))
    Phi = np.angle(Interferogramm)
    return Phi