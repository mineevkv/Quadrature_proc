
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

scope = Oscilloscope('OR7')

f0 = 2.45e9
value_start = 2.58e-6
value_end = 5.8e-6

scope.calc_index_start(value_start)
scope.calc_index_end(value_end)

myfilter = Filter(scope, f0)
phase = phase_calc(scope, myfilter)

graph = PlotFig(scope, phase, myfilter)





