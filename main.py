
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

scope = Oscilloscope('OR5')

f0 = 2.45e9
value_start = 1.6e-6
value_end = 7e-6
band = 100e6

scope.calc_index_start(value_start)
scope.calc_index_end(value_end)

myfilter = Filter(scope, f0, band)
phase = phase_calc(scope, myfilter)

graph = PlotFig(scope, phase)
# # plot result
# plt.style.use('dark_background')
# px = 1 / plt.rcParams['figure.dpi']
# fig = plt.figure(figsize=(1280 * px, 720 * px))
#
# ax = fig.add_subplot(111)
#
# ax.plot(scope.time, scope.ch1, color='gold', linewidth=0.5)
# ax.plot(scope.time, scope.ch2, color='cyan', linewidth=0.5)
# # plt.plot(Time, CH3V, color='magenta', linewidth=0.5)
# ax.plot(scope.time, scope.ch4, color='dodgerblue', linewidth=0.5)
#
# ax.axvline(x=scope.time[scope.index_start], color='red', linewidth=2)
# ax.axvline(x=scope.time[scope.index_end], color='red', linewidth=2)
#
# ax2 = ax.twinx()
# # line, = ax2.plot(Time[index_start:index_end], phase_calc(myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V)*(180/np.pi))
#
# # Make a horizontal slider to control the frequency.
# axfreq = fig.add_axes([0.2, 0.01, 0.5, 0.03])
# freq_slider = Slider(
#     ax=axfreq,
#     label='Filter, Hz',
#     valmin=10e6,
#     valmax=300e6,
#     valinit=100e6,
# )
#
# # The function to be called anytime a slider's value changes
# def update(val):
#     band = val
#     line.set_ydata(phase_calc(myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V)*(180/np.pi))
#     fig.canvas.draw_idle()
#
#
# # register the update function with each slider
# freq_slider.on_changed(update)
#
#
# # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
# resetax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
# button = Button(resetax, 'Reset', hovercolor='dodgerblue')
#
#
# def reset(event):
#     freq_slider.reset()
# button.on_clicked(reset)





