#!/usr/bin/env python

import rospy
import threading
import math
from geometry_msgs.msg import Pose2D
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
  
if __name__ == '__main__':

    rospy.init_node('mocap_node', anonymous=True)
    pose = coord()
    rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
    x_1,y_1,theta_1 = pose.get_msg()
    print (x_1,y_1,theta_1)
    
    pose = coord()
    rospy.Subscriber("/Robot_2/ground_pose",Pose2D,pose)
    x_2,y_2,theta_2 = pose.get_msg()
    #print (x_2,y_2,theta_2)

    rospy.spin()
    