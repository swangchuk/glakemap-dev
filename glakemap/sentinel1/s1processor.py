"""
Created on Fri Mar 01 06:32:59 2019
@author: Sonam Wangchuk
Email:sonam.wangchuk@geo.uzh.ch
"""


print ('Loading modules... ^_^')
import os
import zipfile
from snappy import HashMap
from snappy import GPF
from snappy import ProductIO
import arcpy
from arcpy.sa import *
arcpy.env.overwriteOutput = True
print('Loading module done! ^__^\n')


# Import user defined modules-----------------------------------------------
from dirext.maindir import main_directory
from dirext.dirextmngmt import FileExtMngmt


main_directory = main_directory()

# Load operators and Java HashMap
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
# HashMap = jpy.get_type('java.util.HashMap')


def rio():

    """Returns region of interest"""
    
    gcs = "POLYGON((88.761 27.242, 90.761 27.242, 90.761 28.687, 88.712 28.687, 88.761 27.242))"

    return gcs



class SARDataOperators:


    @staticmethod
    def band_pol(band_polarisation):

        """Provide single or double polarization type in list format"""

        return band_polarisation
     
    
    @staticmethod
    def read_data(data):
        return ProductIO.readProduct(data)
    
    
    @staticmethod
    def orbit_correction(orbcor):
        parameters = HashMap()
        parameters.put('continueOnFail', True)
        parameters.put('orbitType','Sentinel Precise (Auto Download)')
        parameters.put('polyDegree', '3')
        return GPF.createProduct('Apply-Orbit-File', parameters, orbcor)
    
    
    @staticmethod
    def data_calibration(calib):
        parameters = HashMap()
        parameters.put('auxFile', 'Latest Auxiliary File')
        parameters.put('outputSigmaBand', False)
        parameters.put('createBetaBand', True)
        parameters.put('outputBetaBand', True)
        parameters.put('selectedPolarisations', polarization)
        #parameters.put('sourceBands', 'Intensity_' + polarization)
        parameters.put('sourceBands', band_names) # Or 'Intensity_VV', 'Intensity_VH'
        return GPF.createProduct('Calibration', parameters, calib)
    
    
    @staticmethod
    def speckle_filter(spkl):
        parameters = HashMap()
        parameters.put('filter','Refined Lee')
        return GPF.createProduct('Speckle-Filter', parameters, spkl)

    
    @staticmethod
    def terrain_flattening (terflt):
        parameters = HashMap()
        parameters.put('demName','SRTM 1Sec HGT')
        parameters.put('demResamplingMethod', 'BICUBIC_INTERPOLATION')
        parameters.put('reGridMethod', True)
        parameters.put('sourceBands', 'Beta0_' + polarization)
        return GPF.createProduct('Terrain-Flattening', parameters, terflt)

    

    @staticmethod
    def terrain_correction(tercorr):
        parameters = HashMap()
        parameters.put('auxFile', 'Latest Auxiliary File')
        parameters.put('demName','SRTM 1Sec HGT')
        parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
        #parameters.put('mapProjection',PCS)
        #parameters.put('PixelSpacingInDegree', '0')
        #parameters.put('saveLatLon', False)
        #parameters.put('saveLocalIncidenceAngle', True)
        #parameters.put('saveProjectedLocalIncidenceAngle', True)
        parameters.put('saveSelectedSourceBand', True)
        parameters.put('sourceBands', 'Beta0_' + polarization)
        return GPF.createProduct('Terrain-Correction', parameters, tercorr)

    

    @staticmethod
    def scaling_dB(scldB):
        parameters = HashMap()
        parameters.put('sourceBands','Beta0_'+ polarization)
        return GPF.createProduct('LinearToFromdB', parameters, scldB)
    
    
    @staticmethod
    def write_data(wrtdta, filename):
        return ProductIO.writeProduct(wrtdta, filename, 'BEAM-DIMAP' ) #'GeoTIFF'




class ProcessSARData(FileExtMngmt):

    
    def process_sar_data(self):
        
        """Read files containing '.safe' extension and process the data"""
        
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for file in f:
                if self.file_extension in file:
                    print ('The files containing .safe extension are: {} \n'.format((os.path.join(r, file))))
                    #file_name = os.path.join(r, file)
                    file_name = os.path.join(r, file)
                    # Read data
                    print('Reading...\n')
                    
                    sar_data = SARDataOperators()
                    
                    product = sar_data.read_data(file_name)
                    # Product properties
                    global  band_names 
                    band_names = product.getBandNames()
                
                    print('Band type: {}'.format(band_names))
                    width = product.getSceneRasterWidth()
                    height = product.getSceneRasterHeight()
                    global name # Global Name
                    name = product.getName()
                    print("Band name: {}".format(name[:25]))
                    description = product.getDescription()

                    print('Bands:    {}\n'.format(list(band_names)))
                    print('Product    {},{} \n'.format(name, description))
                    print('Raster size:    {} x {} pixels \n'.format(width, height))
                    print('Start time: {}\n'.format(str(product.getStartTime())))
                    print('End time: {}\n'.format(str(product.getEndTime())))

                    
                    def data_polarization(band_polarisation):
                        print('Processing {} of {}'.format(p, sar_data.band_pol(band_polarisation)))
                        # Call the functions
                        # Orbit Correction
                        print('Correcting orbit {} of {}'.format(p, sar_data.band_pol(band_polarisation)))
                        orbit_corr = sar_data.orbit_correction(product)

                        # Subset Data
                        # print('Subsetting {} of {}:'.format(p, polarization))
                        # subset = subset_data(orbit_corr)

                        # Caibration
                        print('Calibrating {} of {}:'.format(p, sar_data.band_pol(band_polarisation)))
                        # calib = data_calibration(subset)
                        calib = sar_data.data_calibration(orbit_corr)

                        # Speckle-Filter
                        print('Speckle filtering {} of {}:'.format(p, sar_data.band_pol(band_polarisation)))
                        spec_filter = sar_data.speckle_filter(calib)

                        # TC
                        terrain_corr = sar_data.terrain_correction(spec_filter)

                        # Scaling
                        dB = sar_data.scaling_dB(terrain_corr)

                        # Output dB
                        output_dir = os.path.join(self.main_dir, self.subfolder_1,
                                                self.subfolder_3, name[:32] + '_' + polarization + '_dB')
                        
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                            
                        print('The folder containing output result is {}'.format (output_dir))
                        output_filename = os.path.join(output_dir, name[:32] + '_' + polarization + '_TC' + '.dim')
                        print('Writing file named {} of {}...'.format(name[:32], polarization))
                        sar_data.write_data(dB, output_filename)
                        print('Processing done!')
                        
                    for p in sar_data.band_pol(self.polarisation):
                        global  polarization
                        polarization = p
                        if len(sar_data.band_pol(self.polarisation))==1:
                            data_polarization(self.polarisation)
                        else:
                            data_polarization(self.polarisation)



class Reprojections(FileExtMngmt):

    """Addeed projection functionality"""

    def __init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3, zip_extension, file_extension, polarisation, projection):
        # super().__init__(main_dir, subfolder_1, subfolder_2, subfolder_3) # Python >3
        # DirMngmt.__init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3)
        super(Reprojections, self).__init__(main_dir, subfolder_1, subfolder_2, subfolder_3, zip_extension, file_extension, polarisation)
        self.projection = projection



    def reprojection(self):
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for file in f:
                for pol in self.polarisation:
                    if pol in file:

                        def reproject():

                            # Reading Basename folder
                            basename_folder = os.path.basename(r)
                            print('The basename file is: {}'.format(basename_folder[0:35]))
                            
                            # Read data             
                            data_dB = os.path.join(r, file)
                            print('The files are: {}'.format(data_dB))

                            if data_dB.endswith('ovr'):
                                os.remove(data_dB)
                                print('Files deleted!')
                            else:
                                print('File does not exist!')
                            
                            print('Reading {} of {} for {}'.format(pol, self.polarisation, basename_folder[0:35])) 
                            data_read = arcpy.Raster(data_dB)
                            print('Reading Done!')

                            output_directory = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3, basename_folder[0:35] + '_Orthorectified')
                            
                            if not os.path.exists(output_directory):
                                os.makedirs(output_directory)

                            output_directory_proj = os.path.join(output_directory, basename_folder[0:35] + '_Proj' )
                            
                            if not os.path.exists(output_directory_proj):
                                os.makedirs(output_directory_proj)

                            output_directory_copy=os.path.join(output_directory, basename_folder[0:35] + '_Copy' )
                            
                            if not os.path.exists(output_directory_copy):
                                os.makedirs(output_directory_copy)


                            projected_raster_name = basename_folder[0:35] + pol[0:6] + '_PROJ' + '.tif'
                            copied_raster_name = basename_folder[0:35] +  pol[0:6]+ '_COPY' + '.tif'


                            
                            def set_null(sar_data):
                                whereClause = "VALUE<-35" #whereClause="VALUE<-26"
                                outSetNull = SetNull(sar_data, sar_data, whereClause)
                                return outSetNull
                            

                            
                            def project_raster(path, null_raster):
                                #in_Raster=os.path.join(Path,Copied_Raster_Name)
                                #Read_Project_Raster=arcpy.Raster(in_Raster)
                                out_projected_raster = os.path.join(path, projected_raster_name)
                                arcpy.ProjectRaster_management(null_raster, out_projected_raster, self.projection, "BILINEAR","#","#","#","#")
                                return out_projected_raster


                            
                            def copy_raster(path, projected_raster):

                                """Sets Background zero background values to No Data"""

                                out_raster = os.path.join(path, copied_raster_name)
                                arcpy.CopyRaster_management(projected_raster, out_raster, "#","0","0","NONE","NONE","32_BIT_FLOAT","NONE","NONE")
                                return out_raster


                            arcpy.CheckOutExtension("spatial")
                            print('Setting {} of {} to NoData for values <-26'.format(pol, self.polarisation))
                            set_null_raster = set_null(data_read)
                            print('Done! ^_^ ^_^ ^_^')

                            print('Projecting {} of {}'.format(pol, self.polarisation))
                            project_raster_data = project_raster(output_directory_proj, set_null_raster)
                            arcpy.CheckInExtension("spatial")
                            print('Done! ^_^ ^_^ ^_^')

                            print('Setting {} of {} (background values) to NoData'.format(pol, self.polarisation))
                            copy_raster(output_directory_copy, project_raster_data)
                            print('Done! ^_^ ^_^ ^_^')
                    

                        if len(self.polarisation)==1:
                            reproject()
                        else:
                            reproject()



class MosaicDataMethods(Reprojections):


    @staticmethod
    def gdb(path, gdb_name):

        """Creates an empty geodatabase file"""

        geo_database = arcpy.CreateFileGDB_management(path, gdb_name)
        return geo_database


    def empty_mosaic_dataset(self, in_workspace, in_mosaicdataset_name):

        """Creates an empty mosaic dataset (emd)"""

        self.in_workspace = in_workspace
        self.in_mosaicdataset_name = in_mosaicdataset_name

        NumberOfBand = "1"
        PixelType = "32_BIT_FLOAT" # Pixel type can be changed
        product_definition = "NONE"
        Wavelength = ""
        md = arcpy.CreateMosaicDataset_management(self.in_workspace, self.in_mosaicdataset_name,
        self.projection, NumberOfBand, PixelType,product_definition, Wavelength)
        return md


    @staticmethod
    def add_raster_emd(in_mosaic_dataset, input_path):

        """Add rasters to an empty mosaic dataset"""

        Raster_Type = "Raster Dataset"
        Update_CellSize = "UPDATE_CELL_SIZES"
        Update_Boundary = "UPDATE_BOUNDARY"
        Update_Overview = "NO_OVERVIEWS"
        add_raster = arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset, Raster_Type, input_path,\
                                                Update_CellSize, Update_Boundary, Update_Overview, "2","#","#",'#', filter_ext, "SUBFOLDERS",\
                                                "EXCLUDE_DUPLICATES","NO_PYRAMIDS","NO_STATISTICS","NO_THUMBNAILS","#","NO_FORCE_SPATIAL_REFERENCE")
        return add_raster


    @staticmethod
    def copy_raster(rasterTocopy, out_raster):
        copy_ras = arcpy.CopyRaster_management(rasterTocopy, out_raster,"#","0","0","NONE","NONE","32_BIT_FLOAT","NONE","NONE")
        return copy_ras
        


class MosaicDatastet(Reprojections):



    def mosaic(self):
        import fnmatch
        for fil in self.polarisation:
            global filter_ext
            filter_ext = fil
            for root, dirs, files in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
                for filename in fnmatch.filter(files, filter_ext):
                    files = os.path.join(root, filename)
                    head, tail = os.path.split(files)
                    print("Working on {} of {}".format(filter_ext, self.polarisation))
                    mdm = MosaicDataMethods(self.main_dir, self.subfolder_1, self.subfolder_2,
                    self.subfolder_3, self.zip_extension, self.file_extension, self.polarisation, self.projection)
                    # gdb_file = mdm.makefolders()
                    gdb_file = os.path.join(self.main_dir, self.subfolder_1, self.subfolder_3)
                    print('Creating geodatabse! ^_^')
                    create_gdb = mdm.gdb(gdb_file, tail[:11] + filter_ext[1:4] + '.gdb')
                    print('Creating empty mosaic dataset file! ^_^')
                    cemd = mdm.empty_mosaic_dataset(create_gdb, tail[:11] + filter_ext[1:4])
                    add_raster = mdm.add_raster_emd(cemd, gdb_file)
                    print('Adding rasters to empty mosaic dataset done! ^_^')
                    out_raster_folder = os.path.join(gdb_file, tail[:11] + filter_ext[1:4])
                    if not os.path.exists(out_raster_folder):
                        os.makedirs(out_raster_folder)
                    out_raster = os.path.join(out_raster_folder, tail[:11] + filter_ext[1:4] + '.tif')
                    print('Coying Raster...')
                    mdm.copy_raster(add_raster, out_raster)
                    print('Copying raster dataset done! ^_^')