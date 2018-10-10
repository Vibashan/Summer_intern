#!/usr/bin/env python

import rospy
import math
import threading
import time
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

if __name__ == '__main__':

    rospy.init_node('mocap_node', anonymous=True)
    rate = rospy.Rate(100)

    pose = coord()
    rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
    x_1,y_1,theta_1 = pose.get_msg()
    print(x_1,y_1,theta_1)

    pub = rospy.Publisher('/turtlebot_teleop_1/cmd_vel',Twist,queue_size=10)
    twist = Twist()

    (x_t,y_t) = (479.792,2407.711)

    while not rospy.is_shutdown():
        while(1):
            pose = coord()
            rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
            x_1,y_1,theta_1 = pose.get_msg()
            print(theta_1)

            twist.linear.x = 0
            twist.linear.y = -0.1
            twist.angular.x = theta_1
            twist.angular.z = 0
            pub.publish(twist)
            time.sleep(0.01)

        print('hooray')
        break
