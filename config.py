
# -------------------Process S1 Data-----------------------#
from sentinel1.s1processor import SARDataOperators


import time
start_time = time.time()

from sentinel1.s1processor import ProcessSARData

from dirext.maindir import main_directory
main_directory = main_directory()
print(main_directory)



from s1processor import ProcessSARData
from s1processor import Reprojections
from s1processor import MosaicDatastet
main_directory = main_directory()



band_polarisation = ['VV'] # band polarization to be processed
process_data = ProcessSARData(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', ".zip", ".safe", band_polarisation)
process_data.makefolders()                   
process_data.unzipfiles()
process_data.process_sar_data()



from spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)
processed_band_pol2 = ['_VV_db.img']
repro = Reprojections(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', processed_band_pol2, gcs)
repro.reprojection()



from spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)
filter_dB = ['*_VV_db_COPY.tif']
mosaic_data = MosaicDatastet(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', filter_dB, gcs)
mosaic_data.makefolders()
mosaic_data.mosaic()



# -------------------Process S2 Data-----------------------#

import os
import time
from maindir import main_directory
from s2processor import CalculateNDWI
from s2processor import MosaicNDWIData
from spatialref import SpatialReference
main_directory = main_directory()
print(main_directory)
os.listdir(main_directory)
start_time = time.time()



dir_mngmt = CalculateNDWI(main_directory, 'Sentinel2', 's2_unziped_data', 's2_processed_data', '.zip', '_MSIL1C.xml', '')
dir_mngmt.makefolders()
dir_mngmt.unzipfiles()
dir_mngmt.calculate_ndwi()



spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)
extens = ['Green.tif', 'Blue.tif'] # Static
mosaic_extens = MosaicNDWIData(main_directory, 'Sentinel2', 's2_unziped_data', 's2_processed_data', '', extens, '')
mosaic_extens.makefolders()
mosaic_extens.list_files()
mosaic_extens.mosaic_ndwi(gcs)

end_time = time.time()
print('Time taken to process Sentinel-2 data: {} minutes'.format((end_time-start_time)/60))


# -------------------Process Dem Data-----------------------#

import os
from maindir import main_directory
main_directory = main_directory()
print(main_directory)
os.listdir(main_directory)



from demprocessor import MoveDemFiles
move_files = MoveDemFiles(main_directory, "Dem", "dem_unziped_data", 'dem_processed_data', ".zip", ".hgt", '')
src_dir = r'C:\\Users\\Sonam\\.snap\\auxdata\\dem\\SRTM 1Sec HGT'
move_files.move_over(src_dir, 'test')



from demprocessor import DemProcessor
from spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)

dem = DemProcessor(main_directory, "Dem", "dem_unziped_data", 'dem_processed_data', ".zip", ".hgt", '')
# dem.unzipfiles()
dem.makefolders()
dem.mosaic_dem_cal_slp('SRTM1_GDB.gdb', 'SRTM1_Mosaic', 'SRTM1_Mosaiced.tif', gcs, 'SRTM1_Slope', 'SRTM1_Slope.tif', 0.00001036)


# -------------------Rule-based ImgSeg-----------------------#






""""
#...............................
       #sub modules
# import MosaicS2Data
#............................... 
import DataForDEM # Check Sentinel2DataProcessing.py
 
import DemDataProcessing
#********************Main and Post-Processing********************#

import RuleBasedSegmentation
#...............................
       #sub modules
#import Zonal_Stat_App

#import Zonal_Stat_Train
#...............................  

#Change Python Environemnt: Random Forest (Python 37)
#Perform Random forest classification
import random_forest_classification_csv_V0  # for building model 

import GLakeMap_Model_Prediction  # for predicting class label

#Change Python Environemnt back to Python 27 64 bit
#Append Random Forest Predictions (value==1) and select polygons

#import Append_Pred_V0

#----------------------------------------------------------------------------------------------
from Append_Pred_V1 import Convert_shp_to_CSV
from Append_Pred_V1 import Extract_glacial_lakes
from Append_Pred_V1 import CSV_filepath_direc

from Append_Pred_V1 import Convert_To_CSV_File

from Append_Pred_V1 import*
from MainDirectory import MainDirectory
main_directory=MainDirectory()#Main_Directory

shp_to_csv = Convert_shp_to_CSV(main_directory, "Data_predicted.csv", 'Location_V0.shp')

csv_file, shp_file = shp_to_csv.read_pred_csv_file()

egl = Extract_glacial_lakes(main_directory, shp_file, csv_file, 'RasterToPolygon', 'Swiss_Alps_gl.shp')
sa = egl.selectAnalysis()

cfd = CSV_filepath_direc(main_directory, "Predicted_Dataset")
out_dir, f_dir, f_na = cfd.csv_file_name()
print(out_dir)

ctcf = Convert_To_CSV_File(sa, out_dir, f_na + ".csv")
out_csv_file = ctcf.csv_file()
print(out_csv_file)
