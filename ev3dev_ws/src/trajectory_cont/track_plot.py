#!/usr/bin/env python

import rospy
import math
import threading
import tf
import time
import matplotlib.pyplot as plt
import numpy as np

from geometry_msgs.msg import Twist,Pose2D
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from sympy import Symbol, Derivative

class coord(object):
    def __init__(self):
        self._event = threading.Event()
        self.x = None
        self.y = None
        self.theta = None

    def __call__(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]
        self.theta = math.degrees(yaw)
        if self.theta >= 0:
          self.theta = self.theta
        else:
          self.theta = 360 + self.theta          
        self._event.set()

    def get_msg(self, timeout=None):
        self._event.wait(timeout)
        return self.x,self.y,self.theta

class speed(object):
    def __init__(self):
        self._event = threading.Event()
        self.vx = None
        self.wt = None

    def __call__(self, msg):
        self.vx = msg.twist.twist.linear.x
        self.wt = msg.twist.twist.angular.z
        self._event.set()

    def get_msg(self, timeout=None):
        self._event.wait(timeout)
        return self.vx,self.wt

def path_planning(t,mode):
    x = t
    y = 3*math.sin((t*math.pi)/8)
    x_dot = 1
    y_dot = ((3*math.pi)/8)*math.cos((t*math.pi)/8)

    r_t = math.sqrt(x*x+y*y)
    if r_t == 0:
        r_t = 0.000001
    r_dot = (x*x_dot+y*y_dot)/(r_t)
    theta_t = math.atan2(y_dot,x_dot)

    if mode == "r_dot":
        return r_dot
    elif mode == "x_axis":
        return x
    elif mode == "y_axis":
        return y
    elif mode == "r_t":
        return r_t

def trajectory_gen():
    total_time = 20
    sampling_rate = 0.25
    x_t,y_t = [],[]
    r_t,r_dot = [],[]
    theta_t = []
    for i in range(int(total_time/sampling_rate)):
        x_t.append(path_planning(i*sampling_rate,"x_axis"))
        y_t.append(path_planning(i*sampling_rate,"y_axis"))
        r_t.append(path_planning(i*sampling_rate,"r_t"))
        r_dot.append(path_planning(i*sampling_rate,"r_dot"))
    return x_t,y_t,r_t,r_dot,total_time,total_time,sampling_rate

def trajectory_track(r_dot,r_t,theta_t,r_act,theta_act,r_int_er,r_old_er,theta_int_er,theta_old_er):
    Kp_ln, Kd_ln, Ki_ln = 2,3,0.2
    r_er = r_t - r_act
    r_diff_er = r_er - r_old_er
    r_int_er = r_er + r_int_er
    PID_ln = r_dot + (Kp_ln*r_er + Kd_ln*r_diff_er + Ki_ln*r_int_er)/(Kp_ln*2+Kd_ln+Ki_ln*4)
    r_old_er = r_er

    Kp_ang, Kd_ang, Ki_ang = 18,5,2
    Kp_dev, Kd_dev, Ki_dev = 12,1,0
    thresh_i = 2*math.pi
    theta_er = math.atan2(math.sin(math.pi*(theta_t-theta_act)/180),math.cos(math.pi*(theta_t-theta_act)/180))
    theta_diff_er = theta_er - theta_old_er
    if abs(theta_er) < 0.1:
        theta_int_er = 0 
    theta_int_er = theta_int_er + theta_er
    PID_wt = math.pi*((Kp_ang*theta_er + Kd_ang*theta_diff_er + Ki_ang*theta_int_er)/(Kp_ang*3+Kd_ang+Ki_ang*thresh_i))#+0.6*(Kp_dev*r_er + Kd_dev*r_diff_er + Ki_dev*r_int_er)/(Kp_dev*2+Kd_dev+Ki_dev*4)
    PID_ln = PID_ln - 0.4*PID_wt*PID_ln
    theta_old_er = theta_er   

    return PID_ln,r_int_er,r_old_er,PID_wt,theta_int_er,theta_old_er

def plotting(x_t,x_act,y_t,y_act,r_t,r_now):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(x_t,'r')
    plt.plot(x_act,'g')
    plt.ylabel('X-axis')

    plt.subplot(212)
    plt.plot(y_t,'r')
    plt.plot(y_act,'g')
    plt.ylabel('Y-axis')

    plt.figure(2)
    plt.subplot(211)
    plt.plot(r_t,'r')
    plt.plot(r_now,'g')
    plt.ylabel('Y-axis')

    plt.show()

if __name__ == '__main__':

    rospy.init_node('mobile_base_nodelet_manager', anonymous=True)

    pub = rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=1)
    twist = Twist()

    x_t,y_t,r_t,r_dot,total_time,total_time,sampling_rate  = trajectory_gen()
    rate = rospy.Rate(1/sampling_rate)

    r_int_er,r_old_er,theta_int_er,theta_old_er,count = 0,0,0,0,0
    x_act,y_act = [],[]
    vx_act,vy_act = [],[]
    r_now = []

    while not rospy.is_shutdown():
        while(1):
            if count < int(total_time/sampling_rate):
                vel = speed()
                rospy.Subscriber("/odom",Odometry,vel)
                vx_r,wt_r = vel.get_msg()

                pose = coord()
                rospy.Subscriber("/odom",Odometry,pose)
                x_r,y_r,theta_r = pose.get_msg()
                x_act.append(x_r)
                y_act.append(y_r)

                r_act = math.sqrt(x_r*x_r+y_r*y_r)
                r_now.append(r_act)
                theta_t = math.degrees(math.atan2((y_t[count]),(x_t[count])))
                if theta_t >= 0:
                    theta_t = theta_t
                else:
                    theta_t = 360 + theta_t
            
                vx,r_int_er,r_old_er,wt,theta_int_er,theta_old_er = trajectory_track(r_dot[count],r_t[count],theta_t,r_act,theta_r,r_int_er,r_old_er,theta_int_er,theta_old_er)
                print r_dot[count],vx,r_t[count],r_act,theta_t,theta_r
                 
                twist.linear.x = vx
                twist.angular.z = wt
                pub.publish(twist)
                rate.sleep()
            else:
                print'hooray'
                plotting(x_t,x_act,y_t,y_act,r_t,r_now)
                break
            count = count+1
        break

        
