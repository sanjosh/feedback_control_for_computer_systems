import random
import feedback as fb
import math

class ThreadPool(fb.Component):

    approx_job_processing_rate_per_interval = 3
    max_threads = 10

    def __init__(self):
        self.threads = 3
        self.load = 10

    def work(self, percentage_increase_in_threads):
        '''
        return completion rate - (number of completed/total)
        :param u:
        :return:
        '''
        self.load += max(random.randint(-5, 50), 0)
        if (self.load == 0):
            self.threads = max(self.threads - 1, 1)
            return 1.0


        num_jobs_can_complete = self.threads * __class__.approx_job_processing_rate_per_interval + random.randint(-1, 1)
        completed = min(self.load, num_jobs_can_complete)
        success_rate = completed/self.load
        self.load -= completed

        self.threads = min(__class__.max_threads, self.threads + math.ceil(percentage_increase_in_threads * self.threads))

        print('thr=', self.threads, 'completed=', completed, 'pending=', self.load,
              ' success_rate=', round(success_rate, 2), 'perc=', round(percentage_increase_in_threads, 2))
        return success_rate

# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib
# https://matplotlib.org/examples/animation/index.html

def setpoint(t):
    return 1.0 # ideal completion rate (all pending jobs are completed)

class MyPidController( fb.Component ):
    def __init__( self, kp, ki, kd=0 ):
        self.kp, self.ki, self.kd = kp, ki, kd
        self._sum_of_errors = 0
        self._rate_of_error_change = 0
        self._prev_error = 0

    def work( self, percentage_jobs_not_completed ):
        '''
        input is failure rate which between [0, 1]
        output is percentage to increase threads by
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

        #print(t, t*fb.DT, r, e, u, v, y, z, plant.monitoring())

    quit()

if __name__ == '__main__':
    fb.DT = 1
    plant = ThreadPool()
    controller = MyPidController(0.1, 0.0, 0.3)  # kp = time to complete one job
    closed_loop(setpoint, controller, plant, 10000)