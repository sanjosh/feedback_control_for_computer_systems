import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import matplotlib as mpl

# mpl.use('GTK3Agg')

def draw_all(t, thread_num, load_list, success_rate, k_proportional, k_integral, k_derivative):

    xnew = np.linspace(t.min(), t.max(), 50)

    # define spline
    spl = make_interp_spline(t, thread_num, k=3)
    thread_num_smooth = spl(xnew)

    spl = make_interp_spline(t, load_list, k=3)
    load_list_smooth = spl(xnew)

    spl = make_interp_spline(t, success_rate, k=3)
    success_rate_smooth = spl(xnew)

    ax0 = plt.subplot(211)
    ax1 = ax0.twinx()
    ax2 = plt.subplot(212)
    ax3 = ax2.twinx()

    ax1.get_shared_y_axes().join(ax1, ax3)

    ax0.plot(xnew, load_list_smooth, 'r', markevery=100, label='pending jobs')
    ax0.set_ylabel('pending jobs')
    ax1.plot(xnew, thread_num_smooth, 'b', markevery=100, label='num threads')
    ax1.set_ylabel('num threads')
    ax2.plot(xnew, success_rate_smooth, 'g', markevery=100, label='setpoint')
    ax2.set_ylabel('success rate')
    # ax3.plot(xnew, thread_num_smooth, 'b', label='num threads')
    # ax3.set_ylabel('num threads')

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # fig.legend()
    # # plt.show()
    plt.locator_params(axis='x', nbins=10)

    filename = 'p{}_i{}_d{}.png'.format(k_proportional, k_integral, k_derivative)
    plt.savefig(filename)


def draw_all_old(t, thread_num, load_list, success_rate, k_proportional, k_integral, k_derivative):

    mpl.style.use('seaborn')

    xnew = np.linspace(t.min(), t.max(), 50)

    # define spline
    spl = make_interp_spline(t, thread_num, k=3)
    thread_num_smooth = spl(xnew)

    spl = make_interp_spline(t, load_list, k=3)
    load_list_smooth = spl(xnew)

    spl = make_interp_spline(t, success_rate, k=3)
    success_rate_smooth = spl(xnew)

    fig, axes = plt.subplots(1, 2)

    ax1 = axes[0]
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('threads')
    plt.plot(xnew, thread_num_smooth, 'C0', markevery=100, label='threads')
    ax1_twin = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax1_twin.plot(xnew, success_rate_smooth, 'C2', markevery=100, label='success rate')
    ax1_twin.set_ylabel('success rate')

    ax2 = axes[1]
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('threads')
    plt.plot(xnew, thread_num_smooth, 'C0', markevery=100, label='threads')
    ax2_twin = ax2.twinx()  # instantiate a second axes that shares the same x-axis
    ax2_twin.plot(xnew, load_list_smooth, 'C2', markevery=100, label='load list')
    ax2_twin.set_ylabel('load list')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.legend()
    # plt.show()

    filename = 'p{}_i{}_d{}.png'.format(k_proportional, k_integral, k_derivative)
    plt.savefig(filename)

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