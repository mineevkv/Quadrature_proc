import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class PlotFig:
    def __init__(self, scope, phase):
        self.line = None
        px = 1 / plt.rcParams['figure.dpi']
        self.fig = plt.figure(figsize=(1280 * px, 720 * px))
        # plt.style.use('dark_background')
        self.ax = self.fig.add_subplot(111)
        self.ax2 = self.ax.twinx()

        self.plot_original(scope)
        self.plot_phase(scope, phase)

        self.setting()
        plt.show()

    def plot_original(self, scope):
        if scope.status['CH1']:
            self.ax.plot(scope.time, scope.ch1, color='gold', linewidth=0.5)
        if scope.status['CH2']:
            self.ax.plot(scope.time, scope.ch2, color='cyan', linewidth=0.5)
        if scope.status['CH3']:
            self.ax.plot(scope.time, scope.ch3, color='magenta', linewidth=0.5)
        if scope.status['CH4']:
            self.ax.plot(scope.time, scope.ch4, color='dodgerblue', linewidth=0.5)

        self.ax.axvline(x=scope.time[scope.index_start], color='red', linewidth=2)
        self.ax.axvline(x=scope.time[scope.index_end], color='red', linewidth=2)

    def plot_phase(self, scope, phase):
        self.line, = self.ax2.plot(scope.time[scope.index_start:scope.index_end], phase)

    def setting(self):
        self.ax.grid(which="major", linewidth=0.5, color='gray', linestyle='dashed')
        self.ax.grid(which="minor", linewidth=0.2)
        self.ax.minorticks_on()
        self.ax.set_xlabel(r'Time, s')
        self.ax.set_ylabel('Voltage, V')
        self.ax2.set_ylabel('Phase, degree')


# plot result








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
#
# ax.grid(which="major", linewidth=0.5, color='gray', linestyle='dashed')
# ax.grid(which="minor", linewidth=0.2)
# ax.minorticks_on()
# ax.set_xlabel(r'Time, s')
# ax.set_ylabel('Voltage, V')
# ax2.set_ylabel('Phase, degree')
#
# plt.show()
#
