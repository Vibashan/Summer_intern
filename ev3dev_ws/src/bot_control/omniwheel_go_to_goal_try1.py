#!/usr/bin/env python

import rospy
import math
import threading
from geometry_msgs.msg import Twist,Pose2D
from nav_msgs.msg import Odometry
from std_msgs.msg import String

class coord(object):
    def __init__(self):
        self._event = threading.Event()
        self.x = None
        self.y = None
        self.theta = None

    def __call__(self, msg):
        self.x = msg.x*1000
        self.y = -msg.y*1000
        self.theta = -math.degrees(msg.theta)
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

def go_to_goal(x_1,y_1,x_error1,y_error1):
    Kp_x = 1.2
    Kd_x = 0.8
    if abs(x_error1) > 100:
        x_error2 = x_t-x_1
        x_d_err = x_error1 - x_error2
        x_pid = (Kp_x*x_error2 + Kd_x*x_d_err )/(Kp_x*4000+Kd_x*4000)
        x_error1 = x_error2

        if abs(x_pid) > 0.2:
            if x_pid < 0:
                x_pid = -0.2
            elif x_pid > 0:
                x_pid = 0.2
        if abs(x_pid) < 0.03:
            if x_pid < 0:
                x_pid = -0.03
            elif x_pid > 0:
                x_pid = 0.03
    else:
        x_pid = 0

    if abs(y_error1) > 100:       
        Kp_y = 1.2
        Kd_y = 0.8  
        y_error2 = y_t-y_1
        y_d_err = y_error1 - y_error2
        y_pid = (Kp_y*y_error2 + Kd_y*y_d_err )/(Kp_y*4000+Kd_y*4000)
        y_error1 = y_error2

        if abs(y_pid) > 0.2:
            if y_pid < 0:
                y_pid = -0.2
            elif y_pid > 0:
                y_pid = 0.2
        if abs(y_pid) < 0.03:
            if y_pid < 0:
                y_pid = -0.03
            elif y_pid > 0:
                y_pid = 0.03
    else:
        y_pid = 0
    
    x_dot = (0.1*x_pid)/math.sqrt(x_pid*x_pid+y_pid*y_pid)
    y_dot = (0.1*y_pid)/math.sqrt(x_pid*x_pid+y_pid*y_pid)

    print('x_dot-',x_dot,'y_dot-',y_dot)

    return x_dot,y_dot,x_error1,y_error1    

if __name__ == '__main__':

    x_dot = 0
    y_dot = 0
    x_error1 = 300
    y_error1 = 300
    wt_1 = 0

    rospy.init_node('mocap_node', anonymous=True)
    rate = rospy.Rate(100)

    pose = coord()
    rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
    x_1,y_1,theta_1 = pose.get_msg()
    print(x_1,y_1,theta_1)

    pub = rospy.Publisher('/turtlebot_teleop_1/cmd_vel',Twist,queue_size=10)
    twist = Twist()

    (x_t,y_t) = (3000,1000)

    while not rospy.is_shutdown():
        while(1):
            pose = coord()
            rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
            x_1,y_1,theta_1 = pose.get_msg()

            if abs(x_t-x_1) < 100 and (y_t-y_1) < 100:
                twist.linear.x = 0
                twist.linear.y = 0
                twist.angular.z = 0
                pub.publish(twist)
                break

            x_dot,y_dot,x_error1,y_error1 = go_to_goal(x_1,y_1,x_error1,y_error1)
            twist.linear.x = x_dot
            twist.linear.y = y_dot
            twist.angular.x = theta_1
            twist.angular.z = wt_1
            pub.publish(twist)

        print('hooray')
        break
