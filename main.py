import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
from scipy.fft import fft, ifft
import os.path
import sys
import logging

from functions import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt='%H:%M:%S')

data_folder = 'data'
filename = 'OR5'

if os.path.exists(f'np{filename}.npy'):
    data = np.load(f'np{filename}.npy')
    logging.info(f'Load file "np{filename}.npy"')
else:
    with open(f'{data_folder}/{filename}.csv', newline='') as csvfile:
        data = np.genfromtxt(csvfile, delimiter=',', skip_header=1, usecols=(0, 1, 2, 3, 4))
        logging.info(f'Load file "{filename}.csv"')
        np.save(f'np{filename}.npy', data, allow_pickle=True, fix_imports=True)
        logging.info(f'Save file "np{filename}.npy"')

Time, CH1V, CH2V, CH3V, CH4V = data.T  # format of oscilloscope Rigol

index_start = index_end = 0

value_start = 1.6e-6
value_end = 7e-6

for i in range(len(Time)):
    if Time[i] > value_start:
        index_start = i
        break

for i in range(len(Time[index_start:])):
    if Time[index_start + i] > value_end:
        index_end = index_start + i
        if (index_end-index_start) % 2:
            index_end -= 1
        break

points = index_end - index_start
iterations = 1000
myfilter = np.zeros(points)
print(myfilter)
band = 100e6
fs = 1/(Time[1] - Time[0])  # Sampling Frequency

# plt.plot(wind)
f0 = 2.45e9



# format order of magnitude of `ax.yaxis`

# plt.show()


# plot result
plt.style.use('dark_background')
px = 1 / plt.rcParams['figure.dpi']
fig = plt.figure(figsize=(1280 * px, 720 * px))

ax = fig.add_subplot(111)

ax.plot(Time, CH1V, color='gold', linewidth=0.5)
ax.plot(Time, CH2V, color='cyan', linewidth=0.5)
# plt.plot(Time, CH3V, color='magenta', linewidth=0.5)
ax.plot(Time, CH4V, color='dodgerblue', linewidth=0.5)

ax.axvline(x=Time[index_start], color='red', linewidth=2)
ax.axvline(x=Time[index_end], color='red', linewidth=2)

ax2 = ax.twinx()
line, = ax2.plot(Time[index_start:index_end], phase_calc(myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V)*(180/np.pi))

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.2, 0.01, 0.5, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Filter, Hz',
    valmin=10e6,
    valmax=300e6,
    valinit=100e6,
)

# The function to be called anytime a slider's value changes
def update(val):
    band = val
    line.set_ydata(phase_calc(myfilter, f0, band, fs, points, index_start, index_end, CH1V, CH2V)*(180/np.pi))
    fig.canvas.draw_idle()


# register the update function with each slider
freq_slider.on_changed(update)


# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='dodgerblue')


def reset(event):
    freq_slider.reset()
button.on_clicked(reset)

ax.grid(which="major", linewidth=0.5, color='gray', linestyle='dashed')
ax.grid(which="minor", linewidth=0.2)
ax.minorticks_on()
ax.set_xlabel(r'Time, s')
ax.set_ylabel('Voltage, V')
ax2.set_ylabel('Phase, degree')

plt.show()

