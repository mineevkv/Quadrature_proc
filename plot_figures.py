import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from functions import *


class PlotFig:
    line = None

    def __init__(self, scope, phase, myfilter):
        px = 1 / plt.rcParams['figure.dpi']
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(1920 * px, 1080 * px))

        self.ax = self.fig.add_subplot(111)
        self.ax2 = self.ax.twinx()

        self.ax_filter = self.fig.add_axes([0.2, 0.01, 0.5, 0.03])
        self.filter_slider = Slider(ax=self.ax_filter, label='Filter, MHz', valmin=0.1 * myfilter.bandwidth / 1e6,
                                    valmax=3 * myfilter.bandwidth / 1e6, valinit=myfilter.bandwidth / 1e6)
        self.ax_btn_reset = self.fig.add_axes([0.8, 0.01, 0.1, 0.04])
        self.btn_reset = Button(self.ax_btn_reset, 'Reset', hovercolor='dodgerblue')

        self.index_start = 0
        self.index_end = len(scope.time) - 1

        self.plot_original(scope, myfilter)
        self.plot_phase(scope, phase)

        self.plot_settings(scope)
        self.set_limits(scope)

        self.filter_slider.on_changed(lambda new_val: self.update(new_val, scope, myfilter))
        self.btn_reset.on_clicked(self.reset)
        plt.show()

    def plot_original(self, scope, myfilter):
        if scope.status['CH1']:
            self.ax.plot(scope.time[self.index_start:self.index_end], scope.ch1[self.index_start:self.index_end],
                         color='gold', linewidth=0.5, label='CH1')
        if scope.status['CH2']:
            self.ax.plot(scope.time[self.index_start:self.index_end], scope.ch2[self.index_start:self.index_end],
                         color='cyan', linewidth=0.5, label='CH2')
        if scope.status['CH3']:
            self.ax.plot(scope.time[self.index_start:self.index_end], 0.05*scope.ch3[self.index_start:self.index_end],
                         color='magenta', linewidth=0.5, label='CH3')
        if scope.status['CH4']:
            self.ax.plot(scope.time[self.index_start:self.index_end], scope.ch4[self.index_start:self.index_end] - np.mean(scope.ch4[0:5000]),
                         color='dodgerblue', linewidth=0.5, label='CH4')

        self.ax.axvline(x=scope.time[scope.index_start], color='red', linewidth=2)
        self.ax.axvline(x=scope.time[scope.index_end], color='red', linewidth=2)

        font = {'weight': 'bold', 'size': 16}
        x1 = (scope.time[scope.index_start]-scope.time[0])/(scope.time[len(scope.time)-1] - scope.time[0])
        x2 = (scope.time[scope.index_end] - scope.time[0]) / (scope.time[len(scope.time) - 1] - scope.time[0])
        self.ax.text(x1, 1, f'{round(scope.time[scope.index_start]*1e6, 2)} us', color='red',
                     horizontalalignment='right', verticalalignment=f'bottom', transform=self.ax.transAxes, **font)
        self.ax.text(x2, 1, f'{round(scope.time[scope.index_end] * 1e6, 2)} us', color='red',
                     horizontalalignment='left', verticalalignment=f'bottom', transform=self.ax.transAxes, **font)

        self.ax.text(0.5, 0.98, f'f = {round(myfilter.f0 / 1e6, 6)} MHz', color='white',
                     horizontalalignment='center', verticalalignment=f'top', transform=self.ax.transAxes, **font)


    def plot_phase(self, scope, phase):
        self.line, = self.ax2.plot(scope.time[scope.index_start:scope.index_end], phase)

    def plot_settings(self, scope):
        self.ax.grid(which="major", linewidth=0.5, color='gray', linestyle='dashed')
        self.ax.grid(which="minor", linewidth=0.2)
        self.ax.minorticks_on()
        self.ax.set_xlabel(r'Time, s')
        self.ax.set_ylabel('Voltage, V')
        self.ax2.set_ylabel('Phase, degree')
        font = {'weight': 'bold', 'size': 16}
        self.ax.set_title(f'{scope.filename}.csv', **font)
        self.ax.legend(loc='lower right')

    def set_limits(self, scope):
        self.ax.set_xlim(scope.time[self.index_start], scope.time[self.index_end])

    def update(self, val, scope, myfilter):
        myfilter.calc_filter(scope, val)
        phase = phase_calc(scope, myfilter)
        self.line.set_ydata(phase)
        self.fig.canvas.draw_idle()

    def reset(self, event):
        self.filter_slider.reset()

    # resetax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
    #
# plot result


#
# Make a horizontal slider to control the frequency.

# The function to be called anytime a slider's value changes


# register the update function with each slider


# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
# resetax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
# button = Button(resetax, 'Reset', hovercolor='dodgerblue')
#
#
# def reset(event):
#     freq_slider.reset()
# button.on_clicked(reset)
