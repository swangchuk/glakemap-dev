"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""

# Load system operators and modules
print ('Loading modules... ^_^')
import time
start_time = time.time()
import os
import arcpy
arcpy.env.overwriteOutput = True
from arcpy.sa import *
print('Loading module done! ^__^\n')

from dirext.dirextmngmt import DirMngmt
from dirext.dirextmngmt import FileExtMngmt



class ReadDatasets(FileExtMngmt):


    def read_data(self, file_ext):

        self.file_ext = file_ext

        for r, d, f in os.walk(os.path.join(self.main_dir)):
            for file in f:
                if file.endswith(self.file_ext): # 'NDWI_Mosaiced_Blue.tif'
                    data_path = os.path.join(r, file)
                    head, tail = os.path.split(data_path)
                    print ('Head: {}, Tail: {}'.format(head, tail))
                    path_basename = os.path.basename(head)
                    print ('Basename: {}'.format(path_basename))
                    if tail.endswith('.tif.aux.xml'):
                        continue
                    elif tail.endswith('tif.ovr'):
                        continue
                    elif tail.endswith('.tif.xml'):
                        continue
                    elif tail.endswith(self.file_ext[-4:]):
                        file_path = os.path.join(head, tail)
                        print('Path: {}'.format(file_path))
                        print('Reading {} raster done!\n\n'.format(self.file_ext))
                        data = arcpy.Raster(file_path)
        return data



class Thresholds():

    @staticmethod
    def threshold(thresh):
        return thresh



class GlacierDataset():


    @staticmethod
    def glacier_dir(gd_path):
        return gd_path




class RuleBasedSegmentation(DirMngmt):


    def __init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3, proj_pcs, proj_gcs, glacier_path, lake_size, lake_searh_dist):
        super(RuleBasedSegmentation, self).__init__(main_dir, subfolder_1, subfolder_2, subfolder_3)
        self.proj_pcs = proj_pcs
        self.proj_gcs = proj_gcs
        self.glacier_path = glacier_path
        self.lake_size = lake_size
        self.lake_searh_dist = lake_searh_dist



    @staticmethod
    def raster2polygon(raster_name, outPolygon):
        field = "VALUE"
        ras2poly = arcpy.RasterToPolygon_conversion(raster_name, outPolygon, "SIMPLIFY", field)
        return ras2poly



    @staticmethod
    def add_polygon_attributes(file_path, pcs_code, gcs_code):
        properties = "AREA"
        length_unit = "KILOMETERS"
        area_unit = "SQUARE_KILOMETERS"
        # coordinate_system = pcs_code
        properties_1 = "CENTROID"
        properties_2 = 'PERIMETER_LENGTH'
        print('Adding X,Y coordinates into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties_1, length_unit, area_unit, gcs_code)
        print('Adding parimeter of a polygon into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties_2, length_unit, area_unit, pcs_code)
        # Generate the extent coordinates using Add Geometry Properties tool
        print('Calculating area and adding area into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties, length_unit, area_unit, pcs_code)
        #coordinate_system_coord = GCS
        DropField = 'gridcode' #Delete gridcode from the attribute table
        print('Deleting gridcode field from the table...')
        arcpy.DeleteField_management(file_path, DropField)



    @staticmethod
    def select_featureby_size(file_path, lake_size):
        file_dir = os.path.split(file_path)[0]
        feature = os.path.join(file_dir, 'RasterToPolygon_Select.shp')
        where_clause = 'POLY_AREA>=' + str(lake_size) #Select area greter than 0.01 km2
        # Execute Select
        print('Extracting lake areas larger than {} km^2'.format(lake_size))
        arcpy.Select_analysis(file_path, feature, where_clause)
        return feature



    @staticmethod
    def select_featureby_location(file_path, gd, lake_searh_dist):
        file_dir = os.path.split(file_path)[0]
        feature = os.path.join(file_dir, 'RasterToPolygon_Select.shp')
        distance = 'WITHIN_A_DISTANCE' 
        search_distance = str(lake_searh_dist) + ' Meters'
        Selection_Type = 'NEW_SELECTION'
        print('Selecting lakes within the distance of {} meters'.format(lake_searh_dist))
        arcpy.MakeFeatureLayer_management(feature, 'select_feature_lyr') # Makes fearure layer
        arcpy.SelectLayerByLocation_management('select_feature_lyr', distance, gd, search_distance, Selection_Type)
        OutPut_SelectLayerByLocation = os.path.join(file_dir, 'SelectLayerByLocation_V0.shp')
        arcpy.CopyFeatures_management('select_feature_lyr', OutPut_SelectLayerByLocation)
        print('Done!')




    def rule_based_imgseg(self, filename, ndwi_blue, ndwi_green, backscatter, bluet, greent1, greent2, rbt):

        self.filename = filename
        self.ndwi_blue = ndwi_blue
        self.ndwi_green = ndwi_green
        self.backscatter = backscatter
        self.bluet = bluet
        self.greent1 = greent1
        self.greent2 = greent2
        self.rbt = rbt

        arcpy.CheckOutExtension("spatial")
        arcpy.env.overwriteOutput = True
        
        imseg = Con((self.ndwi_blue>=self.bluet) & (self.ndwi_blue<= 0.95), 1,
                Con((self.ndwi_green>=self.greent1) & (self.backscatter<=self.rbt), 1,\
                Con((self.ndwi_green>=self.greent2) & (self.backscatter<=self.rbt), 1,
                Con((self.backscatter<=self.rbt), 2))))
        
        
        save_result = os.path.join(self.main_dir, self.subfolder_1, self.filename)
        print('save_result', save_result)
        print('Segmenting image..... ^_^')
        imseg.save(save_result)

        outPolygon = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_2, 'RasterToPolygon.shp')
        print('outPolygon', outPolygon)
        RuleBasedSegmentation.raster2polygon(save_result, outPolygon)
        print('Converting {} to raster done!'.format(outPolygon))

        outProjectData = os.path.join(os.path.split(outPolygon)[0], 'RasterToPolygon_TM.shp')
        print("OutProjectData", outProjectData)
        arcpy.Project_management(outPolygon, outProjectData, self.proj_pcs)
        RuleBasedSegmentation.add_polygon_attributes(outProjectData, self.proj_pcs, self.proj_gcs)
        feature = RuleBasedSegmentation.select_featureby_size(outProjectData, self.lake_size)
        RuleBasedSegmentation.select_featureby_location(feature, self.glacier_path, self.lake_searh_dist)
        


class CalZonalAttr():
    pass