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

def PID(vx,wt,set_vx,set_wt,diff_vx1,diff_wt1):
    KP = 3.5
    KD = 1.5                 

    diff_vx2 = set_vx-vx
    diff_wt2 = set_wt-wt
    vx = vx + 0.3*(KP*diff_vx2 + KD*(diff_vx2-diff_vx1)/(KP*1+KD*1))
    wt = wt + 0.1*(KP*diff_wt2 + KD*(diff_wt2-diff_wt1)/(KP*1+KD*1))
    diff_vx1 = diff_vx2
    diff_wt1 = diff_wt2

    return vx,wt,diff_vx1,diff_wt1

if __name__ == '__main__':

    diff_vx_1 = 0
    diff_wt_1 = 0
    set_vx_1 = 0.1
    set_wt_1 = 0

    rospy.init_node('mocap_node', anonymous=True)
    #rospy.init_node('serial_node', anonymous=True)
    rate = rospy.Rate(100)

    pose = coord()
    rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
    x_1,y_1,theta_1 = pose.get_msg()
    print(x_1,y_1,theta_1)

    pub = rospy.Publisher('/turtlebot_teleop/cmd_vel',Twist,queue_size=10)
    twist = Twist()

    (x_t,y_t) = (2778.245,750.101)
    theta_t = math.degrees(math.atan((y_t-y_1)/(x_t-x_1)))
    if x_t > x_1:
        if theta_t >= 0:
            theta_t = theta_t
        else:
            theta_t = 360 + theta_t
    else:
        if theta_t >= 0:
            theta_t = 180 + theta_t
        else:
            theta_t = 90 - theta_t 

    while not rospy.is_shutdown():

        if theta_t <= 180:
            if theta_t < theta_1 < theta_t+180:         # CCW
                mode = 'CCW'
            else:                                       # CW
                mode = 'CW'

        elif theta_t > 180:                             
            if theta_t-180 < theta_1 < theta_t:         # CCW
                mode = 'CW'
            else:                                       # CW
                mode = 'CCW'
        while(1):
            pose = coord()
            rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
            x_1,y_1,theta_1 = pose.get_msg()

            theta_err = theta_t - theta_1
            if abs(theta_err) < 3:
                twist.angular.z = 0
                pub.publish(twist)
                break
            wt = 0.4
            if mode == 'CW':
                twist.angular.z = -wt
                pub.publish(twist)
            else:
                twist.angular.z = wt
                pub.publish(twist)
        while(1):
            pose = coord()
            rospy.Subscriber("/Robot_1/ground_pose",Pose2D,pose)
            x_1,y_1,theta_1 = pose.get_msg()

            dist = math.sqrt((x_t-x_1)**2+(y_t-y_1)**2)
            if dist < 50 :
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
                break

            vel1 = speed()
            rospy.Subscriber("/odom_1",Odometry,vel)
            vx_1,wt_1 = vel.get_msg()

            wt_1,theta_old1_err,theta_i1_err = go_to_goal(wt_1,theta_t,theta_1,theta_old1_err,theta_i1_err)
            twist.linear.x = vx_1
            twist.angular.z = wt_1
            pub.publish(twist)

            pose = coord()
            rospy.Subscriber("/Robot_2/ground_pose",Pose2D,pose)
            x_2,y_2,theta_2 = pose.get_msg()

            dist = math.sqrt((x_t-x_2)**2+(y_t-y_2)**2)
            if dist < 50 :
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
                break

            vel1 = speed()
            rospy.Subscriber("/odom_2",Odometry,vel)
            vx_2,wt_2 = vel.get_msg()

            wt_1,theta_old1_err,theta_i1_err = go_to_goal(wt_1,theta_t,theta_1,theta_old1_err,theta_i1_err)
            twist.linear.x = vx_1
            twist.angular.z = wt_1
            pub.publish(twist)


        print('hooray')
        break
        #twist.linear.x = 0.5
        #pub.publish(twist)
        #rate.sleep()
