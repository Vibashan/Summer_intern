#!/usr/bin/env python

import math
import matplotlib.pyplot as plt
import numpy as np

from munkres import Munkres,print_matrix

def path_planning(t,mode):
    x = -2 + 2*math.cos((t*math.pi)/10)
    y = 2*math.sin((t*math.pi)/5)
    x_dot = -((2*math.pi)/10)*math.sin((t*math.pi)/10)
    y_dot = ((2*math.pi)/5)*math.cos((t*math.pi)/5)

    r_t = math.sqrt(x*x+y*y)
    if r_t == 0:
        r_t = 0.000001
    r_dot = math.sqrt(x_dot*x_dot+y_dot*y_dot)
    theta_t = math.degrees(math.atan2(y_dot,x_dot))

    if mode == "r_dot":
        return r_dot
    elif mode == "x_axis":
        return x
    elif mode == "y_axis":
        return y
    elif mode == "r_t":
        return r_t
    elif mode == "theta_t":
        return theta_t

def trajectory_gen(bots):
    total_time = 20
    sampling_rate = 0.25
    x_t,y_t = [],[]
    r_t,r_dot = [],[]
    theta_t = []
    for gen in range(bots):
    	x_t.append([]),y_t.append([]),r_t.append([]),r_dot.append([]),theta_t.append([])
    	shift = gen*(total_time/(bots+1))
    	if bots%2 != 0: 
    		shift = gen*(total_time/bots)
    	for i in range(int(total_time/sampling_rate)):
	        x_t[gen].append(path_planning(shift+i*sampling_rate,"x_axis"))
	        y_t[gen].append(path_planning(shift+i*sampling_rate,"y_axis"))
	        r_t[gen].append(path_planning(shift+i*sampling_rate,"r_t"))
	        r_dot[gen].append(path_planning(shift+i*sampling_rate,"r_dot"))
	        theta_t[gen].append(path_planning(shift+i*sampling_rate,"theta_t"))  
    return x_t,y_t,r_t,r_dot,theta_t,total_time,sampling_rate

def swarm_algo(total_bots,bot_mat):
	m = Munkres()
	matrix = bot_mat
	indexes = m.compute(matrix)
	print_matrix(matrix, msg='Lowest cost through this matrix:')
	total = 0
	for row, column in indexes:
		value = matrix[row][column]
		total += value
		print '(%d, %d) -> %d' % (row, column, value)
		print 'total cost: %d' % total
	return 

def plotting(x_t,y_t,r_t,r_dot,theta_t,bots):
    plt.figure(1)
    plt.subplot(211)
    for i in range(bots):
    	#print x_t[i]
    	plt.plot(x_t[i],'r')
    plt.ylabel('X-axis')

    plt.subplot(212)
    for i in range(bots):
    	plt.plot(y_t[i],'r')
    plt.ylabel('Y-axis')

    plt.figure(2)
    plt.subplot(211)
    for i in range(bots):
    	plt.plot(r_t[i],'r')
    plt.ylabel('R-axis')

    plt.subplot(212)
    for i in range(bots):
    	plt.plot(r_dot[i],'r')
    plt.ylabel('R-dot')

    plt.figure(3)
    plt.subplot(211)
    for i in range(bots):
    	plt.plot(theta_t[i],'r')
    plt.ylabel('theta_t')

    plt.show()

if __name__ == '__main__':

	total_bots = 2
	bot_loc = []
	real_cord = [[2,0],[0,0]]

	x_t,y_t,r_t,r_dot,theta_t,total_time,sampling_rate = trajectory_gen(total_bots)
	#print x_t#,y_t,r_t,r_dot,theta_t,total_time,sampling_rate
	print x_t[0][0],y_t[0][0],x_t[1][0],y_t[1][0]#,x_t[2][0],y_t[2][0],x_t[3][0],y_t[3][0]
	for i in range(total_bots):
		bot_loc.append([])
		for j in range(len(real_cord)):
			bot_loc[i].append(math.sqrt((x_t[j][0]-real_cord[i][0])*(x_t[j][0]-real_cord[i][0])+(y_t[j][0]-real_cord[i][1])*(y_t[j][0]-real_cord[i][1])))
	swarm_algo(total_bots,bot_loc)
	plotting(x_t,y_t,r_t,r_dot,theta_t,total_bots)
    
