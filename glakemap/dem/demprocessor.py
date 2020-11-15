"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""
# Load system operators and modules
print('Loading modules... ^_^')
import os
import shutil
import arcpy
arcpy.env.overwriteOutput = True
from arcpy.sa import *
print('Loading module done! ^__^\n')

from glakemap.dirext.dirextmngmt import FileExtMngmt


class MoveDemFiles(FileExtMngmt):

    def move_over(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        for files in os.listdir(self.src_dir):
            if self.zip_extension in files:
                print("DEM file: {}".format(files))
                src = os.path.join(src_dir, files)
                dest = os.path.join(self.main_dir, self.subfolder_1, self.dest_dir, files)
                if not os.path.exists(dest):
                    os.makedirs(dest)
                shutil.move(src, dest)
                print("DEM files moved!")


class DemProcessor(FileExtMngmt):

    def mosaic_dem_cal_slp(self, gdb_name, folder2save_mosaic_ras, mosaiced_dem_ras_name,
                           projection, folder2save_slp_ras, slp_ras_name, z_factor):
        self.gdb_name = gdb_name
        self.folder2save_mosaic_ras = folder2save_mosaic_ras
        self.mosaiced_dem_ras_name = mosaiced_dem_ras_name
        self.projection = projection
        self.folder2save_slp_ras = folder2save_slp_ras
        self.slp_ras_name = slp_ras_name
        self.z_factor = z_factor
        file_path = os.path.join(self.main_dir, self.subfolder_1)
        gdb_file_path = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3)
        print('Creating geodatabase file... ^__^')
        arcpy.CreateFileGDB_management(gdb_file_path, self.gdb_name)
        print('Creating an empty raster dataset inside geodatabse... ^__^')
        mosaic_dataset_name = 'My_RasterDataset'
        mosaicgdb = os.path.join(gdb_file_path, self.gdb_name)
        print("mosaicgdb", mosaicgdb)
        NumberOfBand = "1"
        PixelType = "16_BIT_SIGNED" # Pixel type can be changed
        ProductDefinition = "NONE"
        Wavelength = ""
        arcpy.CreateMosaicDataset_management(mosaicgdb, mosaic_dataset_name, self.projection, NumberOfBand, PixelType, ProductDefinition, Wavelength)
        print('Adding DEM rasters into an empty raster dataset... ^__^')
        path_and_nameof_mosaic_dataset = os.path.join(mosaicgdb, mosaic_dataset_name)
        arcpy.AddRastersToMosaicDataset_management(path_and_nameof_mosaic_dataset, "Raster Dataset",
                                                file_path, "UPDATE_CELL_SIZES","UPDATE_BOUNDARY","NO_OVERVIEWS","2","#","#",
                                                self.projection, '*'+self.file_extension, "SUBFOLDERS","EXCLUDE_DUPLICATES","NO_PYRAMIDS","NO_STATISTICS",
                                                "NO_THUMBNAILS","#","FORCE_SPATIAL_REFERENCE")
        in_raster = os.path.join(mosaicgdb, mosaic_dataset_name)
        create_folder = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3, self.folder2save_mosaic_ras)
        if not os.path.exists(create_folder):
            os.makedirs(create_folder)
        out_raster = os.path.join(create_folder, self.mosaiced_dem_ras_name)
        arcpy.CopyRaster_management(in_raster, out_raster, "#","#","#","NONE","NONE","16_BIT_UNSIGNED","NONE","NONE")

        def slope_cal():
            print('Reading DEM! ^_^')
            read_dem = arcpy.Raster(out_raster)
            print('Caculating slope... ^__^')
            arcpy.CheckOutExtension("spatial")
            slope_raster = Slope(read_dem, "DEGREE", self.z_factor)
            arcpy.CheckInExtension("spatial")
            slope_cal_path = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3, self.folder2save_slp_ras)
            if not os.path.exists(slope_cal_path):
                os.makedirs(slope_cal_path)
            slope_file = os.path.join(slope_cal_path, self.slp_ras_name)
            print('Writing slope raster... ^__^')
            slope_raster.save(slope_file)
            print('Done! ^__^')
            print('Resampling Slope raster...')
            arcpy.CheckOutExtension("spatial")
            in_ras_resample = arcpy.Raster(slope_file)
            resampled_slope_file = os.path.join(slope_cal_path, 'Resam_' + self.slp_ras_name)
            arcpy.Resample_management(in_ras_resample, resampled_slope_file, "8.9831528e-05", "BILINEAR")
            arcpy.CheckInExtension("spatial")
            print('Done! ^__^')
        slope_cal()