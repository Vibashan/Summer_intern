#!/usr/bin/env python

import rospy
import math
import threading
import tf
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

def go_to_goal(wt,theta_tar,theta_now,theta_err1,theta_i_err):
    Kp = 4
    Kd = 1
    Ki = 3
    thresh_i = 2*math.pi

    theta_err2 = math.atan2(math.sin(math.pi*(theta_tar-theta_now)/180),math.cos(math.pi*(theta_tar-theta_now)/180))
    theta_d_err = theta_err1 + theta_err2
    if abs(theta_err2) < 0.02:
        theta_i_err = 0 
    theta_i_err = theta_i_err + theta_err2
    if theta_i_err < -thresh_i:
        theta_i_err = -thresh_i
    elif theta_i_err > thresh_i:
        theta_i_err = thresh_i
    wt = math.pi*((Kp*theta_err2 + Kd*theta_d_err + Ki*theta_i_err)/(Kp*2*math.pi+Kd*math.pi+Ki*thresh_i))
    theta_err1 = theta_err2
    return wt,theta_err1,theta_i_err

if __name__ == '__main__':

    vx_1 = 0.5
    wt_1 = 0
    theta_old1_err = 0
    theta_i1_err = 0

    rospy.init_node('mocap_node', anonymous=True)
    #rospy.init_node('robot_state_publisher', anonymous=True)
    rate = rospy.Rate(100)

    pose = coord()
    rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
    x_1,y_1,theta_1 = pose.get_msg()
    print(x_1,y_1,theta_1)

    pub = rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=10)
    twist = Twist()

    (x_t,y_t) = (479.792,2407.711)
    theta_t = math.degrees(math.atan2((y_t-y_1),(x_t-x_1)))
    if theta_t >= 0:
        theta_t = theta_t
    else:
        theta_t = 360 + theta_t

    while not rospy.is_shutdown():
        while(1):
            pose = coord()
            rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
            x_1,y_1,theta_1 = pose.get_msg()

            if abs(x_t-x_1) < 0.1 and abs(y_t-y_1) < 0.1:
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
                break

            theta_t = math.degrees(math.atan2((y_t-y_1),(x_t-x_1)))
            if theta_t >= 0:
                theta_t = theta_t
            else:
                theta_t = 360 + theta_t

            wt_1,theta_old1_err,theta_i1_err = go_to_goal(wt_1,theta_t,theta_1,theta_old1_err,theta_i1_err)
            print 'x',x_1,'y',y_1,'wt',wt_1,'theta_tar',theta_t,'theta_now',theta_1,'theta_i',theta_i1_err,'theta_old',theta_old1_err
            print vx_1,wt_1
            twist.linear.x = vx_1
            twist.angular.z = wt_1
            pub.publish(twist)

        print'hooray'
        break
