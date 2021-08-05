#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import String

# publish Money
def send_money():
    #send money to make biased content on TV News
    gov=rospy.Publisher('Money',String,queue_size=1)
    rospy.init_node('Government')
    rate=rospy.Rate(0.2) #once every 5 seconds
    
    while not rospy.is_shutdown():
        money='This is '+str(1000*random.randint(1,9))+' Rupees for you to advertise my policies I am paying you So,do not recheck facts. ;) '
        gov.publish(money)
        rate.sleep()


if __name__ == '__main__':
    try:
        send_money()
    except rospy.ROSInterruptException:
        pass