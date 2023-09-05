
import numpy as np
from scipy.fft import fft, ifft
import os.path
import sys
import logging

from functions import *
from Oscilloscope import *
from filter import *
from plot_figures import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt='%H:%M:%S')

scope = Oscilloscope('OR2')

value_start = 0.6e-6
value_end = 7.9e-6

scope.calc_index_start(value_start)
scope.calc_index_end(value_end)
f0 = calc_center_freq(scope)

myfilter = Filter(scope, f0)
phase = phase_calc(scope, myfilter)

graph = PlotFig(scope, phase, myfilter)





