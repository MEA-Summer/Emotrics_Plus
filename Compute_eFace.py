import numpy as np
from Metrics import get_measurements_from_data
from Patient import Patient

def Compute_Resting_eFace(LeftResting, RightResting, reference_side):
    """This function computes the static eFace values using the resting 
    expression results"""

    # 1) BrowRaise Elevation at rest
    a_left, a_right = LeftResting.BrowHeight, RightResting.BrowHeight
    if reference_side == 'Right':
        Brow_at_rest = a_left/a_right
    else:
        Brow_at_rest = a_right/a_left
    
    Brow_at_rest = np.round(Brow_at_rest*100,1)
    
    
    # 2) Palpebral Fissure width at rest
    c_left, c_right = LeftResting.PalpebralFissureHeight, RightResting.PalpebralFissureHeight

    if reference_side == 'Right':
        PalpebralFissure_at_rest = c_right/c_left
    else:
        PalpebralFissure_at_rest = c_left/c_right
    
    PalpebralFissure_at_rest = np.round(PalpebralFissure_at_rest*100,1)
    
    # 3) Oral commissure at rest 
    e_right, d_right = np.sin((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition, np.cos((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition
    e_left, d_left = np.sin((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition, np.cos((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition
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
    if RightResting.NLF_angle == 0 or LeftResting.NLF_angle == 0:
        if RightResting.NLF_angle == 0 and LeftResting.NLF_angle == 0:
            #if both sides are 0 the score is 100
            NLF_at_rest = 100
        else:
            #if only 1 side is 0 then the score is zero
            NLF_at_rest = 0
    else:
        if reference_side == 'Right':
            NLF_at_rest = LeftResting.NLF_angle/RightResting.NLF_angle
        else:
            NLF_at_rest = RightResting.NLF_angle/LeftResting.NLF_angle
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

    return Brow_at_rest, PalpebralFissure_at_rest, OralCommissure_at_rest, NLF_at_rest
    

def Compute_eFace_BH(LeftResting, RightResting, reference_side):
    """This function computes the static eFace value score_brow_rest"""

    # 1) BrowRaise Elevation at rest
    a_left, a_right = LeftResting.BrowHeight, RightResting.BrowHeight
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
    
    return Brow_at_rest


def Compute_eFace_PF(LeftResting, RightResting, reference_side):
    """This function computes the static eFace value score_PalpebralFissure_rest"""
    
    # 2) Palpebral Fissure width at rest
    c_left, c_right = LeftResting.PalpebralFissureHeight, RightResting.PalpebralFissureHeight

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

    return PalpebralFissure_at_rest
    

def Compute_eFace_OC(LeftResting, RightResting, reference_side):
    """This function computes the static eFace value score_OralCommissure_rest"""
    
    # 3) Oral commissure at rest 
    e_right, d_right = np.sin((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition, np.cos((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition
    e_left, d_left = np.sin((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition, np.cos((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition
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

    return OralCommissure_at_rest


def Compute_eFace_NLF(LeftResting, RightResting, reference_side):
    """This function computes the static eFace value NLF_at_rest"""

    # 4) NLF Angle
    if RightResting.NLF_angle == 0 or LeftResting.NLF_angle == 0:
        if RightResting.NLF_angle == 0 and LeftResting.NLF_angle == 0:
            #if both sides are 0 the score is 100
            NLF_at_rest = 100
        else:
            #if only 1 side is 0 then the score is zero
            NLF_at_rest = 0
    else:
        if reference_side == 'Right':
            NLF_at_rest = LeftResting.NLF_angle/RightResting.NLF_angle
        else:
            NLF_at_rest = RightResting.NLF_angle/LeftResting.NLF_angle
    NLF_at_rest = np.round(NLF_at_rest*100,1)

    #apply corrections to remove everything less than zero 
    if NLF_at_rest < 0: NLF_at_rest = 0
    if NLF_at_rest > 200: NLF_at_rest = 200

    #Computing the score based on Tessa's idea
    NLF_at_rest = np.round(NLF_at_rest,1)

    return NLF_at_rest


def Compute_eFace(Patient):

    #compute the different measures from each photo

    LeftResting, RightResting, _ , _  = get_measurements_from_data(Patient._Resting._shape, Patient._Resting._lefteye, Patient._Resting._righteye, Patient._Resting._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    LeftBigSmile, RightBigSmile, _, _ = get_measurements_from_data(Patient._Big_Smile._shape, Patient._Big_Smile._lefteye, Patient._Big_Smile._righteye, Patient._Big_Smile._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    LeftBrowRaise, RightBrowRaise, _, _ = get_measurements_from_data(Patient._Brow_Raise._shape, Patient._Brow_Raise._lefteye, Patient._Brow_Raise._righteye, Patient._Brow_Raise._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    LeftGentleEyeClosure, RightGentleEyeClosure, _, _ = get_measurements_from_data(Patient._Gentle_Eye_Closure._shape, Patient._Gentle_Eye_Closure._lefteye, Patient._Gentle_Eye_Closure._righteye, Patient._Gentle_Eye_Closure._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    LeftTightEyeClosure, RightTightEyeClosure, _, _ = get_measurements_from_data(Patient._Tight_Eye_Closure._shape, Patient._Tight_Eye_Closure._lefteye, Patient._Tight_Eye_Closure._righteye, Patient._Tight_Eye_Closure._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    Leftooooo, Rightooooo, _, _ = get_measurements_from_data(Patient._ooooo._shape, Patient._ooooo._lefteye, Patient._ooooo._righteye, Patient._ooooo._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)
    Lefteeeek, Righteeeek, _, _ = get_measurements_from_data(Patient._eeeek._shape, Patient._eeeek._lefteye, Patient._eeeek._righteye, Patient._eeeek._points, Patient._CalibrationType, Patient._CalibrationValue, Patient._reference_side)

        # 1) BrowRaise Elevation at rest
    a_left, a_right = LeftResting.BrowHeight, RightResting.BrowHeight
    if Patient._reference_side == 'Right':
        Brow_at_rest = a_left/a_right
    else:
        Brow_at_rest = a_right/a_left
    
    Brow_at_rest = np.round(Brow_at_rest*100,1)
    
    
    # 2) Palpebral Fissure width at rest
    c_left, c_right = LeftResting.PalpebralFissureHeight, RightResting.PalpebralFissureHeight

    if Patient._reference_side == 'Right':
        PalpebralFissure_at_rest = c_right/c_left
    else:
        PalpebralFissure_at_rest = c_left/c_right
    
    PalpebralFissure_at_rest = np.round(PalpebralFissure_at_rest*100,1)
    
    # 3) Oral commissure at rest 
    e_right, d_right = np.sin((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition, np.cos((RightResting.SmileAngle-90)*np.pi/180)*RightResting.CommissurePosition
    e_left, d_left = np.sin((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition, np.cos((LeftResting.SmileAngle-90)*np.pi/180)*LeftResting.CommissurePosition
    if Patient._reference_side == 'Right':
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
    
    # 4) NLF Angle at rest
    if RightResting.NLF_angle == 0 or LeftResting.NLF_angle == 0:
        if RightResting.NLF_angle == 0 and LeftResting.NLF_angle == 0:
            #if both sides are 0 the score is 100
            NLF_at_rest = 100
        else:
            #if only 1 side is 0 then the score is zero
            NLF_at_rest = 0
    else:
        if Patient._reference_side == 'Right':
            if LeftResting.NLF_angle > RightResting.NLF_angle:
                NLF_at_rest = (90 - LeftResting.NLF_angle)/(90 - RightResting.NLF_angle)
            else:
                NLF_at_rest = LeftResting.NLF_angle/RightResting.NLF_angle
        else:
            if RightResting.NLF_angle > LeftResting.NLF_angle:
                NLF_at_rest = (90 - RightResting.NLF_angle)/(90 - LeftResting.NLF_angle)
            else:
                NLF_at_rest = RightResting.NLF_angle/LeftResting.NLF_angle
    NLF_at_rest = np.round(NLF_at_rest*100,1)
    
    ##Dynamic Measures 
    # 5) Brow Elevation 
    b_left, b_right = LeftBrowRaise.BrowHeight, RightBrowRaise.BrowHeight
    if Patient._reference_side == 'Right':
        if (b_right - a_right) == 0:
            BrowRaise = 0
        else:
            BrowRaise = (b_left - a_left)/(b_right - a_right)
    else:
        if (b_left - a_left) == 0:
            BrowRaise = 0
        else:
            BrowRaise = (b_right - a_right)/(b_left - a_left)
    
    
    BrowRaise = np.round(BrowRaise*100,1)
    
    # 6)Eye closure gentle 
    g_left_gentle, g_right_gentle = LeftGentleEyeClosure.PalpebralFissureHeight , RightGentleEyeClosure.PalpebralFissureHeight
    if g_left_gentle<1:g_left_gentle=0
    if g_right_gentle<1:g_right_gentle=0
    #g might be negative (measurement errors)
    if Patient._reference_side == 'Right':
        GentleEyeClosure = (c_left - abs(g_left_gentle))/c_left
    else:
        GentleEyeClosure = (c_right - abs(g_right_gentle))/c_right
        
    GentleEyeClosure = np.round(GentleEyeClosure*100,1)
    
    # 7)Eye closure full 
    g_left_full, g_right_full = LeftTightEyeClosure.PalpebralFissureHeight, RightTightEyeClosure.PalpebralFissureHeight 
    if g_left_full<1:g_left_full=0
    if g_right_full<1:g_right_full=0
    if Patient._reference_side == 'Right':
        FullEyeClosure = (c_left - abs(g_left_full))/c_left
    else:
        FullEyeClosure = (c_right - abs(g_right_full))/c_right
        
    FullEyeClosure = np.round(FullEyeClosure*100,1)
    
    
    # 8) Oral Commissure with Smile
    # question for Tessa -> Is this with small or large smile? I'll do it with large smile for the moment
    f_left, f_right = LeftResting.CommissurePosition, RightResting.CommissurePosition
    h_left, h_right = LeftBigSmile.CommissurePosition, RightBigSmile.CommissurePosition
    #if with small smile, then comment above line an uncomment line below
    # h_left, h_right = LeftSmallSmile.CommissurePosition, RightSmallSmile.CommissurePosition
    if Patient._reference_side == 'Right':
        if (h_right - f_right) == 0:
            OralCommissureWithSmile = 0
        else:
            OralCommissureWithSmile =  (h_left - f_left)/(h_right - f_right)
    else:
        if (h_left - f_left) == 0:
            OralCommissureWithSmile = 0
        else:
            OralCommissureWithSmile = (h_right - f_right)/(h_left - f_left)
        
    OralCommissureWithSmile = np.round(OralCommissureWithSmile*100,1)
    
    #9) Lower Lip EEE
    
    j_left, j_right = Lefteeeek.LowerLipHeight, Righteeeek.LowerLipHeight
    if Patient._reference_side == 'Right':
        #making sure that it will work if j_right is zero 
        try:
            LowerLipEEE = j_left/j_right
        except:
            LowerLipEEE = 0
    else:
        #making sure that it will work if j_left is zero 
        try:
            LowerLipEEE = j_right/j_left
        except:
            LowerLipEEE = 0  
        
    LowerLipEEE = np.round(LowerLipEEE*100,1)    
    
    #Dynamic_Score = np.array([abs(100-BrowRaise), abs(100-GentleEyeClosure), abs(100-FullEyeClosure), abs(100-OralCommissureWithSmile), abs(100-LowerLipEEE)]).sum()
    #np.round(Dynamic_Score,1)
    
    
    ##Synkineis Measurements
    #Ocular synkinesis 
    k1_left, k1_right = LeftBigSmile.PalpebralFissureHeight, RightBigSmile.PalpebralFissureHeight
    k2_left, k2_right = Leftooooo.PalpebralFissureHeight, Rightooooo.PalpebralFissureHeight
    if Patient._reference_side == 'Right':
        OcularSynkinesis1 = k1_left/k1_right
        OcularSynkinesis2 = k2_left/k2_right
    else:
        OcularSynkinesis1 = k1_right/k1_left
        OcularSynkinesis2 = k2_right/k2_left
    
    if OcularSynkinesis1 <=  OcularSynkinesis2:
         OcularSynkinesis =  OcularSynkinesis1 
    else:
         OcularSynkinesis =  OcularSynkinesis2
            
    OcularSynkinesis = np.round(OcularSynkinesis*100,1)
    
    
    #apply corrections to remove everything less than zero 
    if Brow_at_rest < 0: Brow_at_rest = 0
    if Brow_at_rest > 200: Brow_at_rest = 200
    if PalpebralFissure_at_rest < 0: PalpebralFissure_at_rest = 0
    if PalpebralFissure_at_rest > 200: PalpebralFissure_at_rest = 200
    if OralCommissure_at_rest < 0: OralCommissure_at_rest = 0
    if OralCommissure_at_rest > 200: OralCommissure_at_rest = 200
    if NLF_at_rest < 0: NLF_at_rest = 0
    if NLF_at_rest > 200: NLF_at_rest = 200

    if BrowRaise < 0: BrowRaise = 0
    if BrowRaise > 100: BrowRaise = 100
    if GentleEyeClosure < 0: GentleEyeClosure = 0
    if GentleEyeClosure > 100: GentleEyeClosure = 100
    if FullEyeClosure < 0: FullEyeClosure = 0
    if FullEyeClosure > 100: FullEyeClosure = 100
    if OralCommissureWithSmile <0: OralCommissureWithSmile = 0
    if OralCommissureWithSmile >100: OralCommissureWithSmile = 100
    if LowerLipEEE <0: LowerLipEEE = 0
    if LowerLipEEE >100: LowerLipEEE = 100
    if OcularSynkinesis <0: OcularSynkinesis = 0
    if OcularSynkinesis >100: OcularSynkinesis = 100
    
    
    
    #Computing the score based on Tessa's idea

    score_brow_rest = 100 - abs(100-Brow_at_rest)
    score_PalpebralFissure_rest = 100 - abs(100-PalpebralFissure_at_rest)
    score_OralCommissure_rest = 100 - abs(100-OralCommissure_at_rest)
    score_NLF_rest = 100 - abs(100-NLF_at_rest)

    score_Brow_Raise = BrowRaise #100-abs(100-BrowRaise)
    score_GentleEyeClosure = GentleEyeClosure #100-abs(100-GentleEyeClosure)
    score_FullEyeClosure = FullEyeClosure #100- abs(100-FullEyeClosure)
    score_OralCommissureWithSmile = OralCommissureWithSmile #100 - abs(100-OralCommissureWithSmile)
    score_LowerLipEEE = LowerLipEEE #100 - abs(100-LowerLipEEE)
    
    score_OcularSynkinesis = OcularSynkinesis #100-abs(100-OcularSynkinesis)

    StaticScore = (score_brow_rest + score_PalpebralFissure_rest + score_OralCommissure_rest + score_NLF_rest)/4
    DynamicScore = (score_Brow_Raise + score_GentleEyeClosure + score_FullEyeClosure+score_OralCommissureWithSmile + score_LowerLipEEE)/5
    SynkinesisScore = score_OcularSynkinesis
    Total_Score = (score_brow_rest + score_PalpebralFissure_rest + score_OralCommissure_rest + 
                    score_NLF_rest + score_Brow_Raise + score_GentleEyeClosure + 
                    score_FullEyeClosure + score_OralCommissureWithSmile + score_LowerLipEEE +
                    score_OcularSynkinesis)/10
    
    return (Brow_at_rest, PalpebralFissure_at_rest, OralCommissure_at_rest, NLF_at_rest,
        BrowRaise, GentleEyeClosure, FullEyeClosure, OralCommissureWithSmile, LowerLipEEE,
         OcularSynkinesis, StaticScore, DynamicScore, SynkinesisScore, Total_Score)

          