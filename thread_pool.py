import random
import math
import numpy as np
from draw_fig import draw1, draw_all

random.seed(323)

sampling_interval = 1  # sampling interval

def setpoint(t):
    return 1.0 # ideal completion rate (all pending jobs should be completed in each cycle)

class ThreadPool():

    approx_job_processing_rate_per_interval = 3  # static gain

    max_threads = 100

    def __init__(self, swing_factor):
        self.threads = 3
        self.load = 10
        self.swing_factor = swing_factor

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
        self.load += max(self.load_randomizer.randint(-self.swing_factor, self.swing_factor), 0)
        self.load_list.append(self.load)

        if (self.load == 0):
            self.threads = max(self.threads - 3, 1)
            success_rate = 1.0
            completed = 0
        else:
            # Simulate the thread pool completing jobs
            num_jobs_can_complete = self.threads * __class__.approx_job_processing_rate_per_interval + self.work_randomizer.randint(-2, 2)
            completed = min(self.load, num_jobs_can_complete)
            success_rate = completed/self.load
            self.load -= completed

            self.threads = min(__class__.max_threads, self.threads + math.ceil(percentage_increase_in_threads * self.threads))

        print('thr=', self.threads, 'completed=', completed, 'pending=', self.load,
                  ' success_rate=', round(success_rate, 2), 'perc=', round(percentage_increase_in_threads, 2))
        self.thread_list.append(self.threads)
        self.rate_list.append(success_rate)
        return success_rate

class MyPidController():

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
        self._sum_of_errors += sampling_interval *percentage_jobs_not_completed
        self._rate_of_error_change = ( percentage_jobs_not_completed - self._prev_error )/sampling_interval
        self._prev_error = percentage_jobs_not_completed

        percent_increase = self.kp*percentage_jobs_not_completed + self.ki*self._sum_of_errors + self.kd*self._rate_of_error_change
        return min(percent_increase, 1.0)

def closed_loop( setpoint, controller, plant, tm=5000, inverted=False):
    z = 0
    for t in range( tm ):
        r = setpoint(t)
        e = r - z
        if inverted == True: e = -e
        u = controller.work(e)
        z = plant.work(u)

if __name__ == '__main__':

    swing_factor_in_load = 1

    plant = ThreadPool(swing_factor_in_load)

    k_proportional = round((1/ThreadPool.approx_job_processing_rate_per_interval), 1)  # static gain factor
    k_integral = 0.1
    k_derivative = 0.0
    controller = MyPidController(k_proportional, k_integral, k_derivative)  # kp = time to complete one job
    closed_loop(setpoint, controller, plant, 10000)

    data = np.array([plant.rate_list, plant.thread_list, plant.load_list])
    t = np.arange(0, data.shape[1])
    success_rate = data[0,:]
    thread_num = data[1,:]
    load_num = data[2,:]

    draw_all(t, thread_num, load_num, success_rate, k_proportional, k_integral, k_derivative, swing_factor_in_load)