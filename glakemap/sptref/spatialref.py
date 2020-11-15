import arcpy


class SpatialReference():
    
    @staticmethod
    def gcs(gcs_code):
        
        """Returns geographic coordinate system"""
        gcs = arcpy.SpatialReference(gcs_code) # 4326
        return gcs

    @staticmethod
    def pcs(pcs_code):
        
        """Returns projected coordinate system"""
        pcs = arcpy.SpatialReference(pcs_code)
        return pcs