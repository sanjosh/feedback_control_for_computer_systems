import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


def draw1(prefix, t, label1, data1, label2, data2,
          k_proportional, k_integral, k_derivative):

    fig, ax1 = plt.subplots()

    xnew = np.linspace(t.min(), t.max(), 50)

    # define spline
    spl = make_interp_spline(t, data1, k=3)
    data1_smooth = spl(xnew)

    spl = make_interp_spline(t, data2, k=3)
    data2_smooth = spl(xnew)

    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel(label1, color=color)
    ax1.plot(xnew, data1_smooth, color=color, markevery=100)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel(label2, color=color)  # we already handled the x-label with ax1
    ax2.plot(xnew, data2_smooth, color=color, markevery=100)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.locator_params(axis='x', nbins=10)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #plt.show()

    filename = 'p{}_i{}_d{}_{}.png'.format(k_proportional, k_integral, k_derivative, prefix)
    plt.savefig(filename)