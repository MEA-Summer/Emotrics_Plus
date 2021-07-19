# -*- coding: utf-8 -*-
"""
Created on Tue May 25 12:28:48 2021

@author: lukem
"""

import numpy as np    
from scipy.interpolate import UnivariateSpline


def estimate_line(circle_left, circle_right):
    #function to estimate the line that connects the center of the eyes and a 
    #new, perpendicular line in the middle point.
        
    x_1=circle_right[0]
    y_1=circle_right[1]
    
    x_2=circle_left[0]
    y_2=circle_left[1]
    
    #find the point in the middle of the line
    x_m=((x_2-x_1)/2)+x_1
    m=(y_2-y_1)/(x_2-x_1)   
    y_m=(y_1+m*(x_m-x_1))
    
    #x_m=int(round(x_m,0))
    #y_m=int(round(y_m,0))
    points=[x_m,y_m]
    
    return m, points


def estimate_lines(InputImage,circle_left, circle_right):
    #function to estimate the line that connects the center of the eyes and a 
    #new, perpendicular line in the middle
    
    h, w, _ = InputImage.shape
    
    circle_left = np.array(circle_left)
    circle_right = np.array(circle_right)
    
    x_1=circle_right[0]
    y_1=circle_right[1]
    
    x_2=circle_left[0]
    y_2=circle_left[1]
    
    #find the point in the middle of the line
    x_m=((x_2-x_1)/2)+x_1
    m=(y_2-y_1)/(x_2-x_1)   
    y_m=(y_1+m*(x_m-x_1))
    
    x_m=int(round(x_m,0))
    y_m=int(round(y_m,0))
    angle=np.arctan(m)+np.pi/2
    
    
    x_p1=int(round(x_m+0.5*h*np.cos(angle)))
    y_p1=int(round(y_m+0.5*h*np.sin(angle)))
    
    x_p2=int(round(x_m-0.5*h*np.cos(angle)))
    y_p2=int(round(y_m-0.5*h*np.sin(angle)))     
    
    
    points=[(x_1,y_1),(x_2,y_2),(x_m,y_m),(x_p1,y_p1),(x_m,y_m),(x_p2, y_p2)]
    
    return points

def rotate_axis(points,rot_angle,displacement):
    
    x=points[:,0]
    y=points[:,1]
    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                      [-np.sin(rot_angle), np.cos(rot_angle)]])
    rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
                      [np.sin(rot_angle), np.cos(rot_angle)]])
 
    rot_x,rot_y=rot_matrix.dot([x-displacement[0],y-displacement[1]])
    
    spline = UnivariateSpline(rot_x,rot_y, s=1)
    
    new_rot_x = 0
    new_rot_y = spline(new_rot_x)
    
    new_x,new_y=rot_matrix_inv.dot([new_rot_x,new_rot_y])
    new_x=new_x+displacement[0]
    new_y=new_y+displacement[1]
    
    new_point=np.array([new_x,new_y])
    
    return new_point

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def mag(x, y):
    """This function is to find the magnitude of a vector"""
    mag = np.sqrt(x**2 + y**2)
    return mag

def find_angle(Ax, Ay, Bx, By, Cx, Cy):
    """This function is used to find the angle ABC given the point A, B, and C (in Degrees)"""
    vect_Ax = Ax - Bx
    vect_Ay = Ay - By
    vect_Cx = Cx - Bx
    vect_Cy = Cy - By
    mag_AB = mag(vect_Ax, vect_Ay)
    mag_CB = mag(vect_Cx, vect_Cy)
    dot = (vect_Ax * vect_Cx) + (vect_Ay * vect_Cy)
    cos = dot/(mag_AB * mag_CB)
    angle = np.arccos(cos)
    angle = np.rad2deg(angle)
    angle = round(angle, 2)
    
    return angle
   
def find_NLF(shape, points):
    right_NLF = shape[68:72]
    left_NLF = shape[72:76]
    # print(right_NLF)
    # print(left_NLF)
    right_NLF_x = None
    right_NLF_y = None
    left_NLF_x = None
    left_NLF_y = None
    for point in right_NLF:
        (x,y,ID) = point
        if ID == 69:
            right_NLF_x = np.array(float(x))
            right_NLF_y = np.array(float(y))
        else:
            right_NLF_x = np.append(right_NLF_x, float(x))
            right_NLF_y = np.append(right_NLF_y, float(y))
    for point in left_NLF:
        (x,y,ID) = point
        if ID == 73:
            left_NLF_x = np.array(float(x))
            left_NLF_y = np.array(float(y))
        else:
            left_NLF_x = np.append(left_NLF_x, float(x))
            left_NLF_y = np.append(left_NLF_y, float(y))        
        
    # print('right_NLF_x = ', right_NLF_x)
    # print('right_NLF_y = ', right_NLF_y)
    # print('left_NLF_x = ', right_NLF_x)
    # print('left_NLF_y = ', right_NLF_y)
    """Find Line of Best Fit"""
    m_right, b_right = np.polyfit(right_NLF_x, right_NLF_y, 1)
    m_left, b_left = np.polyfit(left_NLF_x, left_NLF_y, 1)
    
    """Finding 2 point to draw"""
    #Right
    x1_right = right_NLF_x[0]
    y1_right = m_right*x1_right + b_right
    x2_right = right_NLF_x[-1]
    y2_right = m_right*x2_right + b_right
    #Left
    x1_left = left_NLF_x[0]
    y1_left = m_left*x1_left + b_left
    x2_left = left_NLF_x[-1]
    y2_left = m_left*x2_left + b_left
    
    #Finding Midline
    (mid1_x, mid1_y) = points[3]
    (mid2_x, mid2_y) = points[5]
    
    L_mid = line([mid1_x, mid1_y], [mid2_x, mid2_y])

    #Find Intersection point
    L_right = line([x1_right, y1_right], [x2_right, y2_right])
    L_left = line([x1_left, y1_left], [x2_left, y2_left])
    
    try:
        (x_R_right, y_R_right) = intersection(L_right, L_mid)
        angle_right = find_angle(x1_right, y1_right, x_R_right, y_R_right, mid1_x, mid1_y)
    except:
        (x_R_right, y_R_right) = (0,0)
        angle_right = 0
        
    try:
        (x_R_left, y_R_left) = intersection(L_left, L_mid)
        angle_left = find_angle(x1_left, y1_left, x_R_left, y_R_left, mid1_x, mid1_y)
    except:
        (x_R_left, y_R_left) = (0,0)
        angle_left = 0
    
    if angle_right >= 80:
        (x_R_right, y_R_right) = (0,0)
        angle_right = 0
        
    if angle_left >= 80:
        (x_R_left, y_R_left) = (0,0)
        angle_left = 0   
    
    points = [(x1_right, y1_right), (x_R_right, y_R_right), (x1_left, y1_left), (x_R_left, y_R_left)]
    angles = [angle_right, angle_left]
    
    return points, angles


def find_point_in_lips(points_upper, points_lower, points_upper_inside, 
                points_lower_inside, rot_angle, displacement, radius):
    
    #find where a circle with radius (radius) and center in the corner of the
    #lip enconters the spline represinting the upper lip
    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                      [-np.sin(rot_angle), np.cos(rot_angle)]])
    rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
                      [np.sin(rot_angle), np.cos(rot_angle)]])
    
    x=points_upper[:,0]
    y=points_upper[:,1]
  
    rot_x,rot_y=rot_matrix.dot([x-displacement[0],y-displacement[1]])
    
    spline = UnivariateSpline(rot_x,rot_y, s=1)
    new_rot_x=np.arange(int(round(min(rot_x),0)),int(round(max(rot_x),0))+1)  
    new_rot_y = spline(new_rot_x)

    euclid_distance=np.sqrt(new_rot_x*new_rot_x + new_rot_y*new_rot_y)
    temp=abs(euclid_distance-radius)
    idx_min=np.argmin(temp)   #this one takes 0.000997781753540039s
    #idx_min = int(np.where(temp==temp.min())[0])  #this one takes 0.0009992122650146484s
    cross_lip_rot_x_upper=new_rot_x[idx_min]
    cross_lip_rot_y_upper=new_rot_y[idx_min]
    
    new_x_upper,new_y_upper=rot_matrix_inv.dot([cross_lip_rot_x_upper,cross_lip_rot_y_upper])
    new_x_upper=new_x_upper+displacement[0]
    new_y_upper=new_y_upper+displacement[1]
        
    new_point_upper=np.array([new_x_upper,new_y_upper])
    
    #find the mouth openness
    x=points_lower[:,0]
    y=points_lower[:,1]
   
    rot_x,rot_y=rot_matrix.dot([x-new_x_upper,y-new_y_upper])
    
    spline = UnivariateSpline(rot_x,rot_y, s=1)
    new_rot_x=0#np.arange(int(round(min(rot_x),0)),int(round(max(rot_x),0))+1)  
    new_rot_y = spline(new_rot_x)

    cross_lip_rot_x_lower=new_rot_x
    cross_lip_rot_y_lower=new_rot_y
    
    new_x_lower,new_y_lower=rot_matrix_inv.dot([cross_lip_rot_x_lower,cross_lip_rot_y_lower])
    new_x_lower=new_x_lower+new_x_upper
    new_y_lower=new_y_lower+new_y_upper
        
    new_point_lower=np.array([new_x_lower,new_y_lower])
    
    
    
    #find the teeth show 
    x=points_upper_inside[:,0]
    y=points_upper_inside[:,1]
    rot_x,rot_y=rot_matrix.dot([x-new_x_upper,y-new_y_upper])
    
    spline = UnivariateSpline(rot_x,rot_y, s=1)
    new_rot_x=0#np.arange(int(round(min(rot_x),0)),int(round(max(rot_x),0))+1)  
    new_rot_y = spline(new_rot_x)

    cross_lip_rot_x_upper_inside=new_rot_x
    cross_lip_rot_y_upper_inside=new_rot_y
    
    new_x_upper_inside,new_y_upper_inside=rot_matrix_inv.dot([cross_lip_rot_x_upper_inside,cross_lip_rot_y_upper_inside])
    new_x_upper_inside=new_x_upper_inside+new_x_upper
    new_y_upper_inside=new_y_upper_inside+new_y_upper
        
    new_point_upper_inside=np.array([new_x_upper_inside,new_y_upper_inside])
    
    
    x=points_lower_inside[:,0]
    y=points_lower_inside[:,1]
    rot_x,rot_y=rot_matrix.dot([x-new_x_upper,y-new_y_upper])
    
    spline = UnivariateSpline(rot_x,rot_y, s=1)
    new_rot_x=0#np.arange(int(round(min(rot_x),0)),int(round(max(rot_x),0))+1)  
    new_rot_y = spline(new_rot_x)

    cross_lip_rot_x_lower_inside=new_rot_x
    cross_lip_rot_y_lower_inside=new_rot_y
    
    new_x_lower_inside,new_y_lower_inside=rot_matrix_inv.dot([cross_lip_rot_x_lower_inside,cross_lip_rot_y_lower_inside])
    new_x_lower_inside=new_x_lower_inside+new_x_upper
    new_y_lower_inside=new_y_lower_inside+new_y_upper
        
    new_point_lower_inside=np.array([new_x_lower_inside,new_y_lower_inside])
    
    
    
    #compute mouth openness and teeth show
    openness = new_rot_y
    theet_show = cross_lip_rot_y_lower_inside-cross_lip_rot_y_upper_inside
    if theet_show < 0:
        theet_show = 0

    
    return new_point_upper, new_point_lower, new_point_upper_inside, new_point_lower_inside, openness, theet_show

def rotate_xy(x, y, rot_angle):
    """This function finds the new x and y arrays if the x and y axis are rotated.
       Additional Note: This function assumes that the first point is (0,0)"""
    
    """First convert points to magnitudes and angles"""
    mags = mag(x, y)
    theta = np.arctan(y/x)
    new_theta = theta + rot_angle
    new_x = mags*np.cos(new_theta)
    new_y = mags*np.sin(new_theta)
    
    new_x[0] = 0
    new_y[0] = 0
    
    #Test Line:
    # print('mags =', mags, '\n',
        # 'theta =', theta, '\n',
        # 'new_theta = ', new_theta, '\n')
        
    return new_x, new_y



    
def mouth_measures(center, commissure, rot_angle):
    x=commissure[0]
    y=commissure[1]

    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                      [-np.sin(rot_angle), np.cos(rot_angle)]])
    #rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
    #                  [np.sin(rot_angle), np.cos(rot_angle)]])
 
    rot_x,rot_y=rot_matrix.dot([x-center[0],y-center[1]])
    distance= np.sqrt(rot_x**2 + rot_y**2)

    angle = np.arcsin((-rot_y)/distance)*(180/np.pi)
    
    return distance, angle, abs(rot_y) 


def deviation(pt1, pt2, center, rot_angle):
    x1=pt1[0]
    y1=pt1[1]
    
    x2=pt2[0]
    y2=pt2[1]
    
    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                      [-np.sin(rot_angle), np.cos(rot_angle)]])
    
    
    x1_rot, y1_rot = rot_matrix.dot([x1-center[0], y1-center[1]])
    x2_rot, y2_rot = rot_matrix.dot([x2-center[0], y2-center[1]])
    distance = abs(y1_rot-y2_rot)

    return distance 

def find_mid_point_lips(corner_left, corner_right, center, rot_angle):
    x1=corner_left[0]
    y1=corner_left[1]
    
    x2=corner_right[0]
    y2=corner_right[1]
    
    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                      [-np.sin(rot_angle), np.cos(rot_angle)]])
    
    x1_rot, y1_rot = rot_matrix.dot([x1-center[0], y1-center[1]])
    x2_rot, y2_rot = rot_matrix.dot([x2-center[0], y2-center[0]])   
    
    
    distance_left = abs(x1_rot/2)
    distance_right = abs(x2_rot/2)
    
    return distance_left, distance_right


def palpebral_fissure_height(eye, rot_angle, center):
    
    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                  [-np.sin(rot_angle), np.cos(rot_angle)]])
    rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
                  [np.sin(rot_angle), np.cos(rot_angle)]])
    
    
    #upper lid
    x=eye[0:4,0]
    y=eye[0:4,1]
    rot_x,rot_y=rot_matrix.dot([x-center[0],y-center[1]])
    
    spline_upper= UnivariateSpline(rot_x,rot_y)
    mid_upper = (rot_x[1]+rot_x[2])/2
    
    #lower lid
    x=eye[[0,5,4,3],0]
    y=eye[[0,5,4,3],1]
    rot_x,rot_y=rot_matrix.dot([x-center[0],y-center[1]])
    
    spline_lower = UnivariateSpline(rot_x,rot_y, s=1)
    mid_lower = (rot_x[1]+rot_x[2])/2
    
    
    mid_mid = (mid_upper+mid_lower)/2
    new_up = spline_upper(mid_mid)
    new_down = spline_lower(mid_mid)
    
    
    uper_lid_x,uper_lid_y = rot_matrix_inv.dot([mid_mid,new_up])
    uper_lid_x=uper_lid_x+center[0]
    uper_lid_y=uper_lid_y+center[1]
    
    lower_lid_x,lower_lid_y = rot_matrix_inv.dot([mid_mid,new_down])
    lower_lid_x=lower_lid_x+center[0]
    lower_lid_y=lower_lid_y+center[1]
    
    
    return np.sqrt((uper_lid_x-lower_lid_x)**2 + (uper_lid_y-lower_lid_y)**2)


def area_inside_mouth(points_upper, points_lower, rot_angle, center):

    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                    [-np.sin(rot_angle), np.cos(rot_angle)]])
    # rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
    #                     [np.sin(rot_angle), np.cos(rot_angle)]])

    x_lower=points_lower[:,0]
    y_lower=points_lower[:,1]

    rot_x_lower,rot_y_lower=rot_matrix.dot([x_lower-center[0],y_lower-center[1]])

    spline = UnivariateSpline(rot_x_lower,rot_y_lower, s=1)
    vals_x_lower = np.linspace(rot_x_lower.min(), rot_x_lower.max(), 100, endpoint=True)
    vals_y_lower = spline(vals_x_lower)

    x_upper=points_upper[:,0]
    y_upper=points_upper[:,1]

    rot_x_upper,rot_y_upper=rot_matrix.dot([x_upper-center[0],y_upper-center[1]])

    spline = UnivariateSpline(rot_x_upper,rot_y_upper, s=1)
    vals_x_upper = np.linspace(rot_x_upper.min(), rot_x_upper.max(), 100, endpoint=True)
    vals_y_upper = spline(vals_x_upper)

    #to find the right vs. right we need to find the point where x is 0 (or closest to 0)
    idx_zero = np.argmin(np.abs(vals_x_lower)) 

    #handle extreme cases  using conditions-> 
    if idx_zero == 0: #no lips to the right
        difference = vals_y_lower-vals_y_upper
        area_right = 0
        area_left = np.abs(np.trapz(difference, vals_x_lower))
    elif idx_zero >= len(vals_x_lower): #no lips to the left
        difference = vals_y_lower-vals_y_upper
        area_left = 0 
        area_right = np.abs(np.trapz(difference, vals_x_lower))
    else: #mouth divided in two
        difference = vals_y_lower-vals_y_upper
        area_left = np.abs(np.trapz(difference[idx_zero:], vals_x_lower[idx_zero:],))
        area_right = np.abs(np.trapz(difference[:idx_zero], vals_x_lower[:idx_zero],))

    return area_right, area_left


def area_inside_eye(points_upper, points_lower, rot_angle, center):

    rot_matrix=np.array([[np.cos(rot_angle), np.sin(rot_angle)],
                    [-np.sin(rot_angle), np.cos(rot_angle)]])
    # rot_matrix_inv=np.array([[np.cos(rot_angle), -np.sin(rot_angle)],
    #                     [np.sin(rot_angle), np.cos(rot_angle)]])

    x_lower=points_lower[:,0]
    y_lower=points_lower[:,1]

    rot_x_lower,rot_y_lower=rot_matrix.dot([x_lower-center[0],y_lower-center[1]])

    spline = UnivariateSpline(rot_x_lower,rot_y_lower, s=1)
    vals_x_lower = np.linspace(rot_x_lower.min(), rot_x_lower.max(), 100, endpoint=True)
    vals_y_lower = spline(vals_x_lower)

    x_upper=points_upper[:,0]
    y_upper=points_upper[:,1]

    rot_x_upper,rot_y_upper=rot_matrix.dot([x_upper-center[0],y_upper-center[1]])

    spline = UnivariateSpline(rot_x_upper,rot_y_upper, s=1)
    vals_x_upper = np.linspace(rot_x_upper.min(), rot_x_upper.max(), 100, endpoint=True)
    vals_y_upper = spline(vals_x_upper)

    area = np.trapz(vals_y_lower-vals_y_upper, vals_x_upper)

    return area
        
    
class FaceMeasurementsSide(object):
    
    def __init__(self):        
        self.CommissureExcursion = 0 
        self.SmileAngle = 0
        self.MarginalReflexDistance1 = 0
        self.MarginalReflexDistance2 = 0 
        self.BrowHeight = 0 
        self.DentalShow = 0 
        self.PalpebralFissureHeight = 0
        self.NLF_angle = 0
        self.DentalShowArea = 0
        self.EyeArea = 0
        
class FaceMeasurementsDeviation(object):
    
    def __init__(self):
        self.CommisureHeightDeviation = 0
        self.UpperLipHeightDeviation = 0
        self.LowerLipHeightDeviation = 0
        
        self.CommissureExcursion = 0 
        self.SmileAngle = 0
        self.MarginalReflexDistance1 = 0
        self.MarginalReflexDistance2 = 0 
        self.BrowHeight = 0 
        self.DentalShow = 0
        self.PalpebralFissureHeight = 0
        self.NLF_angle = 0
        self.DentalShowArea = 0
        self.EyeArea = 0

def get_measurements_from_data(shape, left_pupil, right_pupil, points, CalibrationType, CalibrationValue):
    
    shape = np.array(shape)
    
    ResultsLeft = FaceMeasurementsSide()
    ResultsRight = FaceMeasurementsSide()
    ResultsDeviation = FaceMeasurementsDeviation()
    ResultsPercentile = FaceMeasurementsDeviation()
    
    #NLF Angle
    _, NLF_angles = find_NLF(shape, points)
    
    ResultsRight.NLF_angle = NLF_angles[0]
    ResultsLeft.NLF_angle = NLF_angles[1]
    ResultsDeviation.NLF_angle = abs(NLF_angles[1] - NLF_angles[0])
    
    if ResultsDeviation.NLF_angle == 0:
        ResultsPercentile.NLF_angle = 0
    else:
        #Makes sure to not divide by 0
        try:
            ResultsPercentile.NLF_angle = abs(NLF_angles[1] - NLF_angles[0])*100/(max(NLF_angles[0], NLF_angles[1]))
        except:
            ResultsPercentile.NLF_angle = 0
    
    slope, center = estimate_line(left_pupil, right_pupil)
    
    rot_angle=np.arctan(slope)
    #Areas
    slope, center = estimate_line(left_pupil, right_pupil)
    rot_angle=np.arctan(slope)
    
    
    points_lower_innerlip = shape[[60,67,66,65,64],:]
    points_upper_innerlip = shape[60:65,:]
    area_right, area_left = area_inside_mouth(points_upper_innerlip, points_lower_innerlip, rot_angle, center)
    
    
    points_lower_leftlid = shape[[42,47,46,45],:]
    points_upper_leftlid = shape[42:46,:]
    area_left_eye= area_inside_eye(points_upper_leftlid, points_lower_leftlid, rot_angle, center)
    
    points_lower_rightlid = shape[[36,41,40,39],:]
    points_upper_rightlid = shape[36:40,:]
    area_right_eye= area_inside_eye(points_upper_rightlid, points_lower_rightlid, rot_angle, center)
    
    radius=(left_pupil[2]+right_pupil[2])/2
    Calibration = 11.77/(2*radius)

    #Dental Show Area 
    ResultsRight.DentalShowArea = area_right*(Calibration**2)
    ResultsLeft.DentalShowArea = area_left*(Calibration**2)
    #Eye Area
    ResultsRight.EyeArea = area_right_eye*(Calibration**2)
    ResultsLeft.EyeArea = area_left_eye*(Calibration**2)
    #Dental Show Area Difference
    ResultsDeviation.DentalShowArea = abs(ResultsRight.DentalShowArea - ResultsLeft.DentalShowArea) 
    ResultsPercentile.DentalShowArea = (ResultsDeviation.DentalShowArea*100)/max(ResultsRight.DentalShowArea,ResultsLeft.DentalShowArea)
    #Eye Area Difference
    ResultsDeviation.EyeArea = abs(ResultsRight.EyeArea - ResultsLeft.EyeArea)   
    ResultsPercentile.EyeArea = (ResultsDeviation.EyeArea*100)/max(ResultsRight.EyeArea,ResultsLeft.EyeArea)
    
    #lower lip 
    x1_lowerlip=shape[48,0]
    temp=shape[54:60,0]

    x1_lowerlip=np.append(x1_lowerlip,temp[::-1])
    y1_lowerlip=shape[48,1]
    temp=shape[54:60,1]
    y1_lowerlip=np.append(y1_lowerlip,temp[::-1])
    #find where the lip curve crosses with the rotated 'x' axis, this provides the 
    #point where the lips cross with the middle of the face 
    # print(rot_angle, center)
    # print(x1_lowerlip)
    cross_lowerlip=rotate_axis(np.column_stack((x1_lowerlip,y1_lowerlip)),rot_angle,center)
    
    comm_exc_left, smile_angle_left, _ = mouth_measures(cross_lowerlip, shape[54], rot_angle)
    
    ResultsLeft.CommissureExcursion = comm_exc_left
    if cross_lowerlip[1] >= shape[54,1]:
        ResultsLeft.SmileAngle = 90 + smile_angle_left
    else:
        ResultsLeft.SmileAngle = 90 + smile_angle_left    
    #ResultsLeft.CommissureHeight = comm_height_left
    
    comm_exc_right, smile_angle_right, _ = mouth_measures(cross_lowerlip, shape[48], rot_angle)
    
    ResultsRight.CommissureExcursion = comm_exc_right
    
    if cross_lowerlip[1] >= shape[48,1]:
        ResultsRight.SmileAngle = 90 + smile_angle_right
    else:
        ResultsRight.SmileAngle = 90 + smile_angle_right
    #ResultsRight.CommissureHeight = comm_height_right
    
    ResultsDeviation.CommisureHeightDeviation = deviation(shape[48],shape[54],center,rot_angle)
    
    
    #lower lip - inside
    x1_lowerlip_inside=shape[60,0]
    temp=shape[64:68,0]
    x1_lowerlip_inside=np.append(x1_lowerlip_inside,temp[::-1])
    y1_lowerlip_inside=shape[60,1]
    temp=shape[64:68,1]
    y1_lowerlip_inside=np.append(y1_lowerlip_inside,temp[::-1])
    
    #upper lip
    x1_upperlip=shape[48:55,0]
    y1_upperlip=shape[48:55,1]
    
    
    #upper lip - inside
    x1_upperlip_inside=shape[60:65,0]
    y1_upperlip_inside=shape[60:65,1]
    
    
    #find mid distance from corner of mouth the line in the middle of face in 
    #both sides
    distance_left, distance_right = find_mid_point_lips(shape[54], shape[48], center, rot_angle)

    
    #point of contact with mouth and teeth show - left 
    
    (new_point_upper_left, new_point_lower_left, new_point_upper_inside_left, 
     new_point_lower_inside_left, openness_left, 
     theet_show_left) = find_point_in_lips(
            np.column_stack((x1_upperlip,y1_upperlip)), 
            np.column_stack((x1_lowerlip,y1_lowerlip)), 
            np.column_stack((x1_upperlip_inside,y1_upperlip_inside)),
            np.column_stack((x1_lowerlip_inside,y1_lowerlip_inside)), 
            rot_angle, 
            shape[54], 
            distance_left)
    
    ResultsLeft.DentalShow = theet_show_left   
    #_ , _ , ResultsLeft.UpperVermillionHeight = mouth_measures(cross_lowerlip, new_point_upper_left, rot_angle)
    #_ , _ , ResultsLeft.LowerVermillionHeight = mouth_measures(cross_lowerlip, new_point_lower_left, rot_angle)
    
    #point of contact with mouth and teeth show - right
    (new_point_upper_right, new_point_lower_right, new_point_upper_inside_right, 
     new_point_lower_inside_right, openness_right, 
     theet_show_right) = find_point_in_lips(
            np.column_stack((x1_upperlip,y1_upperlip)), 
            np.column_stack((x1_lowerlip,y1_lowerlip)), 
            np.column_stack((x1_upperlip_inside,y1_upperlip_inside)),
            np.column_stack((x1_lowerlip_inside,y1_lowerlip_inside)), 
            rot_angle, 
            shape[48], 
            distance_right)
    
    ResultsRight.DentalShow = theet_show_right
    #_ , _ , ResultsRight.UpperVermillionHeight = mouth_measures(cross_lowerlip, new_point_upper_right, rot_angle)
    #_ , _ , ResultsRight.LowerVermillionHeight = mouth_measures(cross_lowerlip, new_point_lower_right, rot_angle)
    
    ResultsDeviation.UpperLipHeightDeviation= deviation(new_point_upper_left,new_point_upper_right,center,rot_angle)
    ResultsDeviation.LowerLipHeightDeviation= deviation(new_point_lower_left,new_point_lower_right,center,rot_angle)

    
    #upper lid - left
    x1_upperlid_left=shape[42:46,0]
    y1_upperlid_left=shape[42:46,1]
    cross_upperlid_left=rotate_axis(np.column_stack((x1_upperlid_left,y1_upperlid_left)),rot_angle,np.array([left_pupil[0],left_pupil[1]]))
    _ , _ , ResultsLeft.MarginalReflexDistance1 = mouth_measures(left_pupil[0:2], cross_upperlid_left, rot_angle)
    
    #lower lid - left
    x1_lowerlid_left=shape[42,0]
    temp=shape[45:48,0]
    x1_lowerlid_left=np.append(x1_lowerlid_left,temp[::-1])
    y1_lowerlid_left=shape[42,1]
    temp=shape[45:48,1]
    y1_lowerlid_left=np.append(y1_lowerlid_left,temp[::-1])
    cross_lowerlid_left=rotate_axis(np.column_stack((x1_lowerlid_left,y1_lowerlid_left)),rot_angle,np.array([left_pupil[0],left_pupil[1]]))
    _ , _ , ResultsLeft.MarginalReflexDistance2 = mouth_measures(left_pupil[0:2], cross_lowerlid_left, rot_angle)
    
    
    #brown- left
    x1_brown_left=shape[22:27,0]
    y1_brown_left=shape[22:27,1]
    cross_brown_left=rotate_axis(np.column_stack((x1_brown_left,y1_brown_left)),rot_angle,np.array([left_pupil[0],left_pupil[1]]))
    _ , _ , ResultsLeft.BrowHeight = mouth_measures(left_pupil[0:2], cross_brown_left, rot_angle)
    
    
    #upper lid - right
    x1_upperlid_right=shape[36:40,0]
    y1_upperlid_right=shape[36:40,1]
    cross_upperlid_right=rotate_axis(np.column_stack((x1_upperlid_right,y1_upperlid_right)),rot_angle,np.array([right_pupil[0],right_pupil[1]]))
    _ , _ , ResultsRight.MarginalReflexDistance1 = mouth_measures(right_pupil[0:2], cross_upperlid_right, rot_angle)

    
    
    #lower lid - right
    x1_lowerlid_right=shape[36,0]
    temp=shape[39:42,0]
    x1_lowerlid_right=np.append(x1_lowerlid_right,temp[::-1])
    y1_lowerlid_right=shape[36,1]
    temp=shape[39:42,1]
    y1_lowerlid_right=np.append(y1_lowerlid_right,temp[::-1])
    cross_lowerlid_right=rotate_axis(np.column_stack((x1_lowerlid_right,y1_lowerlid_right)),rot_angle,np.array([right_pupil[0],right_pupil[1]]))
    _ , _ , ResultsRight.MarginalReflexDistance2 = mouth_measures(right_pupil[0:2], cross_lowerlid_right, rot_angle)
    
    
    #brown- right
    x1_brow_right=shape[17:22,0]
    y1_brow_right=shape[17:22,1]
    cross_brow_right=rotate_axis(np.column_stack((x1_brow_right,y1_brow_right)),rot_angle,np.array([right_pupil[0],right_pupil[1]]))
    _ , _ , ResultsRight.BrowHeight = mouth_measures(right_pupil[0:2], cross_brow_right, rot_angle)
    
    

    #Palpebral Fissure Height 
    PalpebralFissureHeight_Right = palpebral_fissure_height(shape[36:42,:], rot_angle, center)
    PalpebralFissureHeight_Left = palpebral_fissure_height(shape[42:48,:], rot_angle, center)

    
    radius=(left_pupil[2]+right_pupil[2])/2
    if CalibrationType == 'Iris': #Iris radius will be used as calibration
        Calibration = CalibrationValue/(2*radius)
    else:  #user provided calibration radius 
        Calibration = CalibrationValue
    
    
    
    ResultsLeft.CommissureExcursion = ResultsLeft.CommissureExcursion*Calibration
    ResultsLeft.DentalShow = ResultsLeft.DentalShow*Calibration
    ResultsLeft.MarginalReflexDistance1 = ResultsLeft.MarginalReflexDistance1*Calibration
    ResultsLeft.MarginalReflexDistance2 = ResultsLeft.MarginalReflexDistance2*Calibration
    ResultsLeft.BrowHeight = ResultsLeft.BrowHeight*Calibration
    ResultsLeft.PalpebralFissureHeight = PalpebralFissureHeight_Left*Calibration
    
    
    ResultsRight.CommissureExcursion = ResultsRight.CommissureExcursion*Calibration
    ResultsRight.DentalShow = ResultsRight.DentalShow*Calibration
    ResultsRight.MarginalReflexDistance1 = ResultsRight.MarginalReflexDistance1*Calibration
    ResultsRight.MarginalReflexDistance2 = ResultsRight.MarginalReflexDistance2*Calibration
    ResultsRight.BrowHeight = ResultsRight.BrowHeight*Calibration
    ResultsRight.PalpebralFissureHeight = PalpebralFissureHeight_Right*Calibration
    
    ResultsDeviation.CommisureHeightDeviation = ResultsDeviation.CommisureHeightDeviation*Calibration
    ResultsDeviation.UpperLipHeightDeviation = ResultsDeviation.UpperLipHeightDeviation*Calibration
    ResultsDeviation.LowerLipHeightDeviation = ResultsDeviation.LowerLipHeightDeviation*Calibration
    
    
    ResultsDeviation.CommissureExcursion = abs(ResultsLeft.CommissureExcursion-ResultsRight.CommissureExcursion)
    ResultsDeviation.SmileAngle = abs(ResultsLeft.SmileAngle-ResultsRight.SmileAngle)
    ResultsDeviation.DentalShow = abs(ResultsLeft.DentalShow-ResultsRight.DentalShow)
    ResultsDeviation.MarginalReflexDistance1 = abs(ResultsLeft.MarginalReflexDistance1-ResultsRight.MarginalReflexDistance1)
    ResultsDeviation.MarginalReflexDistance2 = abs(ResultsLeft.MarginalReflexDistance2-ResultsRight.MarginalReflexDistance2)
    ResultsDeviation.BrowHeight = abs(ResultsLeft.BrowHeight-ResultsRight.BrowHeight)
    ResultsDeviation.PalpebralFissureHeight = abs(ResultsLeft.PalpebralFissureHeight - ResultsRight.PalpebralFissureHeight)


    if shape[57,0] >= cross_lowerlip[0] : #left is the good side (probably)
        ResultsPercentile.BrowHeight = abs(ResultsLeft.BrowHeight - ResultsRight.BrowHeight)*100/ResultsLeft.BrowHeight
        ResultsPercentile.MarginalReflexDistance1 = abs(ResultsLeft.MarginalReflexDistance1 - ResultsRight.MarginalReflexDistance1)*100/ResultsLeft.MarginalReflexDistance1
        ResultsPercentile.MarginalReflexDistance2 = abs(ResultsLeft.MarginalReflexDistance2 - ResultsRight.MarginalReflexDistance2)*100/ResultsLeft.MarginalReflexDistance2
        ResultsPercentile.CommissureExcursion = abs(ResultsLeft.CommissureExcursion - ResultsRight.CommissureExcursion)*100/ResultsLeft.CommissureExcursion
        ResultsPercentile.SmileAngle = abs(ResultsLeft.SmileAngle - ResultsRight.SmileAngle)*100/ResultsLeft.SmileAngle
        if ResultsLeft.DentalShow >0:
            ResultsPercentile.DentalShow = abs(ResultsLeft.DentalShow - ResultsRight.DentalShow)*100/ResultsLeft.DentalShow   
        else:
            ResultsPercentile.DentalShow = 0
        
        if ResultsLeft.PalpebralFissureHeight > 0:
            ResultsPercentile.PalpebralFissureHeight = abs(ResultsLeft.PalpebralFissureHeight - ResultsRight.PalpebralFissureHeight)*100/ResultsLeft.PalpebralFissureHeight
        else:
            ResultsPercentile.PalpebralFissureHeight = 0
    else:  #right is the good side 
        ResultsPercentile.BrowHeight = abs(ResultsLeft.BrowHeight - ResultsRight.BrowHeight)*100/ResultsRight.BrowHeight
        ResultsPercentile.MarginalReflexDistance1 = abs(ResultsLeft.MarginalReflexDistance1 - ResultsRight.MarginalReflexDistance1)*100/ResultsRight.MarginalReflexDistance1
        ResultsPercentile.MarginalReflexDistance2 = abs(ResultsLeft.MarginalReflexDistance2 - ResultsRight.MarginalReflexDistance2)*100/ResultsRight.MarginalReflexDistance2
        ResultsPercentile.CommissureExcursion = abs(ResultsLeft.CommissureExcursion - ResultsRight.CommissureExcursion)*100/ResultsRight.CommissureExcursion
        ResultsPercentile.SmileAngle = abs(ResultsLeft.SmileAngle - ResultsRight.SmileAngle)*100/ResultsRight.SmileAngle        
        if ResultsRight.DentalShow > 0:
            ResultsPercentile.DentalShow = abs(ResultsLeft.DentalShow - ResultsRight.DentalShow)*100/ResultsRight.DentalShow
        else:
            ResultsPercentile.DentalShow =0     
        
        if ResultsRight.PalpebralFissureHeight > 0:
            ResultsPercentile.PalpebralFissureHeight = abs(ResultsLeft.PalpebralFissureHeight - ResultsRight.PalpebralFissureHeight)*100/ResultsRight.PalpebralFissureHeight
        else:
            ResultsPercentile.PalpebralFissureHeight = 0
    



    
    return ResultsLeft, ResultsRight, ResultsDeviation, ResultsPercentile
    

    
    
    