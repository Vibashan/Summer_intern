#!/usr/bin/env python

import math
import time
import matplotlib.pyplot as plt
import numpy as np

from sympy import Symbol, Derivative

def path_planning(t,mode):
    '''x = math.cos(t)
    y = math.sin(2*t)
    x_dot = -math.sin(t)
    y_dot = 2*math.cos(2*t)'''

    '''x = t
    y = 3*math.sin((t*math.pi)/8)
    x_dot = 1
    y_dot = ((3*math.pi)/8)*math.cos((t*math.pi)/8)'''

    '''x = t/4
    y = t*t/16
    x_dot = 1/4
    y_dot = t/8'''

    '''x = t
    y = 2*math.sin((t*math.pi)/8)
    x_dot = 1
    y_dot = (math.pi/4)*math.cos((t*math.pi)/8)'''

    '''x = 3*math.sin((t*math.pi)/8)
    y = -3 + 3*math.cos((t*math.pi)/8)
    x_dot = ((3*math.pi)/8)*math.cos((t*math.pi)/8)
    y_dot = ((-3*math.pi)/8)*math.sin((t*math.pi)/8)'''

    x = -3 + 3*math.cos((t*math.pi)/8)
    y = 3*math.sin((t*math.pi)/4)
    x_dot = -((3*math.pi)/8)*math.sin((t*math.pi)/8)
    y_dot = ((3*math.pi)/8)*math.cos((t*math.pi)/4)

    r_t = math.sqrt(x*x+y*y)
    if r_t == 0:
        r_t = 0.000001
    #r_dot = abs(x*x_dot+y*y_dot)/(r_t)
    r_dot = math.sqrt(x_dot*x_dot+y_dot*y_dot)
    theta_t = math.degrees(math.atan2(y_dot,x_dot))

    if mode == "r_dot":
        return r_dot
    elif mode == "x_axis":
        return x
    elif mode == "y_axis":
        return y
    elif mode == "x_vel":
        return x_dot
    elif mode == "y_vel":
        return y_dot
    elif mode == "r_t":
        return r_t
    elif mode == "theta_t":
        return theta_t

def trajectory_gen():
    total_time = 16
    sampling_rate = 0.25
    x_t,y_t = [],[]
    x_dot,y_dot = [],[]
    r_t,r_dot = [],[]
    theta_t = []
    for i in range(int(total_time/sampling_rate)):
        x_t.append(path_planning(i*sampling_rate,"x_axis"))
        y_t.append(path_planning(i*sampling_rate,"y_axis"))
        x_dot.append(path_planning(i*sampling_rate,"x_vel"))
        y_dot.append(path_planning(i*sampling_rate,"y_vel"))
        r_t.append(path_planning(i*sampling_rate,"r_t"))
        r_dot.append(path_planning(i*sampling_rate,"r_dot"))
        theta_t.append(path_planning(i*sampling_rate,"theta_t"))
    return x_t,y_t,x_dot,y_dot,r_t,r_dot,theta_t,total_time,sampling_rate

def plotting(x_t,y_t,x_dot,y_dot,r_t,r_dot,theta_t,total_time,sampling_rate):
	plt.figure(1)
	plt.subplot(211)
	plt.plot(x_t)
	plt.ylabel('X-axis')

	plt.subplot(212)
	plt.plot(y_t)
	plt.ylabel('Y-axis')

	plt.figure(2)
	plt.subplot(211)
	plt.plot(r_t)
	plt.ylabel('R-axis')

	plt.subplot(212)
	plt.plot(r_dot)
	plt.ylabel('R-vel')

	plt.figure(3)
	plt.subplot(211)
	plt.plot(theta_t)
	plt.ylabel('theta-axis')

	plt.subplot(212)
	plt.plot(x_t,y_t)
	plt.axis([-8, 8, -8, 8])
	plt.ylabel('curve')

	plt.figure(4)
	plt.subplot(211)
	plt.plot(x_dot)
	plt.ylabel('X-vel')

	plt.subplot(212)
	plt.plot(y_dot)
	plt.ylabel('Y-vel')

	plt.show()


if __name__ == '__main__':

    x_t,y_t,x_dot,y_dot,r_t,r_dot,theta_t,total_time,sampling_rate  = trajectory_gen()
    plotting(x_t,y_t,x_dot,y_dot,r_t,r_dot,theta_t,total_time,sampling_rate)