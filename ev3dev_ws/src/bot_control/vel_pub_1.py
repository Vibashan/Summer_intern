#!/usr/bin/env python 

import rospy
import sys
import math
from geometry_msgs.msg import Twist

if __name__ == '__main__':

    pub = rospy.Publisher('/cf1/cmd_vel',Twist,queue_size=10)
    rospy.init_node('rviz')
    rate = rospy.Rate(10)
    twist = Twist()
    while not rospy.is_shutdown():
    	print '1'
        twist.linear.z = 0.5
        pub.publish(twist)
        rate.sleep()


