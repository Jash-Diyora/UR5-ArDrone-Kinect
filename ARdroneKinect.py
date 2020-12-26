#!/usr/bin/env python

#libraries for kinect
import rospy
from skeleton_markers.msg import Skeleton
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point 
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Import sthe messages we're interested in sending and receiving
from geometry_msgs.msg import Twist      # for sending commands to the drone
from std_msgs.msg import Empty           # for land/takeoff/emergency
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback

# An enumeration of Drone Statuses
from drone_status import DroneStatus

p = Point()

y_left =0.00
y_right=0.00
x_right=0.00
z_right=0.00
y_torso=0.00
x_torso=0.00
z_torso=0.00

pose=Twist()
st=String()
lt=String()
rt=String()
def callback(msg):
   for joint in msg.name:           
            global st
            st=msg.name[0]
           
            p = msg.position[msg.name.index(joint)]
            global x_left
            global y_left
            global x_right
            global y_right
            global x_torso
            global y_torso
            if joint=="left_hand":
              y_left=p.y
              x_left=p.x
              z_left=p.z
              rospy.loginfo(joint)
            elif joint=="right_hand":
              y_right=p.y
              x_right=p.x
              z_right=p.z
              rospy.loginfo(joint)
            
            elif joint=="torso":
              x_torso=p.x
              z_torso=p.z
              y_torso=p.y
              rospy.loginfo(joint)


            x_right = x_right - x_torso
            rospy.loginfo(x_right)

   #rospy.loginfo(m)


def kinect_drone():
  pubLand=rospy.Publisher('/ardrone/land',Empty)
  pubReset   = rospy.Publisher('/ardrone/reset',Empty)
  pubTakeoff= rospy.Publisher('/ardrone/takeoff',Empty)
  pubCommand = rospy.Publisher('/cmd_vel',Twist)
  pub=rospy.Publisher('/turtle1/cmd_vel',Twist)

  rospy.Subscriber("/skeleton", Skeleton, callback)
  rospy.init_node('kinect_drone')
  
  
  
  
  global count
  global x_left
  global y_left
  global x_right
  global y_right
  global x_torso
  global y_torso
  lt="left_hand"
  
  r = rospy.Rate(10) # 10hz
  while not rospy.is_shutdown():
      
       uniq=Empty()
       vel=Twist()
       if y_left>0.10:      
            #left hand to take off   
            rospy.loginfo(p.y)
            pubTakeoff.publish(uniq)  
       
       else:
            #left hand to land
            pubLand.publish(uniq)  
       
       if y_right>0.44:
            #right hand pitch backward
            vel.linear.x=-0.15
            vel.linear.y=0
            vel.linear.z=0
            vel.angular.z=0
            pubCommand.publish(vel)
            pub.publish(vel)       
                
       elif y_right<-0.04:
            #right hand pitch forward
            vel.linear.x=0.15
            vel.linear.y=0
            vel.linear.z=0
            vel.angular.z=0
            pubCommand.publish(vel)
            pub.publish(vel)
       
       elif x_right>0.60 :

                #right hand roll right 
                vel.linear.x=0
                vel.linear.y=-0.20
                vel.linear.z=0
                vel.angular.z=0
                pubCommand.publish(vel)
                pub.publish(vel)

       elif x_right< 0.10:
                #right hand roll left
                vel.linear.x=0
                vel.linear.y=0.20
                vel.linear.z=0
                vel.angular.z=0
                pubCommand.publish(vel)
                pub.publish(vel)
       
       else:
           # no motion no command
           vel.linear.x=0
           vel.linear.y=0
           vel.linear.z=0
           vel.angular.z=0
           pubCommand.publish(vel)        
           pub.publish(vel)
       
       
       rospy.sleep(0.1)


if __name__ == '__main__':
    try:
        kinect_drone()
    except rospy.ROSInterruptException: 
        pass
