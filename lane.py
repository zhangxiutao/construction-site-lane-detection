#!/usr/bin/env python
"""Departure Warning System with a Monocular Camera"""

__author__ = "Junsheng Fu"
__email__ = "junsheng.fu@yahoo.com"
__date__ = "March 2017"


import numpy as np
import cv2
import matplotlib.pyplot as plt
import cnn_classifier
from timeit import default_timer as timer
from calibration import load_calibration
from copy import copy

leitbake_detector = cnn_classifier.CnnClassifier()

def process_frame(img_cv2, visualization=False):

    start = timer()

    #height, width = img_cv2.shape[0:2]
    #img_cv2 = img_cv2[int(height/2):height,0:width,:]
    
    # resize the input image according to scale
    detections = leitbake_detector.leibake_detect(img_cv2)
    for (x1,y1,x2,y2) in detections:
        cv2.rectangle(img_cv2,(x1,y1),(x2,y2),(255,0,0),2)
    cv2.imshow("leitbake_detected",img_cv2)
    cv2.waitKey(1)
    end = timer()
    print "fps is {}".format(1/(end-start))
    return detections
    



