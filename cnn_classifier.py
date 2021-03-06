# Import the required modules
from __future__ import division
import cv2
import argparse as ap
from config import *
import numpy as np

import torch
import torchvision.transforms as transforms
import torchvision.ops as ops
import torch.nn
import os.path
import cnn
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import uuid
import time

patch_size = min_wdw_sz[0]*min_wdw_sz[1]

class CnnClassifier:

    def __init__(self):

        test_on_gpu = torch.cuda.is_available()
        self.model = cnn.Net()
        if test_on_gpu:
            self.model.cuda()
        self.model.double()
        self.model.load_state_dict(torch.load("./src/construction-site-lane-detection/models/nn_model.pt"))
        self.model.eval()

    def sliding_window(self, image, window_size, step_size):

        for y in xrange(0, image.size[0], step_size[1]):
            for x in xrange(0, image.size[1], step_size[0]):
                if (x+window_size[0]) <= image.size[1] and (y+window_size[1]) <= image.size[0]:
                    window = image.crop((x,y,x + window_size[0],y + window_size[1]))
                    yield (x,y,window)

    def leibake_detect(self, img_cv2):

        img_cv2 = cv2.cvtColor(img_cv2,cv2.COLOR_BGR2RGB)
        img_origin = Image.fromarray(img_cv2) #convert to PIL image

        # List to store the detections
        detections = []
        scores = []
        # The current scale of the image
        scale = 0

        toTensor = transforms.ToTensor()
        norm = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

        # This list contains detections at the current scale
        cd = []
        count = 1          
        for (x, y, im_window) in self.sliding_window(img_origin, min_wdw_sz, step_size):

            data = toTensor(im_window)
            data = data.double()[:3,:,:]
            data = norm(data)
            data = data.unsqueeze(0)
            data = data.cuda()
            output = torch.max(self.model(data), 1)

            if 1 == int(output[1]):
                fileName = uuid.uuid4().hex+".png"
                filePath = "./src/construction-site-lane-detection/detectedWindows/" + fileName
                print(filePath)
                im_window.save(filePath)
                print "Detection:: Location -> ({}, {})".format(x, y)
                detections.append((x, y, x+int(min_wdw_sz[0]), y+int(min_wdw_sz[1])))
                scores.append(output[0])
                cd.append(detections[-1])
                count=count+1

        detections = torch.tensor(detections).double()
        scores = torch.tensor(scores)
        
        if len(detections) != 0:
            detections_nms_idx = ops.nms(detections,scores,0.2)
            detections_nms = [detections[i] for i in detections_nms_idx]
        else:
            detections_nms = []

        return detections_nms	
        

def checkIfWanted(img):

    img = util.img_as_ubyte(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #red mask0
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv,lower_red,upper_red)
    #red mask1
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv,lower_red,upper_red)

    mask_red = mask0 + mask1
    res_red = cv2.bitwise_and(img, img, mask=mask_red)

    #erosion
    erosionKernel = np.ones((5,5),np.uint8)
    erosion_red = cv2.erode(res_red,erosionKernel)
    bw_image_red = cv2.cvtColor(cv2.cvtColor(erosion_red, cv2.COLOR_HSV2BGR), cv2.COLOR_RGB2GRAY)

    #black mask0
    lower_black = np.array([0,0,0]) 
    upper_black = np.array([180,255,46]) 
    mask_black = cv2.inRange(img_hsv,lower_black,upper_black)
    res_black = cv2.bitwise_and(img, img, mask=mask_black)
    res_black = cv2.cvtColor(res_black, cv2.COLOR_BGR2GRAY)
    #erosion
    #erosionKernel = np.ones((5,5),np.uint8)
    #erosion_black = cv2.erode(res_black,erosionKernel)
    #bw_image_black = cv2.cvtColor(cv2.cvtColor(erosion_black, cv2.COLOR_HSV2BGR), cv2.COLOR_RGB2GRAY)


    #print(cv2.countNonZero(bw_image_red))
    #print(patch_size)

    # if cv2.countNonZero(bw_image_red)/patch_size < 0.25 or cv2.countNonZero(bw_image_red)/patch_size > 0.5:
        
    #     return False
    # else:
    #     return True
    return True


    return 
