#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import String

# publish to prime time and
# publish to fake news
def share_opinions():
    speaker=rospy.Publisher('Prime_Time_Debates',String,queue_size=10)
    share_fake=rospy.Publisher('Fake_News',String,queue_size=1)
    rospy.init_node('Opinionated_retard')
    rate=rospy.Rate(0.2) #once every 5 seconds
    
    while not rospy.is_shutdown():
        debate='I will shout and NOT let you speak, I have opinion on every subject. Lie#' +str(random.randint(1,9))
        speaker.publish(debate)
        fake='I have an opinion on this, I heard it from someone but this is definitely TRUE. Lie#' +str(random.randint(1,9)) + ' '
        share_fake.publish(fake)
        rate.sleep()


if __name__ == '__main__':
    try:
        share_opinions()
    except rospy.ROSInterruptException:
        pass