import arcpy


class SpatialReference():


    def gcs(self, gcs_code):


        """Returns geographic coordinate system"""
        
        
        self.gcs_code = gcs_code
        gcs = arcpy.SpatialReference(self.gcs_code) # 4326
        return gcs



    def pcs(self, pcs_code):
        

        """Returns projected coordinate system"""


        self.pcs_code = pcs_code
        pcs = arcpy.SpatialReference(self.pcs_code)
        return pcs