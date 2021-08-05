#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# publish Facts
def send_facts():
    #send money to make biased content on TV News
    rsc=rospy.Publisher('Facts',String,queue_size=10)
    rospy.init_node('Research_Scientific_Community')
    rate=rospy.Rate(0.1) #once every 10 seconds
    
    while not rospy.is_shutdown():
        fact='We have researched and surveyed on this topic an found out this, we have published a report on this. '
        rsc.publish(fact)
        rate.sleep()


if __name__ == '__main__':
    try:
        send_facts()
    except rospy.ROSInterruptException:
        pass