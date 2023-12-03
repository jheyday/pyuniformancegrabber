import subprocess
import os
import pandas as pd
from contextlib import redirect_stdout
import io



class uniformance():
    def __init__(self, hostname, port=3000, user='', password='') -> None:
        self.Hostname               = hostname
        self.Port                   = port
        self.Username               = user
        self.Password               = password
        self._Taglist                = []
        self._Starttime             = 'NOW-1D'
        self._Endtime               = 'NOW'
        self._SampleFrequency       = 0
        self._SampleFrequencyType   = "Raw"
        self._UseSampleFrequency    = False
        self._ReductionType         = 'None'
        self._ReductionFrequency    = 60
        self._ReductionOffset       = 'Around'
        self.exe_path = os.path.join(os.path.dirname(__file__),
                                     'phdapinetinterface.exe')

    ###########################################################################
    # Other Functions
    ###########################################################################
    def show_parameters(self):
        server_details  = pd.DataFrame({'Hostname': self.Hostname,
                                       'Port': self.Port,
                                       'Username': self.Username,
                                       'Password': self.Password,
                                       }, index=[0])
        parameters      = pd.DataFrame({'Starttime': self._Starttime,
                                       'Endtime': self._Endtime,
                                       'UseSampleFreq': self._UseSampleFrequency,
                                       'SampleFreq': self._SampleFrequency,
                                       'SampleFreqType': self._SampleFrequencyType,
                                       'ReductionType': self._ReductionType,
                                       'ReductionFreq': self._ReductionFrequency,
                                       'ReductionOffset': self._ReductionOffset
                                       }, index=[0])
        
        return [server_details, parameters]
        
    ###########################################################################
    # Tag Functions
    ###########################################################################
    
    def check_tag(self, tag_name):
        result = subprocess.run([self.exe_path, "checktag",
                                "-h", self.Hostname,
                                "-P", str(self.Port),
                                "-u", self.Username,
                                "-p", self.Password,
                                "-t", tag_name
                                ], shell=True, capture_output=True,text=True)

        stdout = result.stdout.strip("\r\n")
        if stdout.endswith("found"):
            print(tag_name+' was found')
            return(0)
        elif stdout.endswith("system"):
            print(tag_name+" was not found, check tagname and try again")
            return(1)
        else:
            print("Connection to PHD failed, Check server details or try again")
            return(1) 
        
    def add_tag(self, tagname, unsafe=False):
        if not(isinstance(tagname, list)):
            tagname = [tagname]

        
            
        for tag in tagname:
            if tag in self._Taglist:
                print(tag+' Already exists in taglist')
                continue
            if unsafe == True:
                self._Taglist.append(tag)
                print(tag+" added to taglist")
                continue
            text_trap = io.StringIO()
            with redirect_stdout(text_trap):
                checktag = self.check_tag(tag)
            
            if checktag == 0:
                self._Taglist.append(tag)
                print(tag+" added to taglist")
            else:
                print(tag+ " Not added, check tagname or try again")
        
        return(self._Taglist)
    
    def show_tags(self):
        return(self._Taglist)
    
    def clear_tags(self):
        self._Taglist = []
    
    def remove_tag(self, tagname):
        if tagname in self._Taglist:
            self._Taglist.remove(tagname)
            print(tagname+" Removed from taglist")
            return(0)
        else:
            print(tagname+ ' was not found in list')
            return(1)  
    
    ###########################################################################
    # Sampling Functions
    ###########################################################################
    
    def set_SampleFrequency(self, samplefrequency):
        if not(str(samplefrequency).isnumeric()):
            print("Sample frequency must be numeric")
            return(1)
        
        self._SampleFrequency = samplefrequency
        
        if self._UseSampleFrequency == False:
            self._UseSampleFrequency = True
            print("useSampleFrequency set to true, this can be disabled via set_useSampleFrequency")
            
        if self._SampleFrequencyType == 'Raw':
            self._SampleFrequencyType = 'Snapshot'
            print("_SampleFrequencyType set to Snapshot, this can be changed via set_SampleFrequencyType")
            
    def set_useSampleFrequency(self, usesamplefrequency):
        if not(isinstance(usesamplefrequency, bool)):
            print("useSampleFrequency must be True or False")
            return(1)
        
        if self._SampleFrequencyType == 'Raw' and usesamplefrequency == True:
            print('Ensure SampleFrequencyType supports sampling ie Snapshot')
        
        self._UseSampleFrequency = usesamplefrequency
        
    def set_SampleType(self, sample_type):
        valid_sampling = ["Snapshot", "Average", "Resampled", "Raw", "InterpolatedRaw"]
        if sample_type in valid_sampling:
            self._SampleFrequencyType = sample_type
            print("Sampling Type set to "+sample_type)
            return(0)
        
        print('sampling type must be one of "Snapshot", "Average", "Resampled", "Raw", "InterpolatedRaw"')
        return(1)
    
    def set_ReductionFrequency(self, reduction_frequency):
        if not(str(reduction_frequency).isnumeric()):
            print("Sample frequency must be numeric")
            return(1)
        
        self._ReductionFrequency = reduction_frequency
        
        
    def set_ReductionType(self, reduction_type):
        valid_sampling = ["None", "Average", "Delta", "Minimum", "Maximum",
                          "StandardDeviation", "RegressionSlope",
                          "RegressionConstant","RegressionDeviation","First",
                          "Last"]
        if reduction_type in valid_sampling:
            self._ReductionType = reduction_type
            print("Reduction Type set to "+reduction_type)
            return(0)
        
        print('sampling type must be one of "None", "Average", "Delta", \
            "Minimum", "Maximum", "StandardDeviation", "RegressionSlope", \
                "RegressionConstant","RegressionDeviation","First","Last"')
        return(1)
    
    def set_ReductionOffset(self, reduction_offset):
        valid_offsets = ["After", "Around", "Before"]
        
        if reduction_offset in valid_offsets:
            self._ReductionOffset = reduction_offset
            return(0)
        
        print('Ensure Reduction Type matches one of "After","Around", "Before".')
        return(1)
    
    ###########################################################################
    # Time Functions
    ###########################################################################
    
    def set_starttime(self, starttime):
        self._Starttime = starttime
        
    def set_endtime(self, endtime):
        self._Endtime = endtime
    
    ###########################################################################
    # Result Functions
    ###########################################################################
    
    def get_results(self):
        dataframe_list = []
        for tags in self._Taglist:
            datain = io.StringIO()
            result = subprocess.run([self.exe_path, "getdata",
                                    "-h", self.Hostname,
                                    "-P", str(self.Port),
                                    "-u", self.Username,
                                    "-p", self.Password,
                                    "-t", tags,
                                    "-s", self._Starttime,
                                    "-e", self._Endtime,
                                    "-g", str(self._UseSampleFrequency),
                                    "-f", str(self._SampleFrequency),
                                    "-F", self._SampleFrequencyType,
                                    "-r", str(self._ReductionFrequency),
                                    "-R", self._ReductionType,
                                    "-o", self._ReductionOffset
                                    ], shell=True, capture_output=True, text=True)
            datain.write(result.stdout)
            dataframe_list.append(pd.read_xml(datain))
        return(dataframe_list)
        
        
#a = uniformance("MALSHW1")
#b = a.show_parameters()
#print(b[0])
#print(b[1])
#a.add_tag('A.RL_AI7361.BATCH')
#m = a.get_results()
#print(m[0])