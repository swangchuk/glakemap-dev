

import os
import arcpy
arcpy.env.overwriteOutput = True

from glakemap.dirext.dirextmngmt import DirMngmt



class ReadData(DirMngmt):

    
    @staticmethod
    def read_post_process_data(main_dir, file_extension):

        for r, d, f in os.walk(main_dir):
            for file in f:
                if file.endswith(file_extension):
                    data_loc = os.path.join(r, file)
                    print('Model location; {}'.format(data_loc))
        return data_loc




class PostProcessing():


    @staticmethod
    def post_process(shp_file_path, csv_file_path, out_shp_filename, csv_filename):
        # Create a feature layer from the featureclass
        arcpy.MakeFeatureLayer_management(shp_file_path, 'Path_Polygon_Layer')
        # Join Shapefle table and predicted csv file with FID
        arcpy.AddJoin_management('Path_Polygon_Layer', "Id", csv_file_path, "Id")
        # Select polygons with label=1
        where_clause = "Label=1"
        arcpy.SelectLayerByAttribute_management('Path_Polygon_Layer', "NEW_SELECTION", where_clause)
        # Path for the result
        out_feature_dir = os.path.split(shp_file_path)[0]
        # Feature result name
        out_feature = os.path.join(out_feature_dir, out_shp_filename)
        # Copy the the selected features i.e polygons with label=1
        copy_feature = arcpy.CopyFeatures_management('Path_Polygon_Layer', out_feature)
        arcpy.TableToTable_conversion(copy_feature, out_feature_dir, csv_filename)