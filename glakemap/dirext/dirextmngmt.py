import os
import zipfile



class DirMngmt(object):

    """1) Creates folders and unzip files containing zip extension 2) Read
    '.safe' file and process SAR data """
    
    def __init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3):
        
        """Note: Give 'subfolder_1' name and folder containing 
        SAR data the same name. Otherwise '.zip' cannot be located """
        
        self.main_dir = main_dir
        self.subfolder_1 = subfolder_1
        self.subfolder_2 = subfolder_2
        self.subfolder_3 = subfolder_3



    def main_directory(self):

        return self.main_dir



    def makefolders(self):

        """ Create folders"""
        

        folder_1 = os.path.join(self.main_dir, self.subfolder_1)
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)

        folder_2 = os.path.join(folder_1, self.subfolder_2)
        if not os.path.exists(folder_2):
            os.makedirs(folder_2)

        folder_3 = os.path.join(folder_1, self.subfolder_3)
        if not os.path.exists(folder_3):
            os.makedirs(folder_3)



class FileExtMngmt(DirMngmt):


    def __init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3, zip_extension, file_extension, polarisation):
        # super().__init__(main_dir, subfolder_1, subfolder_2, subfolder_3) # Python >3
        # DirMngmt.__init__(self, main_dir, subfolder_1, subfolder_2, subfolder_3)
        super(FileExtMngmt, self).__init__(main_dir, subfolder_1, subfolder_2, subfolder_3) # only python 2
        self.zip_extension = zip_extension
        self.file_extension = file_extension
        self.polarisation = polarisation



    def unzipfiles(self):
        
        """Unzip files containing '.zip' extension """
        
        for r, d, f in os.walk(os.path.join(self.main_dir, self.subfolder_1)):
            for file in f:
                if self.zip_extension in file:
                    print ('The files containing .ZIP extension are: {} \n'.format((os.path.join(r, file))))
                    file_name = os.path.join(r, file)
                    zip_ref = zipfile.ZipFile(file_name)
                    print ('The number of zip files: {}'.format(len(f)))
                    print ('Extracting {} of {} \n'.format(file, f))
                    zip_ref.extractall(os.path.join(self.main_dir, self.subfolder_1, self.subfolder_2))
                    print ('Extractring files completed!\n')
                    zip_ref.close()