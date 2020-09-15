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
                if file.endswith(self.file_ext):
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
        properties_1 = "CENTROID"
        properties_2 = 'PERIMETER_LENGTH'
        print('Adding X,Y coordinates into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties_1, length_unit, area_unit, gcs_code)
        print('Adding parimeter of a polygon into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties_2, length_unit, area_unit, pcs_code)
        print('Calculating area and adding area into the attribute table...')
        arcpy.AddGeometryAttributes_management(file_path, properties, length_unit, area_unit, pcs_code)
        drop_field = 'gridcode' # Delete gridcode from the attribute table
        print('Deleting gridcode field from the table...')
        arcpy.DeleteField_management(file_path, drop_field)



    @staticmethod
    def select_featureby_size(file_path, lake_size):
        file_dir = os.path.split(file_path)[0]
        feature = os.path.join(file_dir, 'RasterToPolygon_Select.shp')
        where_clause = 'POLY_AREA>=' + str(lake_size)
        print('Extracting lake areas larger than {} km^2'.format(lake_size))
        arcpy.Select_analysis(file_path, feature, where_clause)
        return feature



    @staticmethod
    def select_featureby_location(file_path, glacier_data, lake_searh_dist):
        file_dir = os.path.split(file_path)[0]
        feature = os.path.join(file_dir, 'RasterToPolygon_Select.shp')
        distance = 'WITHIN_A_DISTANCE' 
        search_distance = str(lake_searh_dist) + ' Meters'
        Selection_Type = 'NEW_SELECTION'
        print('Selecting lakes within the distance of {} meters'.format(lake_searh_dist))
        arcpy.MakeFeatureLayer_management(feature, 'select_feature_lyr') # Makes fearure layer
        arcpy.SelectLayerByLocation_management('select_feature_lyr', distance, glacier_data, search_distance, Selection_Type)
        output_selectLayerByLocation = os.path.join(file_dir, 'SelectLayerByLocation_V0.shp')
        arcpy.CopyFeatures_management('select_feature_lyr', output_selectLayerByLocation)
        layer = 'select_feature_lyr2'
        arcpy.MakeFeatureLayer_management(output_selectLayerByLocation, layer) # Makes fearure layer
        print('Calculating distance of glacial lakes from a glacier...')
        arcpy.Near_analysis(layer, glacier_data, '', True, False, 'PLANAR')
        # return output_selectLayerByLocation



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
        print('Converting {} to shapefiles done!'.format(outPolygon))

        outProjectData = os.path.join(os.path.split(outPolygon)[0], 'RasterToPolygon_TM.shp')
        print("OutProjectData", outProjectData)
        arcpy.Project_management(outPolygon, outProjectData, self.proj_pcs)
        RuleBasedSegmentation.add_polygon_attributes(outProjectData, self.proj_pcs, self.proj_gcs)
        feature = RuleBasedSegmentation.select_featureby_size(outProjectData, self.lake_size)
        RuleBasedSegmentation.select_featureby_location(feature, self.glacier_path, self.lake_searh_dist)
        



class ZonesFeature(FileExtMngmt):

    def zone(self):
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for file in f:
                if file.endswith(self.file_extension):
                    zone_path = os.path.join(r, file)
        return zone_path



class ReadDatasetsPath(FileExtMngmt):
    

    def read_data(self, file_ext):

        self.file_ext = file_ext

        for r, d, f in os.walk(os.path.join(self.main_dir)):
            for file in f:
                if file.endswith(self.file_ext):
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
                        
        return file_path



class CalZonalAttr(ReadDatasetsPath):

        
        def zonal_attr(self, filenames, zone_data, csv_filename):
            self.filenames = filenames
            self.zone_data = zone_data
            self.csv_filename = csv_filename

            arcpy.CheckOutExtension("spatial")
            feature_layer_name = "feature_layer"
            arcpy.MakeFeatureLayer_management(self.zone_data, feature_layer_name) # Makes fearure layer

            zone_stat_ras = []
            
            for file in self.filenames:
                arcpy.env.extent = "MINOF"
                outTable_name = file[:-4] + '.dbf' # Table output names and extension in a list
                outZSaT = ZonalStatisticsAsTable(self.zone_data, "FID", file, outTable_name, "DATA", "MEAN")
                print ('Calculating zonal stat of {}'.format(file))
                zone_stat_ras.append(outZSaT)

            for file in zone_stat_ras:
                print('Working on {}'.format(file))
                arcpy.AddJoin_management(feature_layer_name, "FID", file, "FID_")

            file_path_csv = os.path.join(self.main_dir, self.subfolder_1)
            print('Exporting csv file!')
            arcpy.TableToTable_conversion(feature_layer_name, file_path_csv, self.csv_filename)
