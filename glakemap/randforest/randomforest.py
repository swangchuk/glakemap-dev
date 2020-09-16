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



class LoadModel(DirMngmt):
    
    
    def model(self, file_extension):

        self.file_extension = file_extension

        for r, d, f in os.walk(os.getcwd()):
            for file in f:
                if file.endswith(self.file_extension):
                    rf_model = os.path.join(r, file)
                    print('Model location; {}'.format(rf_model))
        return rf_model



class ProcessRFData():
    

    @staticmethod
    def process_csv_data(file):


        drop_list = ['FID', 'OID', 'COUNT', 'AREA', 'COUNT', 'SRTM1_Mosaiced_MEAN']

        duplicates_col_names = []

        df = pd.read_csv(file)
        print("Raw Column Names : {}\n".format(list(df.columns)))
        print('Shape: {}\n'.format(df.shape))
        col_names = list(df.columns)

        for col_names in df.columns:
            for d in drop_list:
                if d in  col_names:
                    duplicates_col_names.append(col_names)
        
    
        for items in duplicates_col_names:
            if 'POLY_AREA' in  items:
                duplicates_col_names.remove(items)
        

        def compactness_ratio(area, perimeter):
            cr = 4.0*3.14159*(area/(perimeter*perimeter))
            return cr
        df['CR'] = compactness_ratio(df.POLY_AREA, df.PERIMETER)


        print('Duplicates_col_names\n', duplicates_col_names)
        print(len(duplicates_col_names))
        df = df.drop(columns=duplicates_col_names)
        df = df.dropna()
        print('New dataframe cols: {}; length: {}'.format(list(df.columns), len(list(df.columns))))
        df2 = df.iloc[:, 6:13].values
        print(df2)
        return df



class ModelPrediction(DirMngmt):
    

    def make_prediction(self, model, data, output_file):
        self.model = model
        self.data = data
        self.output_file = output_file
        loaded_model = pickle.load(open(self.model, 'rb'))
        y_pred = loaded_model.predict(data.iloc[:, 6:13].values)
        df_pred = pd.DataFrame({"Label" : y_pred})
        dataset_ROI_Pred = pd.concat([self.data, df_pred], axis=1, sort=False)
        predicted_result_path = os.path.join(self.main_dir, self.subfolder_1, self.output_file)
        dataset_ROI_Pred.to_csv(predicted_result_path, encoding='utf-8', index=False)







