import numpy as np


def Compute_Resting_eFace(LeftRest, RightRest, reference_side):
    """This function computes the static eFace values using the resting 
    expression results"""

    # 1) EyeBrow Elevation at rest
    a_left, a_right = LeftRest.BrowHeight, RightRest.BrowHeight
    if reference_side == 'Right':
        Brow_at_rest = a_left/a_right
    else:
        Brow_at_rest = a_right/a_left
    
    Brow_at_rest = np.round(Brow_at_rest*100,1)
    
    
    # 2) Palpebral Fissure width at rest
    c_left, c_right = LeftRest.PalpebralFissureHeight, RightRest.PalpebralFissureHeight

    if reference_side == 'Right':
        PalpebralFissure_at_rest = c_right/c_left
    else:
        PalpebralFissure_at_rest = c_left/c_right
    
    PalpebralFissure_at_rest = np.round(PalpebralFissure_at_rest*100,1)
    
    # 3) Oral commissure at rest 
    e_right, d_right = np.sin((RightRest.SmileAngle-90)*np.pi/180)*RightRest.CommissurePosition, np.cos((RightRest.SmileAngle-90)*np.pi/180)*RightRest.CommissurePosition
    e_left, d_left = np.sin((LeftRest.SmileAngle-90)*np.pi/180)*LeftRest.CommissurePosition, np.cos((LeftRest.SmileAngle-90)*np.pi/180)*LeftRest.CommissurePosition
    if reference_side == 'Left':
        #e_left is the disease side
        if e_left < e_right and e_left > 0:
            OralCommissure_at_rest = 1-((e_right - e_left)/e_right)
        else:
            OralCommissure_at_rest = d_left/d_right
    else:
        #e_right is the disease side
        if e_right < e_left and e_right > 0:
            OralCommissure_at_rest = 1-((e_left - e_right)/e_left)
        else:
            OralCommissure_at_rest = d_right/d_left
    
    OralCommissure_at_rest = np.round(OralCommissure_at_rest*100,1)

    # 4) NLF Angle
    if RightRest.NLF_angle == 0 or LeftRest.NLF_angle == 0:
        if RightRest.NLF_angle == 0 and LeftRest.NLF_angle == 0:
            #if both sides are 0 the score is 100
            NLF_at_rest = 100
        else:
            #if only 1 side is 0 then the score is zero
            NLF_at_rest = 0
    else:
        if reference_side == 'Right':
            NLF_at_rest = LeftRest.NLF_angle/RightRest.NLF_angle
        else:
            NLF_at_rest = RightRest.NLF_angle/LeftRest.NLF_angle
    NLF_at_rest = np.round(NLF_at_rest*100,1)

    #apply corrections to remove everything less than zero 
    if Brow_at_rest < 0: Brow_at_rest = 0
    if Brow_at_rest > 200: Brow_at_rest = 200
    if PalpebralFissure_at_rest < 0: PalpebralFissure_at_rest = 0
    if PalpebralFissure_at_rest > 200: PalpebralFissure_at_rest = 200
    if OralCommissure_at_rest < 0: OralCommissure_at_rest = 0
    if OralCommissure_at_rest > 200: OralCommissure_at_rest = 200
    if NLF_at_rest < 0: NLF_at_rest = 0
    if NLF_at_rest > 200: NLF_at_rest = 200

    #Computing the score based on Tessa's idea

    score_brow_rest = 100 - abs(100-Brow_at_rest)
    score_PalpebralFissure_rest = 100 - abs(100-PalpebralFissure_at_rest)
    score_OralCommissure_rest = 100 - abs(100-OralCommissure_at_rest)

    score_brow_rest = np.round(score_brow_rest,1)
    score_PalpebralFissure_rest = np.round(score_PalpebralFissure_rest,1)
    score_OralCommissure_rest = np.round(score_OralCommissure_rest,1)
    NLF_at_rest = np.round(NLF_at_rest,1)

    return score_brow_rest, score_PalpebralFissure_rest, score_OralCommissure_rest, NLF_at_rest
    

def Compute_eFace_BH(LeftRest, RightRest, reference_side):
    """This function computes the static eFace value score_brow_rest"""

    # 1) EyeBrow Elevation at rest
    a_left, a_right = LeftRest.BrowHeight, RightRest.BrowHeight
    if reference_side == 'Right':
        Brow_at_rest = a_left/a_right
    else:
        Brow_at_rest = a_right/a_left
    
    Brow_at_rest = np.round(Brow_at_rest*100,1)
    
    #apply corrections to remove everything less than zero 
    if Brow_at_rest < 0: Brow_at_rest = 0
    if Brow_at_rest > 200: Brow_at_rest = 200
    
    #Computing the score based on Tessa's idea
    score_brow_rest = 100 - abs(100-Brow_at_rest)
    score_brow_rest = np.round(score_brow_rest,1)
    
    return score_brow_rest


def Compute_eFace_PF(LeftRest, RightRest, reference_side):
    """This function computes the static eFace value score_PalpebralFissure_rest"""
    
    # 2) Palpebral Fissure width at rest
    c_left, c_right = LeftRest.PalpebralFissureHeight, RightRest.PalpebralFissureHeight

    if reference_side == 'Right':
        PalpebralFissure_at_rest = c_right/c_left
    else:
        PalpebralFissure_at_rest = c_left/c_right
    
    PalpebralFissure_at_rest = np.round(PalpebralFissure_at_rest*100,1)
    
    #apply corrections to remove everything less than zero 
    if PalpebralFissure_at_rest < 0: PalpebralFissure_at_rest = 0
    if PalpebralFissure_at_rest > 200: PalpebralFissure_at_rest = 200

    #Computing the score based on Tessa's idea

    score_PalpebralFissure_rest = 100 - abs(100-PalpebralFissure_at_rest)

    score_PalpebralFissure_rest = np.round(score_PalpebralFissure_rest,1)

    return score_PalpebralFissure_rest
    

def Compute_eFace_OC(LeftRest, RightRest, reference_side):
    """This function computes the static eFace value score_OralCommissure_rest"""
    
    # 3) Oral commissure at rest 
    e_right, d_right = np.sin((RightRest.SmileAngle-90)*np.pi/180)*RightRest.CommissurePosition, np.cos((RightRest.SmileAngle-90)*np.pi/180)*RightRest.CommissurePosition
    e_left, d_left = np.sin((LeftRest.SmileAngle-90)*np.pi/180)*LeftRest.CommissurePosition, np.cos((LeftRest.SmileAngle-90)*np.pi/180)*LeftRest.CommissurePosition
    if reference_side == 'Left':
        #e_left is the disease side
        if e_left < e_right and e_left > 0:
            OralCommissure_at_rest = 1-((e_right - e_left)/e_right)
        else:
            OralCommissure_at_rest = d_left/d_right
    else:
        #e_right is the disease side
        if e_right < e_left and e_right > 0:
            OralCommissure_at_rest = 1-((e_left - e_right)/e_left)
        else:
            OralCommissure_at_rest = d_right/d_left
    
    OralCommissure_at_rest = np.round(OralCommissure_at_rest*100,1)

    
    if OralCommissure_at_rest < 0: OralCommissure_at_rest = 0
    if OralCommissure_at_rest > 200: OralCommissure_at_rest = 200

    #Computing the score based on Tessa's idea
    score_OralCommissure_rest = 100 - abs(100-OralCommissure_at_rest)

    score_OralCommissure_rest = np.round(score_OralCommissure_rest,1)

    return score_OralCommissure_rest


def Compute_eFace_NLF(LeftRest, RightRest, reference_side):
    """This function computes the static eFace value NLF_at_rest"""

    # 4) NLF Angle
    if RightRest.NLF_angle == 0 or LeftRest.NLF_angle == 0:
        if RightRest.NLF_angle == 0 and LeftRest.NLF_angle == 0:
            #if both sides are 0 the score is 100
            NLF_at_rest = 100
        else:
            #if only 1 side is 0 then the score is zero
            NLF_at_rest = 0
    else:
        if reference_side == 'Right':
            NLF_at_rest = LeftRest.NLF_angle/RightRest.NLF_angle
        else:
            NLF_at_rest = RightRest.NLF_angle/LeftRest.NLF_angle
    NLF_at_rest = np.round(NLF_at_rest*100,1)

    #apply corrections to remove everything less than zero 
    if NLF_at_rest < 0: NLF_at_rest = 0
    if NLF_at_rest > 200: NLF_at_rest = 200

    #Computing the score based on Tessa's idea
    NLF_at_rest = np.round(NLF_at_rest,1)

    return NLF_at_rest
    
    