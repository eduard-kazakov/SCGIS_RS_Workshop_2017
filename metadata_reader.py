# -*- coding: utf-8 -*-

from datetime import datetime
import math
import os.path

class LandsatMetadata:
    supported_landsat_versions = ['Landsat_4','Landsat_5','Landsat_7','Landsat_8']

    ########################################
    ############## LANDSAT 8 ###############
    ########################################
    
    landsat_8_dict = {'acquisition_date':'DATE_ACQUIRED',
                      'acquisition_time':'SCENE_CENTER_TIME',
                      
                      'red_channel_path':'FILE_NAME_BAND_4',
                      'nir_channel_path':'FILE_NAME_BAND_5',
                      'thermal_channel_path':'FILE_NAME_BAND_11',
                      'pan_channel_path':'FILE_NAME_BAND_8',
                      
                      'red_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_4',
                      'red_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_4',
                      'nir_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_5',
                      'nir_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_5',
                      'pan_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_8',
                      'pan_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_8',
                      
                      'thermal_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_11',
                      'thermal_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_11',
                      
                      
                      
                      'red_channel_min_rad':'RADIANCE_MINIMUM_BAND_4',
                      'red_channel_max_rad':'RADIANCE_MAXIMUM_BAND_4',
                      'nir_channel_min_rad':'RADIANCE_MINIMUM_BAND_5',
                      'nir_channel_max_rad':'RADIANCE_MAXIMUM_BAND_5',
                      'pan_channel_min_rad':'RADIANCE_MINIMUM_BAND_8',
                      'pan_channel_max_rad':'RADIANCE_MAXIMUM_BAND_8',
                      'thermal_channel_min_rad':'RADIANCE_MINIMUM_BAND_11',
                      'thermal_channel_max_rad':'RADIANCE_MAXIMUM_BAND_11',
                      
                      'red_channel_min_refl': 'REFLECTANCE_MAXIMUM_BAND_4',
                      'nir_channel_min_refl': 'REFLECTANCE_MAXIMUM_BAND_5',
                      
                      'red_channel_mult':'RADIANCE_MULT_BAND_4',
                      'red_channel_add':'RADIANCE_ADD_BAND_4',
                      'nir_channel_mult':'RADIANCE_MULT_BAND_5',
                      'nir_channel_add':'RADIANCE_ADD_BAND_5',
                      'pan_channel_mult':'RADIANCE_MULT_BAND_8',
                      'pan_channel_add':'RADIANCE_ADD_BAND_8',
                      
                      'thermal_channel_mult':'RADIANCE_MULT_BAND_11',
                      'thermal_channel_add':'RADIANCE_ADD_BAND_11',
                      
                      'thermal_wavelength': 12,
                      
                      'thermal_k1':'K1_CONSTANT_BAND_11',
                      'thermal_k2':'K2_CONSTANT_BAND_11',
                      
                      'red_channel_solar_irradiance': 0,
                      'nir_channel_solar_irradiance': 0,
                      
                      'earth_sun_distance':'EARTH_SUN_DISTANCE',
                      'sun_elevation':'SUN_ELEVATION',
                      'sun_azimuth':'SUN_AZIMUTH'
                      }
                      
    ########################################
    ############## LANDSAT 7 ###############
    ########################################
    
    landsat_7_dict = {'acquisition_date':'DATE_ACQUIRED',
                      'acquisition_time':'SCENE_CENTER_TIME',
                      
                      'red_channel_path':'FILE_NAME_BAND_3',
                      'nir_channel_path':'FILE_NAME_BAND_4',
                      'thermal_channel_path':'FILE_NAME_BAND_6_VCID_1',
                      
                      'red_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_3',
                      'red_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_3',
                      'nir_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_4',
                      'nir_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_4',
                      'thermal_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_6_VCID_1',
                      'thermal_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_6_VCID_1',
                      
                      'red_channel_min_rad':'RADIANCE_MINIMUM_BAND_3',
                      'red_channel_max_rad':'RADIANCE_MAXIMUM_BAND_3',
                      'nir_channel_min_rad':'RADIANCE_MINIMUM_BAND_4',
                      'nir_channel_max_rad':'RADIANCE_MAXIMUM_BAND_4',
                      'thermal_channel_min_rad':'RADIANCE_MINIMUM_BAND_6_VCID_1',
                      'thermal_channel_max_rad':'RADIANCE_MAXIMUM_BAND_6_VCID_1',
                      
                      'red_channel_mult':'RADIANCE_MULT_BAND_3',
                      'red_channel_add':'RADIANCE_ADD_BAND_3',
                      'nir_channel_mult':'RADIANCE_MULT_BAND_4',
                      'nir_channel_add':'RADIANCE_ADD_BAND_4',
                      'thermal_channel_mult':'RADIANCE_MULT_BAND_6_VCID_1',
                      'thermal_channel_add':'RADIANCE_ADD_BAND_6_VCID_1',
                      
                      'thermal_wavelength': 11.45,
                      
                      'thermal_k1':666.09,
                      'thermal_k2':1282.71,
                      
                      'red_channel_solar_irradiance': 1547,
                      'nir_channel_solar_irradiance': 1044,
                      
                      
                      'earth_sun_distance':None,
                      'sun_elevation':'SUN_ELEVATION',
                      'sun_azimuth':'SUN_AZIMUTH'
                      }
                      
    ########################################
    ############## LANDSAT 4-5 TM ##########
    ########################################
    
    landsat_4_dict = {'acquisition_date':'DATE_ACQUIRED',
                       'acquisition_time':'SCENE_CENTER_TIME',
                      
                       'red_channel_path':'FILE_NAME_BAND_3',
                       'nir_channel_path':'FILE_NAME_BAND_4',
                       'thermal_channel_path':'FILE_NAME_BAND_6',
                      
                       'red_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_3',
                       'red_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_3',
                       'nir_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_4',
                       'nir_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_4',
                       'thermal_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_6',
                       'thermal_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_6',
                      
                       'red_channel_min_rad':'RADIANCE_MINIMUM_BAND_3',
                       'red_channel_max_rad':'RADIANCE_MAXIMUM_BAND_3',
                       'nir_channel_min_rad':'RADIANCE_MINIMUM_BAND_4',
                       'nir_channel_max_rad':'RADIANCE_MAXIMUM_BAND_4',
                       'thermal_channel_min_rad':'RADIANCE_MINIMUM_BAND_6',
                       'thermal_channel_max_rad':'RADIANCE_MAXIMUM_BAND_6',
                      
                       'red_channel_mult':'RADIANCE_MULT_BAND_3',
                       'red_channel_add':'RADIANCE_ADD_BAND_3',
                       'nir_channel_mult':'RADIANCE_MULT_BAND_4',
                       'nir_channel_add':'RADIANCE_ADD_BAND_4',
                       'thermal_channel_mult':'RADIANCE_MULT_BAND_6',
                       'thermal_channel_add':'RADIANCE_ADD_BAND_6',
                       
                       'thermal_wavelength': 11.45,
                       
                       'thermal_k1':671.62,
                       'thermal_k2':1284.30,
                       
                       'red_channel_solar_irradiance': 1557,
                       'nir_channel_solar_irradiance': 1033,
                      
                       'earth_sun_distance':None,
                       'sun_elevation':'SUN_ELEVATION',
                       'sun_azimuth':'SUN_AZIMUTH'
                      }
                      
    landsat_5_dict = {'acquisition_date':'DATE_ACQUIRED',
                       'acquisition_time':'SCENE_CENTER_TIME',
                      
                       'red_channel_path':'FILE_NAME_BAND_3',
                       'nir_channel_path':'FILE_NAME_BAND_4',
                       'thermal_channel_path':'FILE_NAME_BAND_6',
                      
                       'red_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_3',
                       'red_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_3',
                       'nir_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_4',
                       'nir_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_4',
                       'thermal_channel_min_dn':'QUANTIZE_CAL_MIN_BAND_6',
                       'thermal_channel_max_dn':'QUANTIZE_CAL_MAX_BAND_6',
                      
                       'red_channel_min_rad':'RADIANCE_MINIMUM_BAND_3',
                       'red_channel_max_rad':'RADIANCE_MAXIMUM_BAND_3',
                       'nir_channel_min_rad':'RADIANCE_MINIMUM_BAND_4',
                       'nir_channel_max_rad':'RADIANCE_MAXIMUM_BAND_4',
                       'thermal_channel_min_rad':'RADIANCE_MINIMUM_BAND_6',
                       'thermal_channel_max_rad':'RADIANCE_MAXIMUM_BAND_6',
                      
                       'red_channel_mult':'RADIANCE_MULT_BAND_3',
                       'red_channel_add':'RADIANCE_ADD_BAND_3',
                       'nir_channel_mult':'RADIANCE_MULT_BAND_4',
                       'nir_channel_add':'RADIANCE_ADD_BAND_4',
                       'thermal_channel_mult':'RADIANCE_MULT_BAND_6',
                       'thermal_channel_add':'RADIANCE_ADD_BAND_6',
                       
                       'thermal_wavelength': 11.45,
                       
                       'thermal_k1':607.76,
                       'thermal_k2':1260.56,
                       
                       'red_channel_solar_irradiance': 1554,
                       'nir_channel_solar_irradiance': 1036,
                      
                       'earth_sun_distance':None,
                       'sun_elevation':'SUN_ELEVATION',
                       'sun_azimuth':'SUN_AZIMUTH'
                      }

    metadata_file_path = ''
    metadata_file = None
    landsat_version = None
    
    # Important metadata 
    acquisition_date = None
    acquisition_time = None
    
    red_channel_path = None
    nir_channel_path = None
    thermal_channel_path = None
    
    red_channel_min_dn = None
    red_channel_max_dn = None
    nir_channel_min_dn = None
    nir_channel_max_dn = None
    thermal_channel_min_dn = None
    thermal_channel_max_dn = None
    
    red_channel_min_rad = None
    red_channel_max_rad = None
    nir_channel_min_rad = None
    nir_channel_max_rad = None
    thermal_channel_min_rad = None
    thermal_channel_max_rad = None
    
    red_channel_mult = None
    red_channel_add = None
    nir_channel_mult = None
    nir_channel_add = None
    
    earth_sun_distance = None
    sun_elevation= None
    
    sun_azimuth = None
    
    
    def __init__(self, metadata_file_path, landsat_version):
        if not (landsat_version in self.supported_landsat_versions):
            raise ValueError('Unsupported landsat version')
        
        try:
            test_opening = open(metadata_file_path,'r')
            test_opening.close()
        except:
            raise IOError('File doesn\'t exists')
        
        
        self.metadata_file_path = metadata_file_path
        self.landsat_version = landsat_version
            
        self.read_metadata (self.metadata_file_path, self.landsat_version)
    
    def get_value_by_key(self, metadata_file, key):
        
        for line in open(metadata_file,'r'):
            if line.find(key) <> -1:
                equal_symbol_entrance = line.find ('=')
                value = line [equal_symbol_entrance+1:].replace(' ','').replace('"','').replace('\n','')
                return value
        raise IOError ('Parameter ' + key + ' not found at metadata')
        
    def calculate_earth_sun_distance(self, julian_day):
        return 1 - 0.01668*math.cos(julian_day*2*math.pi/365)   
    
    def read_metadata (self,metadata_file, landsat_version):
        print 'reading metadata...'
        
        if landsat_version == 'Landsat_8':
            landsat_dict = self.landsat_8_dict
        elif landsat_version == 'Landsat_7':
            landsat_dict = self.landsat_7_dict
        elif landsat_version == 'Landsat_5':
            landsat_dict = self.landsat_5_dict
        elif landsat_version == 'Landsat_4':
            landsat_dict = self.landsat_4_dict
        
                
        self.acquisition_date = datetime.strptime(self.get_value_by_key(metadata_file,landsat_dict['acquisition_date']),'%Y-%m-%d')
        self.acquisition_time = datetime.strptime(self.get_value_by_key(metadata_file,landsat_dict['acquisition_time']).split('.')[0],'%H:%M:%S')
        
        self.red_channel_path = os.path.dirname(metadata_file) + '/' + self.get_value_by_key(metadata_file,landsat_dict['red_channel_path'])
        self.nir_channel_path = os.path.dirname(metadata_file) + '/' + self.get_value_by_key(metadata_file,landsat_dict['nir_channel_path'])
        self.thermal_channel_path = os.path.dirname(metadata_file) + '/' + self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_path'])
        self.pan_channel_path = os.path.dirname(metadata_file) + '/' + self.get_value_by_key(metadata_file,landsat_dict['pan_channel_path'])
    
        self.red_channel_min_dn = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_min_dn']))
        self.red_channel_max_dn = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_max_dn']))
        self.nir_channel_min_dn = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_min_dn']))
        self.nir_channel_max_dn = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_max_dn']))
        self.thermal_channel_min_dn = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_min_dn']))
        self.thermal_channel_max_dn = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_max_dn']))
    
        self.red_channel_min_rad = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_min_rad']))
        self.red_channel_max_rad = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_max_rad']))
        self.nir_channel_min_rad = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_min_rad']))
        self.nir_channel_max_rad = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_max_rad']))
        self.thermal_channel_min_rad = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_min_rad']))
        self.thermal_channel_max_rad = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_max_rad']))
    
        self.red_channel_mult = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_mult']))
        self.red_channel_add = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_add']))
        self.nir_channel_mult = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_mult']))
        self.nir_channel_add = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_add']))
        self.thermal_channel_mult = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_mult']))
        self.thermal_channel_add = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_channel_add']))
        
        self.sun_elevation= math.radians(float(self.get_value_by_key(metadata_file,landsat_dict['sun_elevation'])))
        self.sun_zenith = math.radians(90) - self.sun_elevation
        
        self.sun_azimuth = math.radians(float(self.get_value_by_key(metadata_file,landsat_dict['sun_azimuth'])))
        
        self.thermal_wavelength = landsat_dict['thermal_wavelength']
        
        if landsat_dict['earth_sun_distance']:
            self.earth_sun_distance = float(self.get_value_by_key(metadata_file,landsat_dict['earth_sun_distance']))
        else:
            julian_day = self.acquisition_date.timetuple().tm_yday
            self.earth_sun_distance = self.calculate_earth_sun_distance(julian_day)
            
        if self.landsat_version == 'Landsat_8':
            self.red_channel_min_refl = float(self.get_value_by_key(metadata_file,landsat_dict['red_channel_min_refl']))
            self.nir_channel_min_refl = float(self.get_value_by_key(metadata_file,landsat_dict['nir_channel_min_refl']))
            self.red_channel_solar_irradiance = ((math.pi * self.earth_sun_distance * self.earth_sun_distance) * self.red_channel_max_rad) / (self.red_channel_min_refl)
            self.nir_channel_solar_irradiance = ((math.pi * self.earth_sun_distance * self.earth_sun_distance) * self.nir_channel_max_rad) / (self.nir_channel_min_refl)
            
            self.thermal_k1 = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_k1']))
            self.thermal_k2 = float(self.get_value_by_key(metadata_file,landsat_dict['thermal_k2']))
            
        else:    
            self.red_channel_solar_irradiance = landsat_dict['red_channel_solar_irradiance']
            self.nir_channel_solar_irradiance = landsat_dict['nir_channel_solar_irradiance']

            self.thermal_k1 = landsat_dict['thermal_k1']
            self.thermal_k2 = landsat_dict['thermal_k2']
            
        

#metadata = LandsatMetadata('E://dzz_mag//bolivia//LE72310722001223AGS00//LE72310722001223AGS00_MTL.txt','Landsat_7')
#print metadata.earth_sun_distance 
