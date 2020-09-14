"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""


print('Loading modules... ^_^')
import os
import arcpy
from snappy import HashMap
from snappy import GPF
from snappy import ProductIO
from snappy import ProductUtils
arcpy.env.overwriteOutput = True
from arcpy.sa import *
print('Loading module done! ^__^\n')


# Import user defined modules-----------------------

from dirext.dirextmngmt import FileExtMngmt

# Load operators and Java HashMap
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()



class CalculateNDWI(FileExtMngmt):


    @staticmethod
    def read_data(filename):
        return ProductIO.readProduct(filename)


    @staticmethod
    def write_tif(product, filename):
        ProductIO.writeProduct(product, filename, "GeoTIFF")


    
    @staticmethod
    def calculate_ndwi_blue(data, band_names):
        "Calculates Normalized Difference Water Index (NDWI) using blue and near-infrared bands"
        parameters = HashMap()
        parameters.put('greenSourceBand', band_names[1]) # greenSourceBand is Blueband (B2) here!
        parameters.put('nirSourceBand', band_names[7]) # NIR {Blue-NIR/Blue+NIR}
        parameters.put('resampleType', 'Highest resolution') # In case the resolution of the raster does not match
        return GPF.createProduct("Ndwi2Op", parameters,data)
    
                
    
    @staticmethod
    def calculate_ndwi_green(data, band_names):
        "Calculates Normalized Difference Water Index (NDWI) using green and near-infrared bands"
        parameters = HashMap()
        parameters.put('greenSourceBand', band_names[2]) # Green
        parameters.put('nirSourceBand', band_names[7]) # NIR {Green-NIR/Green+NIR}
        parameters.put('resampleType','Highest resolution') # In case the resolution of the raster does not match
        return GPF.createProduct("Ndwi2Op", parameters, data)

    


    def calculate_ndwi(self):   
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for file in f:
                if self.file_extension in file:
                    print('The files are: {}\n'.format((os.path.join(r, file))))
                    file_name = os.path.join(r, file)
                    # Read data
                    print('Reading {} of {}...\n'.format(file, f))
                    # product = read_data(file_name)
                    product = CalculateNDWI.read_data(file_name)
                    # Product properties
                    band_names = product.getBandNames()
                    width = product.getSceneRasterWidth()
                    height = product.getSceneRasterHeight()
                    name = product.getName()
                    description = product.getDescription()
                    
                    print('Product name is:   {}\n'.format(name[-27:-7]))
                    print('Bands:    {}\n'.format(list(band_names)))
                    print('Product    {},{} \n'.format(name, description))
                    print('Raster size:    {} x {} pixels \n'.format(width, height))
                    print('Start time: ' +  str(product.getStartTime()))
                    print('End time: ' +  str(product.getEndTime()))
                    
                    # Path to a directory and make a new folder (File_Name)
                    file_name = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3, name[-27:-7] + '_NDWI_Blue')
                    if not os.path.exists(file_name):
                        os.makedirs(file_name)
                    print('Result directory {}'.format(file_name))
                    output_dir = os.path.join(file_name, name[-27:-7] + '_NDWI_Blue') # Name of the product 
                    # Computes NDWI blue
                    print('Computing NDWI Blue...')
                    ndwi_blue = CalculateNDWI.calculate_ndwi_blue(product, band_names)
                    ProductUtils.copyGeoCoding(product, ndwi_blue)
                    print ('Writing NDWI Blue...')
                    # Write product into a specified directory
                    CalculateNDWI.write_tif(ndwi_blue, output_dir)
                    # Path to a directory and make a new folder (File_Name)
                    file_name = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3, name[-27:-7] + '_NDWI_Green')
                    if not os.path.exists(file_name):
                        os.makedirs(file_name)
                    print('Result directory {}'.format(file_name))
                    output_dir = os.path.join(file_name, name[-27:-7] + '_NDWI_Green') # Name of the product 
                    print('Computing NDWI Green...')
                    ndwi_green = CalculateNDWI.calculate_ndwi_green(product, band_names)
                    ProductUtils.copyGeoCoding(product, ndwi_green)
                    print('Writing NDWI Green...\n')
                    CalculateNDWI.write_tif(ndwi_green, output_dir)




class MosaicNDWIData(FileExtMngmt):

    

    def list_files(self):
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for ext in self.file_extension:
                filters = ext
                for file in f:
                    if file.endswith(filters):
                        files_found = os.path.join(r, file)
                        print("File found: {}".format(files_found))
    


    def mosaic_ndwi(self, gcs):
        self.gcs = gcs

        for ext in self.file_extension:
            filters = ext
            filters_new = "*" + filters
            # Creates a file geodatabase
            geodatabase_file_name = 'NDWI_GDB' + '_' + filters[:-4] + '.gdb'
            print(geodatabase_file_name)
            #Creates a raster dataset with .tif extension
            mosaiced_raster_name = 'NDWI_Mosaiced' + '_' + filters[:-4] + '.tif'
            print(mosaiced_raster_name)

            # 1) Creates a file geodatabase in a folder
            print('Creating Geodatabase file: {} of {} ... ^_^'.format(ext, self.file_extension))
            output_dir = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3)
            # output_dir_serach = os.path.split(output_dir)[0]
            print('Output_directory {}:'.format(output_dir))
            arcpy.CreateFileGDB_management(output_dir, geodatabase_file_name) # Creates gdb file
            print('Done!^_^')

            # 2) Creates an empty mosaic dataset in a file geodatabase
            in_workspace = os.path.join(output_dir, geodatabase_file_name) # Path to the geodatabase
            in_mosaicdataset_name = 'NDWI_RasterDataset' + '_' + filters[:-4]
            NumberOfBand = "1"
            PixelType = "32_BIT_FLOAT" # Pixel type can be changed
            product_definition = "NONE"
            Wavelength = ""
            print('Creating an empty mosaic dataset: {} of {} ... ^_^'.format(ext, self.file_extension))
            arcpy.CreateMosaicDataset_management(in_workspace, in_mosaicdataset_name, self.gcs, NumberOfBand, PixelType, product_definition, Wavelength)
            print('Done!^_^')

            # 3) Add raster dataset to a mosaic dataset from many sources, including a file, folder, raster catalog, table, or web service.
            in_mosaic_dataset = os.path.join(in_workspace, in_mosaicdataset_name)
            print('Adding rasters to an empty mosaic dataset: {} of {} ... ^_^'.format(ext, self.file_extension))
            arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset, "Raster Dataset", output_dir, \
                                                    "UPDATE_CELL_SIZES","UPDATE_BOUNDARY","NO_OVERVIEWS","2","#","#",'#', filters_new, "SUBFOLDERS",\
                                                    "EXCLUDE_DUPLICATES","NO_PYRAMIDS","NO_STATISTICS","NO_THUMBNAILS","#","NO_FORCE_SPATIAL_REFERENCE")
            print('Done! ^_^')
            
            # 4) Creates a folder to copy NDWI mosaiced dataset
            in_raster = os.path.join(in_workspace, in_mosaicdataset_name)
            ndwi = os.path.join(output_dir, 'NDWI_Mosaic' + '_' + filters[:-4])
            if not os.path.exists(ndwi):
                os.makedirs(ndwi)
            print('Copying raster: {} of {} ... ^_^'.format(ext, self.file_extension))
            out_raster = os.path.join(ndwi, mosaiced_raster_name)
            arcpy.CopyRaster_management(in_raster, out_raster,"#","0","0","NONE","NONE","32_BIT_FLOAT","NONE","NONE")
            print('Done! ^_^ ^_^ ^_^')