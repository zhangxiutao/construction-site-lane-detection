#!/usr/bin/env python
from __future__ import print_function

# import roslib
# roslib.load_manifest('my_package')
import os
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from lane import *


class LeitbakeDetector:

  def __init__(self):
    print("init")
    #self.image_pub = rospy.Publisher("/image_leitbake",Image,queue_size=1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback, queue_size = 1)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape

    process_frame(cv_image)
    
    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)

def main(args):
  
  rospy.init_node('LeitbakeDetector', anonymous=True)
  ld = LeitbakeDetector()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)