#!/usr/bin/env python

import rospy
from std_msgs.msg import String

journalism=rospy.Publisher('Prime_Time_Debates',String,queue_size=1)
# subscribe to content selection 
# subscribe to Fake news
def listen():
    rospy.init_node('Journalist',anonymous=True)
    rospy.Subscriber('Fake_News',String,listen_fake)
    rospy.Subscriber('Content_Selection',String,listen_content)

    rospy.spin()


# Publish to prime time debates
def listen_fake(data):
    debates='Welcome to some Loud Exciting Masala Fake News with Shouting retards'
    fake=str(data.data)
    fake=fake[-6:-1]
    
    journalism.publish(debates+fake)

def listen_content(data):
    debates='We will shout about: '
    content=str(data.data)
    content=content[-10:-1]
    
    journalism.publish(debates+content)


if __name__ == '__main__':
    try:
        listen()
    except rospy.ROSInterruptException:
        pass