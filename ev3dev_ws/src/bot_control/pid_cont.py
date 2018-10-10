#!/usr/bin/env python

import rospy
import math
import threading
from geometry_msgs.msg import Twist,Pose2D
from nav_msgs.msg import Odometry
from std_msgs.msg import String

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

def PID(vx,wt,set_vx,set_wt,diff_vx1,diff_wt1):
    KP = 3.5
    KD = 1.5                 

    diff_vx2 = set_vx-vx
    diff_wt2 = set_wt-wt
    vx = vx + 0.3*(KP*diff_vx2 - KD*(diff_vx2-diff_vx1)/(KP*1+KD*1))
    wt = wt + 0.1*(KP*diff_wt2 - KD*(diff_wt2-diff_wt1)/(KP*1+KD*1))
    diff_vx1 = diff_vx2
    diff_wt1 = diff_wt2
    print(diff_vx1)
    print(diff_wt1)

    return vx,wt,diff_vx1,diff_wt1

if __name__ == '__main__':

    diff_vx_1 = 0
    diff_wt_1 = 0
    set_vx_1 = 0.1
    set_wt_1 = 0

    rospy.init_node('serial_node', anonymous=True)
    rate = rospy.Rate(100)
    pub = rospy.Publisher('/turtlebot_teleop/cmd_vel',Twist,queue_size=10)
    twist = Twist()

    while(1):
        vel = speed()
        rospy.Subscriber("/odom",Odometry,vel)
        vx_1,wt_1 = vel.get_msg()

        vx_1,wt_1,diff_vx_1,diff_wt_1 = PID(vx_1,wt_1,set_vx_1,set_wt_1,diff_vx_1,diff_wt_1)

        twist.linear.x = vx_1
        twist.angular.z = wt_1
        pub.publish(twist)
