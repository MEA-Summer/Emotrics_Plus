# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:37:08 2021

@author: lukem
"""
import numpy as np
#import cv2
from Eye_window import ProcessEye



def get_iris_manual(Image, shape, position):
    
    #function of obtain the iris manually, it ask the user to select 4 points 
    #around the iris
    shape = np.array(shape)
    
    #get the eye from the image 
    if position == 'left':
        #Left Eye
        x_left = shape[42,0]
        w_left = (shape[45,0]-x_left)
        y_left = min(shape[43,1],shape[44,1])
        h_left = (max(shape[46,1],shape[47,1])-y_left)
        Eye = Image.copy()
        Eye = Eye[(int(y_left-20)):(int(y_left+h_left+20)),(int(x_left-20)):(int(x_left+w_left+20))]
    elif position == 'right':
        x_right = shape[36,0]
        w_right = (shape[39,0]-x_right)
        y_right = min(shape[37,1],shape[38,1])
        h_right = (max(shape[41,1],shape[40,1])-y_right)
        Eye = Image.copy()
        Eye = Eye[(int(y_right-20)):(int(y_right+h_right+20)),(int(x_right-20)):(int(x_right+w_right+20))]
    
    #transform brg(opencv color scheme) to rbg (normal color scheme)
    #temp_image=Eye.copy()
    #temp_image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2RGB)
    
    #open the window to get the pupil
    # EyeWindow = ProcessEye(temp_image)
    EyeWindow = ProcessEye(Eye)
    EyeWindow.exec_()

    #return to full image coordinates 
    circle = EyeWindow._circle
    if circle is not None: #verify that the is something to return 
        if position == 'left':
            circle[0] = circle[0]+x_left-20
            circle[1] = circle[1]+y_left-20
        elif position == 'right':
            circle[0] = circle[0]+x_right-20
            circle[1] = circle[1]+y_right-20
                
        #return circle information to main window
        return circle
    else: #if the user didn't include the 4 points then return 'None'
        return None