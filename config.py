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

dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
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
pcs = spatial_ref.pcs(32645) # Check the projected coordinate system for your region of interest and change accordingly
processed_band_pol2 = ['_VV_db.img'] # Add the band polarisation to be processed. Also supports multi-polarisation e.g. ['_VV_db.img', '_VH_db.img']
repro = Reprojections(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', processed_band_pol2, gcs)
repro.reprojection()

from glakemap.sptref.spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645) # Check the projected coordinate system for your region of interest and change accordingly
filter_dB = ['*_VV_db_COPY.tif'] # Add the band polarisation to be processed. Also supports multi-polarisation e.g. ['*_VV_db_COPY.tif', '*_VH_db_COPY.tif']
mosaic_data = MosaicDatastet(main_directory, "Sentinel1", "s1_unziped_data", 's1_processed_data', '', '', filter_dB, gcs)
mosaic_data.makefolders()
mosaic_data.mosaic()

end_time = time.time()
print('Time taken to process Sentinel-1 data: {} minutes'.format((end_time-start_time)/60))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Process S2 Data--------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import time
from glakemap.sentinel2.s2processor import CalculateNDWI
from glakemap.sentinel2.s2processor import MosaicNDWIData
from glakemap.sptref.spatialref import SpatialReference

dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645) # Check the projected coordinate system for your region of interest and change accordingly

start_time = time.time()
dir_mngmt = CalculateNDWI(main_directory, 'Sentinel2', 's2_unziped_data', 's2_processed_data', '.zip', '_MSIL1C.xml', '') # _MSIL1C.xml
dir_mngmt.makefolders()
dir_mngmt.unzipfiles()
dir_mngmt.calculate_ndwi()

extens = ['Green.tif', 'Blue.tif'] # Static
mosaic_extens = MosaicNDWIData(main_directory, 'Sentinel2', 's2_unziped_data', 's2_processed_data', '', extens, '')
mosaic_extens.makefolders()
mosaic_extens.list_files()
mosaic_extens.mosaic_ndwi(gcs)

from glakemap.sentinel2.s2processor import MosaicS2Data
merges2dta = MosaicS2Data(main_directory, 'Sentinel2', '', 's2_processed_data', '','', '')
filter_s2_data = ['_B08.jp2'] # '_B02.jp2','_B03.jp2', '_B04.jp2', '_B08.jp2'
s2dta = merges2dta.mosaics2data(filter_s2_data, gcs)

end_time = time.time()
print('Time taken to process Sentinel-2 data: {} minutes'.format((end_time-start_time)/60))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Process Dem Data-------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

from glakemap.dem.demprocessor import MoveDemFiles
move_files = MoveDemFiles(main_directory, "Dem", "dem_unziped_data", 'dem_processed_data', ".zip", ".hgt", '')
src_dir = r"C:\Users\Sonam\.snap\auxdata\dem\SRTM 1Sec HGT" # Dem data are automatically downloded while processing Sentinel-1 data. Find the folder where it is located and provide the path. Check .snap folder inside you PC.
move_files.move_over(src_dir, os.path.join(main_directory, "Dem", "raw_data"))

from glakemap.dem.demprocessor import DemProcessor
from glakemap.sptref.spatialref import SpatialReference
spatial_ref = SpatialReference()
gcs = spatial_ref.gcs(4326)
pcs = spatial_ref.pcs(32645) # Check the projected coordinate system for your region of interest and change accordingly

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
dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
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

glacier_path = gd.glacier_dir("E:\Glacier_GL_Data\GLIMS\glims_db_20190530\glims_polygons.shp") # Download glacier outline from GLIMS and provide path to it.
lake_size = 0.01 # in km2
lake_searh_distance = 10000 # in meter
ruleimgseg = RuleBasedSegmentation(main_directory, "rule-imgseg", "raster2polygon", "", spt.pcs(32645), spt.gcs(4326), glacier_path, lake_size, lake_searh_distance)
ruleimgseg.makefolders()
ruleimgseg.rule_based_imgseg('Glacial_Lakes_Segmented.tif', ndwi_blue_data, ndwi_green_data, sar_data,
ndwi_bluet, ndwi_green_t1, ndwi_green_t2, backscattert)

import os
dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
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
# Python 3 can be used here

import os
dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path here
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

from glakemap.randforest.randomforest import RandomForestData
from glakemap.randforest.randomforest import ProcessRFData
from glakemap.randforest.randomforest import LoadModel
from glakemap.randforest.randomforest import ModelPrediction

enter_model_name = "glakemap.sav"
rf_dir = RandomForestData(main_directory, "random_forest", "", "")
rf_dir.makefolders()
rf_file_pth = rf_dir.rf_data("_Data_V1.csv")
print('Raw data path----------> : {}'.format(rf_file_pth))
rf_data = ProcessRFData()
df_rfdata = rf_data.process_csv_data(rf_file_pth)

save_csv_dir = os.path.join(dir_path, 'random_forest')
processed_csv_filename = os.path.join(save_csv_dir, 'processed_data.csv')
print('Processed data path----------> : {}'.format(processed_csv_filename))
processed_csv = df_rfdata.to_csv(processed_csv_filename, index=False)
rf_file_pth2 = rf_dir.rf_data("processed_data.csv")

model = LoadModel(main_directory, "random_forest", "", "")
rf_model = model.model(enter_model_name)

pred = ModelPrediction(main_directory, "random_forest", "", "")
in_data, predicted_result = pred.make_prediction(rf_model, rf_file_pth2, 'predicted_data.csv')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -------------------Post-Processing-------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Use python 2 with arcpy
import os
dir_path = r"C:\Users\Sonam\Documents\gt\glakemap-dev\data_directory" # Change the file path
from glakemap.dirext.dirextmngmt import DirMngmt
directory = DirMngmt(dir_path, '', '','')
main_directory = directory.main_direc()
print(main_directory)
os.listdir(main_directory)

from glakemap.pp.postprocess import ReadData
from glakemap.pp.postprocess import PostProcessing

read_data = ReadData(main_directory, "", "", "")
shp_file_path = read_data.read_post_process_data(main_directory, 'Location_V0.shp')
print(shp_file_path)

csv_file_path = read_data.read_post_process_data(main_directory, 'predicted_data.csv')
print(csv_file_path)

out_shp_filename = 'glacial_lakes_final2.shp'
out_csv_filename = 'glacial_lakes_final2.csv'

pp =  PostProcessing()
pp.post_process(shp_file_path, csv_file_path, out_shp_filename, out_csv_filename)

