import random
import feedback as fb
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

random.seed(323)

def setpoint(t):
    return 1.0 # ideal completion rate (all pending jobs should be completed in each cycle)

class ThreadPool(fb.Component):

    approx_job_processing_rate_per_interval = 3
    max_threads = 100

    def __init__(self):
        self.threads = 3
        self.load = 10

        self.thread_list = []
        self.rate_list = []
        self.load_list = []
        self.load_randomizer = random.Random()
        self.work_randomizer = random.Random()

    def work(self, percentage_increase_in_threads):
        '''
        change the number of threads
        simulate the processing of pending jobs
        return completion rate = (number of completed/total)
        :param u:
        :return:
        '''

        # Simulate changes in load (incoming jobs)
        self.load += max(self.load_randomizer.randint(-5, 5), 0)
        self.load_list.append(self.load)

        if (self.load == 0):
            self.threads = max(self.threads - 3, 1)
            success_rate = 1.0
            completed = 0
        else:
            # Simulate the thread pool completing jobs
            num_jobs_can_complete = self.threads * __class__.approx_job_processing_rate_per_interval + self.work_randomizer.randint(-1, 1)
            completed = min(self.load, num_jobs_can_complete)
            success_rate = completed/self.load
            self.load -= completed

            self.threads = min(__class__.max_threads, self.threads + math.ceil(percentage_increase_in_threads * self.threads))

        print('thr=', self.threads, 'completed=', completed, 'pending=', self.load,
                  ' success_rate=', round(success_rate, 2), 'perc=', round(percentage_increase_in_threads, 2))
        self.thread_list.append(self.threads)
        self.rate_list.append(success_rate)
        return success_rate

class MyPidController( fb.Component ):

    def __init__( self, kp, ki, kd=0 ):
        self.kp, self.ki, self.kd = kp, ki, kd
        self._sum_of_errors = 0
        self._rate_of_error_change = 0
        self._prev_error = 0

    def work( self, percentage_jobs_not_completed ):
        '''
        input is failure rate which between [0, 1]
        output is percentage by which to increase or decrease current threads
        :param error:
        :return:
        '''
        self._sum_of_errors += fb.DT*percentage_jobs_not_completed
        self._rate_of_error_change = ( percentage_jobs_not_completed - self._prev_error )/fb.DT
        self._prev_error = percentage_jobs_not_completed

        percent_increase = self.kp*percentage_jobs_not_completed + self.ki*self._sum_of_errors + self.kd*self._rate_of_error_change
        return min(percent_increase, 1.0)

def closed_loop( setpoint, controller, plant, tm=5000, inverted=False,
                 actuator=fb.Identity(), returnfilter=fb.Identity() ):
    z = 0
    for t in range( tm ):
        r = setpoint(t)
        e = r - z
        if inverted == True: e = -e
        u = controller.work(e)
        v = actuator.work(u)
        y = plant.work(v)
        z = returnfilter.work(y)

def draw1(prefix, t, label1, data1, label2, data2):

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

    filename = prefix + '_p{}_i{}_d{}.png'.format(k_proportional, k_integral, k_derivative)
    plt.savefig(filename)

if __name__ == '__main__':
    fb.DT = 1
    plant = ThreadPool()
    k_proportional = 0.9
    k_integral = 0.0
    k_derivative = 0.1
    controller = MyPidController(k_proportional, k_integral, k_derivative)  # kp = time to complete one job
    closed_loop(setpoint, controller, plant, 1000)

    data = np.array([plant.rate_list, plant.thread_list, plant.load_list])
    print(data.shape)

    t = np.arange(0, data.shape[1])
    data1 = data[0,:]
    data2 = data[1,:]
    data3 = data[2,:]

    draw1('threadpool',t, 'success_rate', data1, 'num threads', data2)
    draw1('load', t, 'load', data3, 'num threads', data2)