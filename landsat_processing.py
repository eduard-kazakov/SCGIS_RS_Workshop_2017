# -*- coding: utf-8 -*-
from metadata_reader import LandsatMetadata
from osgeo import gdal
import numpy as np
import math

class LandsatProcessor ():
    metadata = None
    dos_required = False

    def __init__(self,metadata_file,landsat_version,dos_required=False):
        self.metadata = LandsatMetadata(metadata_file,landsat_version)
        self.dos_required = dos_required
    
    def get_red_radiance_as_array (self):
        red_dn = gdal.Open(self.metadata.red_channel_path)
        red_dn_array = np.array(red_dn.GetRasterBand(1).ReadAsArray().astype(np.float16))
        red_dn_array[red_dn_array==0]=[np.nan]
        print 'calculating red channel radiance...'
        red_radiance_array = self.metadata.red_channel_mult * red_dn_array + self.metadata.red_channel_add
        return red_radiance_array
        
    def get_nir_radiance_as_array (self):        
        nir_dn = gdal.Open(self.metadata.nir_channel_path)
        nir_dn_array = np.array(nir_dn.GetRasterBand(1).ReadAsArray().astype(np.float16))
        nir_dn_array[nir_dn_array==0]=[np.nan]
        print 'calculating NIR channel radiance...'
        nir_radiance_array = self.metadata.nir_channel_mult * nir_dn_array + self.metadata.nir_channel_add
        return nir_radiance_array
        
    def get_red_reflectance_as_array (self):
        red_radiance = self.get_red_radiance_as_array()
        print 'calculating red channel reflectance...'
        
        if self.dos_required:
            print 'applying DOS atmospheric correction for red reflectance...'
            min_red_radiance = np.nanmin(red_radiance)

            red_1_perc = (0.01 * (math.cos(self.metadata.sun_zenith)**3) * self.metadata.red_channel_solar_irradiance) / (math.pi * (self.metadata.earth_sun_distance**2) )
            red_haze_radiance = min_red_radiance - red_1_perc
            red_reflectance = (math.pi * (red_radiance - red_haze_radiance) * (self.metadata.earth_sun_distance**2))/(self.metadata.red_channel_solar_irradiance * math.sin(self.metadata.sun_elevation))
        else:    
            red_reflectance = (math.pi * red_radiance * (self.metadata.earth_sun_distance**2))/(self.metadata.red_channel_solar_irradiance * math.sin(self.metadata.sun_elevation))
        
        return red_reflectance

    def get_nir_reflectance_as_array (self):
        nir_radiance = self.get_nir_radiance_as_array()
        print 'calculating NIR channel reflectance...'
        
        if self.dos_required:
            print 'applying DOS atmospheric correction for NIR reflectance...'
            min_nir_radiance = np.nanmin(nir_radiance)

            nir_1_perc = (0.01 * (math.cos(self.metadata.sun_zenith)**3) * self.metadata.nir_channel_solar_irradiance) / (math.pi * (self.metadata.earth_sun_distance**2) )
            nir_haze_radiance = min_nir_radiance - nir_1_perc
            nir_reflectance = (math.pi * (nir_radiance - nir_haze_radiance) * (self.metadata.earth_sun_distance**2))/(self.metadata.nir_channel_solar_irradiance * math.sin(self.metadata.sun_elevation))
        else:    
            nir_reflectance = (math.pi * nir_radiance * (self.metadata.earth_sun_distance**2))/(self.metadata.nir_channel_solar_irradiance * math.sin(self.metadata.sun_elevation))
        
        return nir_reflectance
 
    def get_ndvi_as_array (self):
        red_reflectance = self.get_red_reflectance_as_array()
        nir_reflectance = self.get_nir_reflectance_as_array()
        print 'calculating NDVI...'
        ndvi = (nir_reflectance - red_reflectance) / (nir_reflectance + red_reflectance)
        return ndvi
        
    def get_emissivity_from_ndvi_as_array (self):
        def convert_ndvi_to_lse (ndvi_value):
            if ndvi_value > 0.727:
                return 0.990
            elif (ndvi_value >= 0.157) and (ndvi_value <= 0.727):
                return 1.0094 + 0.047*math.log(ndvi_value)
            elif (ndvi_value >= -0.185) and (ndvi_value < 0.157):
                return 0.970
            else:
                return 0.995

        
        np_convert_ndvi_to_lse = np.vectorize(convert_ndvi_to_lse)
                
        ndvi = self.get_ndvi_as_array()
        print 'calculating land surface emissivity...'
        lse = np_convert_ndvi_to_lse(ndvi)
        
        return lse
        
        
    def get_thermal_radiance_as_array (self):
        thermal_dn = gdal.Open(self.metadata.thermal_channel_path)
        thermal_dn_array = np.array(thermal_dn.GetRasterBand(1).ReadAsArray().astype(np.int16))
        print 'calculating thermal channel radiance...'
        thermal_radiance_array = self.metadata.thermal_channel_mult * thermal_dn_array + self.metadata.thermal_channel_add
        return thermal_radiance_array
        
    def get_brightness_temperature_as_array (self):
        thermal_radiance = self.get_thermal_radiance_as_array()
        print 'calculating brightness temperature...'
        brightness_temperature = (self.metadata.thermal_k2 / np.log(self.metadata.thermal_k1 / thermal_radiance + 1))
        return brightness_temperature
    
    def save_array_as_geotiff (self, input_array, output_path, is_thermal = False):
        print 'writing file ' + str(output_path) + '...'
        if not is_thermal:
            base_raster = gdal.Open(self.metadata.red_channel_path)
        else:
            base_raster = gdal.Open(self.metadata.thermal_channel_path)
            
        cols = base_raster.RasterXSize
        rows = base_raster.RasterYSize
        bands = 1
        cell_type = gdal.GDT_Float32
        driver_name = 'GTiff'
        driver = gdal.GetDriverByName(driver_name)
        projection = base_raster.GetProjection()
        transform = base_raster.GetGeoTransform()
        
        out_data = driver.Create(output_path,cols,rows,bands,cell_type)
        out_data.SetProjection (projection)
        out_data.SetGeoTransform (transform)

        out_data.GetRasterBand(1).WriteArray (input_array)
        
        
    def get_surface_temperature_simplified_model (self):
        p = 14380 # from planck, boltzman and light velocity
        def calculate_lst_simple (brightness_temperature, lse, wavelength):    
            return ( brightness_temperature / ( 1 + ((wavelength * brightness_temperature / p) * math.log(lse)) ) ) - 273.15
        
        np_calculate_lst_simple = np.vectorize(calculate_lst_simple)
            
        lse = self.get_emissivity_from_ndvi_as_array()
        brightness_temperature = self.get_brightness_temperature_as_array()
        wavelength = self.metadata.thermal_wavelength
        print 'calculating land surface temperature (simplified model [Weng, et al. 2004])...'
        
        lst = np_calculate_lst_simple(brightness_temperature,lse, wavelength)
        return lst
        
data_source = LandsatProcessor('E:/dzz_mag/bolivia/LC82310722016225LGN00/LC82310722016225LGN00_MTL.txt','Landsat_8', dos_required=False)
#red_rad = data_source.get_nir_reflectance_as_array()
#br_temp = data_source.get_brightness_temperature()
#ndvi = data_source.get_ndvi_as_array()
#data_source.save_array_as_geotiff(ndvi,'E:/ndvi.tif')
#nir_rad = data_source.get_nir_radiance_as_array()
#red_rad = data_source.get_red_radiance_as_array()
#nir = data_source.get_nir_reflectance_as_array()
#red = data_source.get_red_reflectance_as_array()
#data_source.save_array_as_geotiff(nir,'E:/lst/nir_dos2.tif')
#data_source.save_array_as_geotiff(red,'E:/lst/red_dos2.tif')
lst = data_source.get_surface_temperature_simplified_model()
data_source.save_array_as_geotiff(lst,'E:/lst/lst8_test.tif')
#data_source.save_array_as_geotiff(nir_rad,'E:/lst/nir_rad.tif')
#data_source.save_array_as_geotiff(red_rad,'E:/lst/red_rad.tif')

#lst = data_source.get_surface_temperature_simplified_model()
#data_source.save_array_as_geotiff(lst,'E:/lst_l7_NODOS_1.tif')