#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import random



# Publish to content selection
media=rospy.Publisher('Content_Selection',String,queue_size=1)

def content_selection(data):
    
    content='You will report only on content I advise to you, else leave this job. Given Content#' + str(random.randint(1,4)) + ' '

    media.publish(content)

def bias_media():
    # Subscribe to Money
    rospy.init_node('News_Channel')
    rospy.Subscriber('Money',String,content_selection)

    rospy.spin()

if __name__ == '__main__':
    try:
        bias_media()
    except rospy.ROSInterruptException:
        pass