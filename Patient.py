


class PatientPhotograph(object):
    
    #this class contains all the information associated with a photo
    def __init__(self):
        self._photo = None  #this is a open cv image element
        self._file_name = None  #is the physical address of the photo
        self._name = '' #this is the file name
        self._extension = '' #this is the file extension
        self._expression = '' #this is the photo expression, there are seven different types of photos
        self._shape = None #this is the landmark localization provided by dlib
        self._lefteye = None #this si the position and diameter of left iris
        self._righteye = None #this si the position and diameter of right iris
        self._points = None
        self._boundingbox = None #this is the facial bounding-box provided by dlib
        # self._Tag = '' #this is the tag that goes in the Emotrics window
        # self._OpenEmotrics = True #this informs the main prgram if it should open Emotrics 
        #                           #for landmark localization. Emotrics will be open only 
        #                           #if the user double clikc on a photo
        # self._NewPatient = False #this variable is used to indicate if new photos 
        #                          #from new patients are beeing droped to the app. 
        #                          #In that case, the patient information is removed 
        #                          #so that it wont be shown next time the user 
        #                          #opens the results window 


class Patient(object):    
    #this class compiles the patient information
    def __init__(self):
        self._Resting = PatientPhotograph()
        # self._SmallSmile = PatientPhotograph()
        self._Big_Smile = PatientPhotograph()
        self._Brow_Raise = PatientPhotograph()
        self._Gentle_Eye_Closure = PatientPhotograph()
        self._Tight_Eye_Closure = PatientPhotograph()
        self._ooooo = PatientPhotograph()
        self._eeeek = PatientPhotograph()
        
        #additional info that is needed for processing 
        self._Patient_ID = None #Patient ID
        self._MRN = None #Medical Record Number
        self._reference_side = None #healthy side of the face
        
        self._CalibrationType='Iris'
        self._CalibrationValue=11.77
        self._ModelName = 'MEE'

