#!/usr/bin/env python

import rospy
from skeleton_markers.msg import Skeleton
from math import copysign
import PyKDL as KDL
import time

import socket
import time 
port=5028
s=socket.socket()
s.bind(('0.0.0.0',port))
s.listen(1)
global data

print 'server started'

class TrackerCommand():
    def __init__(self):
        rospy.init_node('skeleton_markers', anonymous=True)
        rospy.on_shutdown(self.shutdown)
        
        # How frequently do we publish      
        self.rate = rospy.get_param("~command_rate", 1)
        rate = rospy.Rate(self.rate)
        
        # Subscribe to the skeleton topic.
        rospy.Subscriber('skeleton', Skeleton, self.skeleton_handler, queue_size = 1)
        
        # Store the current skeleton configuration in a local dictionary.
        self.skeleton = dict()
        #self.skeleton['confidence'] = dict()
        self.skeleton['position'] = dict()
        #self.skeleton['orientation'] = dict()
        
        while not rospy.is_shutdown():
            rate.sleep()
        
    def skeleton_handler(self, msg):
        for joint in msg.name:  
            #self.skeleton['confidence'][joint] = msg.confidence[msg.name.index(joint)]
            self.skeleton['position'][joint] = KDL.Vector(msg.position[msg.name.index(joint)].x, msg.position[msg.name.index(joint)].y, msg.position[msg.name.index(joint)].z)
            if joint == 'right_hand':
                if self.skeleton['position'][joint][0] > 0:
                    conn.send('1')
                    #time.sleep(0.01)
                elif self.skeleton['position'][joint][0] < 0:
                    conn.send('0')
                    #time.sleep(0.01)
                print self.skeleton['position'][joint]
            #self.skeleton['orientation'][joint] = msg.orientation[msg.name.index(joint)]

    def shutdown(self):
        rospy.loginfo("Shutting down Tracker Command Node.")
        
if __name__ == '__main__':
    while 1:
        conn,addr=s.accept()
        try:
            TrackerCommand()
        except rospy.ROSInterruptException:
            pass
    conn.close()    