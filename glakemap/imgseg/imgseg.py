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


class RuleBasedSegmentation(DirMngmt):


    @staticmethod
    def raster2polygon(raster_name, outPolygon):
        field = "VALUE"
        ras2poly = arcpy.RasterToPolygon_conversion(raster_name, outPolygon, "SIMPLIFY", field)
        return ras2poly


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
        

















"""
Backscatter_Threshold = -14
NDWI_Blue_Threshold = 0.5
NDWI_Green_Threshold_M = 0.3
NDWI_Green_Threshold_Low = 0.05 #0.1
Slope_Threshold = 30

Slope_Threshold_2 = 15
Backscatter_Threshold_2 = -14
Local_incidence_Angle = ""
#GL_Output_Name_1='Glacial_Lakes_BHU_V0.tif'
GL_Output_Name_2 = 'Glacial_Lakes_Segmented.tif'

#Import glacier dataset: We use glacier dataset downloaded from GLIMS
from GlacierDataset import GlacierDatasetGLIMS
Glacier_Dataset = GlacierDatasetGLIMS()
print (Glacier_Dataset)

start_time=time.time() #Start time

#User defined modules---------------------------------------------------------------
from MainDirectory import MainDirectory
main_directory=MainDirectory()#.Main_Directory
print(main_directory)
os.listdir(main_directory)

from ReadData import Reading_NDWI_Blue
from ReadData import Reading_NDWI_Green
# from ReadData import Reading_SAR_Data
from ReadData import Reading_SAR_Data
from ReadData import Reading_Slope

# def file_exts(ext1, ext2):
#     f1 = ext1
#     f2 = ext2
#     return f1, f2
# ext1, ext2 = file_exts('_VV_VV_db_COPY.tif', '_VV.tif')

#Coordinate Systems
from SpatialReferenceGCS import Spatial_Reference_GCS
from SpatialReferencePCS import Spatial_Reference_PCS

#Call the function
GCS = Spatial_Reference_GCS()
PCS = Spatial_Reference_PCS()

# Folder_Containing_DT_Results=os.path.join(main_directory,'Decision_Tree_Results')
# if not os.path.exists(Folder_Containing_DT_Results):
#     os.makedirs(Folder_Containing_DT_Results)

#Load operators and Java HashMap
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = jpy.get_type('java.util.HashMap')

#====================================================================================================================
                                                    #CHANGE PARAMETERS
#====================================================================================================================
def Folder_DT():
    Folder_Containing_DT_Results = os.path.join(main_directory,'Rule-Based_Segmentation') #Makes folder as named
    if not os.path.exists(Folder_Containing_DT_Results):
        os.makedirs(Folder_Containing_DT_Results)
    return Folder_Containing_DT_Results
F_2_DT=Folder_DT() # Calling the function
print ('Folder to store Segmented Results is: {}'.format(F_2_DT))

#====================================================================================================================================
                                                # Rule-based segmentation
#====================================================================================================================================
#Call the function
NDWI_Blue = Reading_NDWI_Blue(main_directory)
print(NDWI_Blue)
print(type(NDWI_Blue))
NDWI_Green = Reading_NDWI_Green(main_directory)
print(NDWI_Green)

Radar_Backscatter = Reading_SAR_Data('_VV_VV_db_COPY.tif', '_VV.tif', main_directory)

#Radar_Backscatter=Reading_SAR_Data(main_directory)

print(Radar_Backscatter)

Slope=Reading_Slope(main_directory)
print(Slope)
arcpy.CheckOutExtension("spatial")

print 'Classifying lakes:1,2,3 types...\n'
print '1: Low Turbid Glacial lakes'
print '2: Medium Turbid Glacial lakes'
print '3: High Turbid Glacial lakes'


# Glacial_Lakes=Con((NDWI_Blue>=NDWI_Blue_Threshold),1,Con((NDWI_Green>=NDWI_Green_Threshold_M) & (Radar_Backscatter<=Backscatter_Threshold) & (Slope<=Slope_Threshold),2,\
#                                                          Con((NDWI_Green>=NDWI_Green_Threshold_Low) & (Radar_Backscatter<=Backscatter_Threshold) & (Slope<=Slope_Threshold),3)))

#Glacial_Lakes.save(os.path.join(F_2_DT, GL_Output_Name_1))
#print 'Done! ^_^ \n'
# import progressbar
from time import sleep

def rule_based_segmentation():
    
    Glacial_Lakes_V0 = Con((NDWI_Blue >= NDWI_Blue_Threshold) & (NDWI_Blue <= 0.95), 1,
                        Con((NDWI_Green>=NDWI_Green_Threshold_M) & (Radar_Backscatter<=Backscatter_Threshold), 1,\
                            Con((NDWI_Green>=NDWI_Green_Threshold_Low) & (Radar_Backscatter<=Backscatter_Threshold), 1,
                                Con((Radar_Backscatter<=Backscatter_Threshold_2), 2))))
    
    #Con((Radar_Backscatter<=Backscatter_Threshold_2) & (Slope<=Slope_Threshold_2), 2))))
    arcpy.CheckOutExtension("spatial")
    #Path and file name to be saved
    Save_Con_Result=os.path.join(F_2_DT, GL_Output_Name_2)
    
    Save_Re = Glacial_Lakes_V0.save(Save_Con_Result)
    
    return Save_Re
    #arcpy.SetProgressorPosition()
    #bar.update(Glacial_Lakes_V0)
    #Glacial_Lakes_V0.save(os.path.join(F_2_DT, GL_Output_Name_2))
    #sleep(0.1)
    #print ('Done! ^_^')
Rule_Based_Segmentation()
#arcpy.ResetProgressor()
#CONVERT RASTER TO POLYGON

#Folder to store the conversion results
def FolderToStoreConResult():
    FolderToStoreConResults=os.path.join(main_directory, 'RasterToPolygon') #Makes folder as named
    if not os.path.exists(FolderToStoreConResults):
        os.makedirs(FolderToStoreConResults)
    return FolderToStoreConResults

# F2Store_CR=FolderToStoreConResult()
print('The folder to store R2P result and others are: {}'.format(FolderToStoreConResult()))

# FolderToStoreConResults=os.path.join(MF,'RasterToPolygon') #Makes folder as named
# if not os.path.exists(FolderToStoreConResults):
#     os.makedirs(FolderToStoreConResults)

# Raster to polygon
    
def RasterToPolygon(RasterName): #Takes one input parameter
    field="VALUE"
    outPolygon=os.path.join(FolderToStoreConResult(),'RasterToPolygon.shp')
    # Execute RasterToPolygon
    # arcpy.RasterToPolygon_conversion(RasterName, outPolygon, "SIMPLIFY", field)
    RasToPoly=arcpy.RasterToPolygon_conversion(RasterName, outPolygon, "SIMPLIFY", field)
    # return RasterToPolygon
    return RasToPoly



FileToConvert = os.path.join(F_2_DT, GL_Output_Name_2) #Path to the raster to be converted

print('Converting {} to polygon'.format(FileToConvert))

Ras_To_Poly = RasterToPolygon(FileToConvert) #Calling the function

print(Ras_To_Poly)

#PROJECT SPATIAL DATA FROM ONE COORDINATE SYSTEM TO ANOTHER

#PCS=arcpy.SpatialReference(32645)# UTM coordinate system for areas
#GCS=arcpy.SpatialReference(4326) # Geographic Coordinate System for coordinates (x,y)
#InProject=os.path.join(F2Store_CR,'RasterToPolygon.shp')
OutProjectData = os.path.join(FolderToStoreConResult(), 'RasterToPolygon_TM.shp')



def Project():
    Project_Feature = arcpy.Project_management(Ras_To_Poly, OutProjectData, PCS)
    return Project_Feature



# Call the function
print('Projecting raster to UTM Coordinate')
Trans_Coor = Project()#(InProject)
print(Trans_Coor) 

#ADD GEOMETRY ATTRIBUTES TO A TABLE: Area and X,Y coordinates
 
# Set local variables
#in_features = os.path.join(F2Store_CR,'RasterToPolygon_TM.shp')
properties = "AREA"
length_unit = "KILOMETERS"
area_unit = "SQUARE_KILOMETERS"
coordinate_system = PCS
properties_1 = "CENTROID"
properties_2='PERIMETER_LENGTH'
print('Adding X,Y coordinates to the attribute table...')
arcpy.AddGeometryAttributes_management(Trans_Coor, properties_1, length_unit, area_unit, GCS)
print('Done!')
print('Adding parimeter of a polygon into the attribute table...')
arcpy.AddGeometryAttributes_management(Trans_Coor, properties_2, length_unit, area_unit, coordinate_system)
# Generate the extent coordinates using Add Geometry Properties tool
print('Calculating area and adding area into the attribute table...')
arcpy.AddGeometryAttributes_management(Trans_Coor, properties, length_unit, area_unit, coordinate_system)
#coordinate_system_coord = GCS
DropField='gridcode' #Delete gridcode from the attribute table
print('Deleting gridcode field from the table...')
arcpy.DeleteField_management(Trans_Coor, DropField)



#arcpy.Select_analysis
def SelectFeatureClass():
    select_feature_class = os.path.join(FolderToStoreConResult(), 'RasterToPolygon_Select.shp')
    where_clause = 'POLY_AREA>=0.01' #Select area greter than 0.01 km2
    # Execute Select
    print('Extracting areas larger than 0.01 km2...')
    Select_Feature_Class=arcpy.Select_analysis(Trans_Coor, select_feature_class, where_clause)
    return(Select_Feature_Class)



print ('Extracting Feature Class Complete!')
SelectFeature = SelectFeatureClass() # CALL THE FUNCTION
print (SelectFeature)



def SelectLayerByLocation():
    Distance='WITHIN_A_DISTANCE' 
    Search_Distance='10000 Meters'
    Selection_Type='NEW_SELECTION'
    print('Selecting features within the distacne of 7000 m...')
    arcpy.MakeFeatureLayer_management(SelectFeature, 'select_feature_lyr') #Makes fearure layer
    arcpy.SelectLayerByLocation_management('select_feature_lyr', Distance, Glacier_Dataset, Search_Distance, Selection_Type)
    OutPut_SelectLayerByLocation=os.path.join(FolderToStoreConResult(), 'SelectLayerByLocation_V0.shp')
    Output_Copy_Features = arcpy.CopyFeatures_management('select_feature_lyr', OutPut_SelectLayerByLocation)
    print('Done!')
    return Output_Copy_Features



Copy_Features = SelectLayerByLocation() #CALL THE FUNCTION
print(Copy_Features)
print('Select layer by location complete!')

# def Eliminate_PolygonParts():
#     In_Feauture = Copy_Features
#     Out_Fearure = OutPut_SelectLayerByLocation=os.path.join(F2Store_CR,'SelectLayerByLocation_V2.shp')
#     Condiotion = "AREA"
#     Part_Option = "CONTAINED_ONLY"
#     Eliminate_Parts = arcpy.EliminatePolygonPart_management(In_Feauture, Out_Fearure, Condiotion, 50000, "", Part_Option)
#     return Eliminate_Parts
# Eliminate_Polygon_Parts = Eliminate_PolygonParts()
# Calculate Zonal statistics for Train Data-----------------------------------------------
#import Zonal_Stat_Train #Runs file from Zonal_Stat_Train.py
#-----------------------------------------------------------------------------------------
# Calculate Zonal statistics for Rule-based segmented Data--------------------------------
import Zonal_Stat_App #Runs file from Zonal_Stat_App.py
end_time=time.time()
print ('Time taken for rule-based segmentation is: {} minutes'.format((end_time-start_time)/60))

"""