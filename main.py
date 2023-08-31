import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, ifft
import os.path
import sys
import logging

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

value_start = 1.5e-6
value_end = 6.81e-6

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
myfilter[0: int((points/2))] = 1

print(myfilter)

spOp = fft(CH1V[index_start:index_end])
spCh = fft(CH2V[index_start:index_end])

plt.plot(abs(spCh))
plt.plot(abs(spOp))
plt.show()


# plot result
plt.style.use('dark_background')
px = 1 / plt.rcParams['figure.dpi']
fig = plt.figure(figsize=(1280 * px, 720 * px))

ax = fig.add_subplot(111)

plt.plot(Time, CH1V, color='gold', linewidth=0.5)
plt.plot(Time, CH2V, color='cyan', linewidth=0.5)
# plt.plot(Time, CH3V, color='magenta', linewidth=0.5)
plt.plot(Time, CH4V, color='dodgerblue', linewidth=0.5)

plt.axvline(x=Time[index_start], color='red', linewidth=2)
plt.axvline(x=Time[index_end], color='red', linewidth=2)

ax.grid(which="major", linewidth=0.5, color='gray', linestyle='dashed')
ax.grid(which="minor", linewidth=0.2)
ax.minorticks_on()
ax.set_xlabel(r'Time, s')
ax.set_ylabel('Voltage, V')

# plt.show()
