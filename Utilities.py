# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:05:23 2021

@author: lukem
"""
import os
import numpy as np
from scipy import linalg
import pandas as pd
import torch

def write_shape(filename, shape):
    shape_np = shape.numpy()
    shape_df = pd.DataFrame(shape_np)
    shape_df.to_csv(filename)
    
    
def get_shape_yaml(file):
    with open(file, 'r') as file:
        for i,line in enumerate(file): 
            if i > 0:
                # print('i = ',i)
                # print('line = ', line)
                if i == 1:
                    temp = (line[:]).split(',')
                    point_temp = np.array([int(float(temp[1])), int(float(temp[2])), int(float(temp[0])+1)])
                    shape = torch.from_numpy(point_temp).view(1,3)
                else:
                    temp = (line[:]).split(',')
                    point_temp = np.array([int(float(temp[1])), int(float(temp[2])), int(float(temp[0])+1)])
                    point_temp = torch.from_numpy(point_temp).view(1,3)
                    shape = torch.cat((shape, point_temp), -2)
        
    return shape
    
def save_txt_file(file_name,shape,circle_left,circle_right, boundingbox):
    
    #save the file name, landmarks and iris position into a txt file
    
    file_no_ext=file_name[0:-4]
    delimiter = os.path.sep
    temp=file_name.split(delimiter)
    photo_name=temp[-1]
    
    #create temporaty files with the information from the landamarks and 
    #both eyes
    #this piece is a bit weird, it creates three temporary files that are used
    #to create the final file, these files are then eliminated. This is
    #simplest (and easiest) way that i found to do this
    np.savetxt(file_no_ext +'_temp_shape.txt', shape, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_circle_left.txt', circle_left, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_circle_right.txt', circle_right, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_boundingbox.txt', boundingbox, delimiter=',',
                   fmt='%i', newline='\r')
        
    #create a new file that will contain the information, the file will have 
    #the same name as the original picture 
    #if the file exists then remove it -- sorry
    if os.path.isfile(file_no_ext+'.txt'):
        os.remove(file_no_ext + '.txt')           
        
    #now start writing in it
    with open(file_no_ext + '.txt','a') as f:
        #start writing content in the file 
        #(\n indicates new line), (# indicates that the line will be ignored)
        f.write('# File name { \n')
        f.write(photo_name)
        f.write('\n# } \n')
        
        f.write('# Facial Landmarks [x,y] { \n')
        with open(file_no_ext +'_temp_shape.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Left iris [x,y,r] { \n')
        with open(file_no_ext + '_temp_circle_left.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Right iris [x,y,r] { \n')
        with open(file_no_ext + '_temp_circle_right.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Face bounding Box [top(x), left(y), width, height] { \n')
        with open(file_no_ext + '_temp_boundingbox.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# }')
        
    
    os.remove(file_no_ext +'_temp_shape.txt')
    os.remove(file_no_ext + '_temp_circle_left.txt')
    os.remove(file_no_ext + '_temp_circle_right.txt')
    os.remove(file_no_ext + '_temp_boundingbox.txt')

def get_info_from_txt(file):
    #function to read the landmark, iris and bounding box location from txt files
    # print('Using Saved Dots')
    shape = None
    left_pupil = np.zeros((1,3),dtype=int)
    right_pupil = np.zeros((1,3),dtype=int)
    bounding_box = np.zeros((1,4),dtype=int)
    
    getting_Landmarks = False
    gotten_Landmarks = False
    ID_count = 1
    
    getting_lefteye = False
    gotten_lefteye = False
    count_lefteye = 0
    
    getting_righteye = False
    gotten_righteye = False
    count_righteye = 0
    
    getting_boundingbox = False
    gotten_boundingbox = False
    count_box = 0
    
    waiting = False
    
    with open(file, 'r') as file:
        for i,line in enumerate(file):    
            #Skips first 3 lines as those are the file name info
            if i > 3:
                temp = (line[:-1]).split(',')
                if temp[0].isnumeric():
                    
                        
                        if i == 4: 
                            #Once at the 4th line, it starts collecting shape
                            #(It is the 4th line every time)
                            #All other line numbers depend on the amount of landmarks saved
                            getting_Landmarks = True
                            
                        if getting_Landmarks == True:
                            if len(temp) == 3:
                                #If the txt file has a label saved right it
                                point_temp = np.array([int(temp[0]), int(temp[1]), int(temp[2])])
                                point_temp = torch.from_numpy(point_temp).view(1,3)
                                #If its the first line, it creates the shape
                                if shape is None:
                                    shape = point_temp
                                #If not, it adds it to the previously collected shape info
                                else:
                                    shape = torch.cat((shape, point_temp), -2)
                            if len(temp) == 2:
                                #If the txt file doesn't have a label column, fill it in
                                point_temp = np.array([int(temp[0]), int(temp[1]), int(ID_count)])
                                ID_count = ID_count + 1 #keeps track of IDs
                                point_temp = torch.from_numpy(point_temp).view(1,3)
                                #If its the first line, it creates the shape
                                if shape is None:
                                    shape = point_temp
                                #If not, it adds it to the previously collected shape info
                                else:
                                    shape = torch.cat((shape, point_temp), -2)
                                
                        if getting_lefteye == True:
                            left_pupil[0, count_lefteye] = int(temp[0])
                            count_lefteye += 1
                        
                        if getting_righteye == True:
                            right_pupil[0, count_righteye] = int(temp[0])
                            count_righteye += 1
                        
                        if getting_boundingbox == True:
                            bounding_box[0, count_box] = int(temp[0])
                            count_box += 1
                            
                            
                else:
                    #If the line is not numeric, then it has hit a new section. Therefore, it will evaluate
                    #which section was just completed
                    if waiting == False:
                        if getting_Landmarks == True:
                            gotten_Landmarks = True
                            getting_Landmarks = False
                            waiting = True
                        
                        elif getting_lefteye == True:
                            gotten_lefteye = True
                            getting_lefteye = False
                            waiting = True
                            
                        elif getting_righteye == True:
                            gotten_righteye = True
                            getting_righteye = False
                            waiting = True
                            
                        elif getting_boundingbox == True:
                            gotten_boundingbox = True
                            getting_boundingbox = False
                            waiting = True
                            
                        else:
                            pass
                            
                    elif waiting == True:
                        #Since there is only every 2 lines inbetween each section 
                        #and the first line is when the waiting is turned turn,
                        #the waiting variable can be immediately turned back to False
                        waiting = False
                        #Then the section that is next must be found
                        if gotten_lefteye == False:
                            getting_lefteye = True
                            
                        elif gotten_righteye == False:
                            getting_righteye = True
                            
                        elif gotten_boundingbox == False:
                            getting_boundingbox =True
                        
                        else:
                            pass
    
    lefteye = [left_pupil[0,0], left_pupil[0,1], left_pupil[0,2]]
    righteye = [right_pupil[0,0], right_pupil[0,1], right_pupil[0,2]]
    boundingbox = [bounding_box[0,0],bounding_box[0,1],bounding_box[0,2],bounding_box[0,3]]    
       
           
    return shape, lefteye, righteye, boundingbox

    
def find_circle_from_points(x,y):
    #this function finds the center and radius of a circle from a set of points 
    #in the circle. x and y are the coordinates of the points. 
    
    # coordinates of the barycenter
    x_m = np.mean(x)
    y_m = np.mean(y)

    # calculation of the reduced coordinates
    u = x - x_m
    v = y - y_m

    # linear system defining the center (uc, vc) in reduced coordinates:
    #    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
    #    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
    Suv  = sum(u*v)
    Suu  = sum(u**2)
    Svv  = sum(v**2)
    Suuv = sum(u**2 * v)
    Suvv = sum(u * v**2)
    Suuu = sum(u**3)
    Svvv = sum(v**3)

    # Solving the linear system
    A = np.array([ [ Suu, Suv ], [Suv, Svv]])
    B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
    uc, vc = linalg.solve(A,B)

    xc_1 = x_m + uc
    yc_1 = y_m + vc

    # Calcul des distances au centre (xc_1, yc_1)
    Ri_1     = np.sqrt((x-xc_1)**2 + (y-yc_1)**2)
    R_1      = np.mean(Ri_1)

    
    circle=[int(xc_1),int(yc_1),int(R_1)]
    #circle.append((int(xc_1),int(yc_1),int(R_1)))
    
    return circle    


def save_xls_file(file_name, MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual):
    #saves the facial metrics into a xls file. It works only for a single photo
    
    file_no_ext=file_name[0:-4]
    delimiter = os.path.sep
    temp=file_name.split(delimiter)
    photo_name=temp[-1]
    
    number_of_measurements = 12
    Columns = ['Right','Left','Deviation (absolute)','Deviation (percent)']
    Columns = Columns * number_of_measurements
    
    temp = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Palpebral Fissure Height', 'Eye Area', 'NLF Angle',
            'Upper Lip Slope', 'Commisure Height', 'Interlabial Distance',
            'Interlabial Area of the Hemiface','Commissure Position','Lower Lip Height']
    number_of_repetitions=4
    Header = [item for item in temp for i in range(number_of_repetitions)]
    
    
    elements = ['BH', 'MRD1', 'MRD2', 'PFH', 'EA', 'NA', 'ULS', 'CH', 'ID', 'IAH', 'CP', 'LLH']
    BH = np.array([[MeasurementsRight.BrowHeight,MeasurementsLeft.BrowHeight,MeasurementsDeviation.BrowHeight,MeasurementsPercentual.BrowHeight]],dtype=object)
    MRD1 = np.array([[MeasurementsRight.MarginalReflexDistance1, MeasurementsLeft.MarginalReflexDistance1,MeasurementsDeviation.MarginalReflexDistance1,MeasurementsPercentual.MarginalReflexDistance1]], dtype=object)
    MRD2 = np.array([[MeasurementsRight.MarginalReflexDistance2, MeasurementsLeft.MarginalReflexDistance2,MeasurementsDeviation.MarginalReflexDistance2,MeasurementsPercentual.MarginalReflexDistance2]],dtype=object)
    PFH = np.array([[MeasurementsRight.PalpebralFissureHeight, MeasurementsLeft.PalpebralFissureHeight,MeasurementsDeviation.PalpebralFissureHeight,MeasurementsPercentual.PalpebralFissureHeight]],dtype=object)
    EA = np.array([[MeasurementsRight.EyeArea, MeasurementsLeft.EyeArea,MeasurementsDeviation.EyeArea,MeasurementsPercentual.EyeArea]],dtype=object)
    NA = np.array([[MeasurementsRight.NLF_angle, MeasurementsLeft.NLF_angle,MeasurementsDeviation.NLF_angle,MeasurementsPercentual.NLF_angle]],dtype=object)
    ULS = np.array([[MeasurementsRight.UpperLipSlope, MeasurementsLeft.UpperLipSlope,MeasurementsDeviation.UpperLipSlope,MeasurementsPercentual.UpperLipSlope]],dtype=object)
    CH = np.array([[MeasurementsRight.CommisureHeight, MeasurementsLeft.CommisureHeight,MeasurementsDeviation.CommisureHeight,MeasurementsPercentual.CommisureHeight]],dtype=object)
    ID = np.array([[MeasurementsRight.InterlabialDistance, MeasurementsLeft.InterlabialDistance,MeasurementsDeviation.InterlabialDistance,MeasurementsPercentual.InterlabialDistance]],dtype=object)
    IAH = np.array([[MeasurementsRight.InterlabialArea_of_the_Hemiface,MeasurementsLeft.InterlabialArea_of_the_Hemiface,MeasurementsDeviation.InterlabialArea_of_the_Hemiface,MeasurementsPercentual.InterlabialArea_of_the_Hemiface]],dtype=object)
    CP = np.array([[MeasurementsRight.CommissurePosition,MeasurementsLeft.CommissurePosition,MeasurementsDeviation.CommissurePosition,MeasurementsPercentual.CommissurePosition]],dtype=object)
    LLH = np.array([[MeasurementsRight.LowerLipHeight,MeasurementsLeft.LowerLipHeight,MeasurementsDeviation.LowerLipHeight,MeasurementsPercentual.LowerLipHeight]],dtype=object)
    
    
    
    fill=BH
    for i in elements:
        if i is not 'BH':
            fill = np.append(fill, eval(i), axis = 1)
    
    
    
    Index = [photo_name]
    
    
    df = pd.DataFrame(fill, index = Index, columns = Columns)
    df.columns = pd.MultiIndex.from_tuples(list(zip(Header,df.columns)))
    
    
    df.to_excel(file_no_ext+'.xlsx',index = True)