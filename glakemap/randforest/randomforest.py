"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""


import os
import pickle
import pandas as pd
from glakemap.dirext.dirextmngmt import DirMngmt



class RandomForestData(DirMngmt):

    
    def rf_data(self, file_extension):

        self.file_extension = file_extension

        for r, d, f in os.walk(os.path.join(self.main_dir)):
            for file in f:
                if file.endswith(self.file_extension):
                    rf_file = os.path.join(r, file)
        return rf_file



class ProcessRFData():
    pass

