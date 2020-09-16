"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Process S1 Data--------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import time
start_time = time.time()
from glakemap.dirext.dirextmngmt import DirMngmt
from glakemap.sentinel1.s1processor import ProcessSARData
from glakemap.sentinel1.s1processor import Reprojections
from glakemap.sentinel1.s1processor import MosaicDatastet

dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)



band_polarisation = ['VV'] # Add the band polarisation to be processed. Also supports multi-polarisation e.g. ['VV', 'VH']
process_data = ProcessSARData(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', ".zip", ".safe", band_polarisation)
process_data.makefolders()                   
process_data.unzipfiles()
process_data.process_sar_data()



from glakemap.sptref.spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)
processed_band_pol2 = ['_VV_db.img'] # Add the band polarisation to be processed. Also supports multi-polarisation e.g. ['_VV_db.img', '_VH_db.img']
repro = Reprojections(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', processed_band_pol2, gcs)
repro.reprojection()



from glakemap.sptref.spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)
filter_dB = ['*_VV_db_COPY.tif'] # Add the band polarisation to be processed. Also supports multi-polarisation e.g. ['*_VV_db_COPY.tif', '*_VH_db_COPY.tif']
mosaic_data = MosaicDatastet(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', filter_dB, gcs)
mosaic_data.makefolders()
mosaic_data.mosaic()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Process S2 Data--------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import time
from glakemap.sentinel2.s2processor import CalculateNDWI
from glakemap.sentinel2.s2processor import MosaicNDWIData
from glakemap.sptref.spatialref import SpatialReference

dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
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


from glakemap.sentinel2.s2processor import MosaicS2Data
merges2dta = MosaicS2Data(main_directory, 'Sentinel2', '', 's2_processed_data', '','', '')

filter_s2_data = ['_B08.jp2'] # '_B02.jp2','_B03.jp2', '_B04.jp2', '_B08.jp2'
s2dta = merges2dta.mosaics2data(filter_s2_data, gcs)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Process Dem Data-------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)


from glakemap.dem.demprocessor import MoveDemFiles
move_files = MoveDemFiles(main_directory, "Dem", "dem_unziped_data", 'dem_processed_data', ".zip", ".hgt", '')
src_dir = r'C:\\Users\\Sonam\\.snap\\auxdata\\dem\\SRTM 1Sec HGT'
move_files.move_over(src_dir, 'test')



from glakemap.dem.demprocessor import DemProcessor
from glakemap.sptref.spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645)

dem = DemProcessor(main_directory, "Dem", "dem_unziped_data", 'dem_processed_data', ".zip", ".hgt", '')
dem.unzipfiles()
dem.makefolders()
dem.mosaic_dem_cal_slp('SRTM1_GDB.gdb', 'SRTM1_Mosaic', 'SRTM1_Mosaiced.tif', gcs, 'SRTM1_Slope', 'SRTM1_Slope.tif', 0.00001036)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Rule-based ImgSeg------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import time
start_time = time.time()
import os
dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

from glakemap.imgseg.imgseg import ReadDatasets
from glakemap.imgseg.imgseg import Thresholds
from glakemap.imgseg.imgseg import RuleBasedSegmentation
from glakemap.sptref.spatialref import SpatialReference as spt
from glakemap.imgseg.imgseg import GlacierDataset as gd

data = ReadDatasets(main_directory, "rule-imgseg", "", "", "", "", "")
data.makefolders()
def reading_data(file_exten):
       try:
              return data.read_data(file_exten)
              
       except UnboundLocalError:
              print("------------> {} File NOT found!\n".format(file_exten))


sar_data = reading_data('_VV.tif')
ndwi_blue_data = reading_data('NDWI_Mosaiced_Blue.tif')
ndwi_green_data = reading_data('NDWI_Mosaiced_Green.tif')

# slope_data = reading_data('Resam_SRTM1_Slope.tif')

thresh = Thresholds()

ndwi_bluet = thresh.threshold(0.5)
ndwi_green_t1 = thresh.threshold(0.3)
ndwi_green_t2 = thresh.threshold(0.05)
backscattert = thresh.threshold(-14.0)


glacier_path = gd.glacier_dir("E:\Glacier_GL_Data\GLIMS\glims_db_20190530\glims_polygons.shp")
lake_size = 0.01 # in km2
lake_searh_distance = 10000 # in meter

ruleimgseg = RuleBasedSegmentation(main_directory, "rule-imgseg", "raster2polygon", "", spt.pcs(32645), spt.gcs(4326), glacier_path, lake_size, lake_searh_distance)

ruleimgseg.makefolders()
ruleimgseg.rule_based_imgseg('Glacial_Lakes_Segmented.tif', ndwi_blue_data, ndwi_green_data, sar_data,
ndwi_bluet, ndwi_green_t1, ndwi_green_t2, backscattert)



import os
dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

# from imgseg.imgseg import ReadDatasetsPath
from glakemap.imgseg.imgseg import ZonesFeature
from glakemap.imgseg.imgseg import CalZonalAttr
zone_dir = ZonesFeature(main_directory, "rule-imgseg", "", "", "", "SelectLayerByLocation_V0.shp", "")
zone_path = zone_dir.zone()


zone_attr = CalZonalAttr(main_directory, "rule-imgseg", "", "", "", "", "")

ndwi_blue_data_pth = zone_attr.read_data('NDWI_Mosaiced_Blue.tif')
ndwi_green_data_pth = zone_attr.read_data('NDWI_Mosaiced_Green.tif')
sar_data_pth = zone_attr.read_data('_VV.tif')
slope_data_pth = zone_attr.read_data('Resam_SRTM1_Slope.tif')
nir_pth = zone_attr.read_data('08_Band.tif')
dem_pth = zone_attr.read_data('_Mosaiced.tif')

file_list = [ndwi_blue_data_pth, ndwi_green_data_pth, sar_data_pth, slope_data_pth, nir_pth, dem_pth]

zone_attr.zonal_attr(file_list, zone_path, 'Feature_Data_V1.csv')

end_time = time.time()
print('Time taken to process Sentinel-2 data: {} minutes'.format((end_time-start_time)/60))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Random Forest-------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
dir_path = "E:\Poiqu_GL\Poiqu" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

from glakemap.randforest.randomforest import RandomForestData

rf = RandomForestData(main_directory, "random_forest", "", "")
rf.makefolders()

rf_file_pth = rf.rf_data("_Data_V1.csv")





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
