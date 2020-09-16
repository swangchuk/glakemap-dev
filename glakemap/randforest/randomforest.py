"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""


import os
import sklearn
import pickle
import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import ExcelWriter

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
    

    @staticmethod
    def process_csv_data(file):


        drop_list = ['FID', 'OID', 'COUNT', 'AREA', 'COUNT']

        duplicates_col_names = []

        df = pd.read_csv(file)
        df = df.drop(columns='OID')
        df = df.dropna()
        print("Raw Column Names : {}\n".format(list(df.columns)))
        print('Shape: {}\n'.format(df.shape))
        # print(df.head())
        col_names = list(df.columns)
        # print(col_names)


        for col_names in df.columns:
            for d in drop_list:
                if d in  col_names:
                    duplicates_col_names.append(col_names)
        
    
        for items in duplicates_col_names:
            if 'POLY_AREA' in  items:
                duplicates_col_names.remove(items)
         

        print('Duplicates_col_names\n', duplicates_col_names)
        print(len(duplicates_col_names))

        df = df.drop(columns=duplicates_col_names)
        print('New dataframe cols: {}; length: {}'.format(list(df.columns), len(list(df.columns))))
        return df







