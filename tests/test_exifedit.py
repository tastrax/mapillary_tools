import os
import sys
import unittest
from PIL import Image, ExifTags
from PIL import ExifTags
from os import path
sys.path.append("python")
from lib.exifedit import ExifEdit
import datetime
import shutil
import math

def decimal_to_deg_min_sec(value, precision):
    '''
    Convert the degrees in float to degrees, minutes and seconds as tuple of tuples with precision identifier.
    >>> latitude = 23.122886
    >>> deg_to_deg_min_sec(latitude)
    ((23.0, 1), (7.0, 1), (223896.0, 10000))#CHECK the precision on the seconds
    '''
    deg = math.floor(value)
    min = math.floor((value-deg)*60)
    sec = math.floor((value-deg-min/60) * 36000000)

    return ((deg, 1), (min, 1), (sec, precision))


"""Initialize all the neccessary data"""

EMPTY_EXIF_FILE = os.path.join("tests", "data", "empty_exif.jpg")
EMPTY_EXIF_FILE_TEST = os.path.join("tests", "data", "tmp", "empty_exif.jpg")
        
#more info on the standard exif tags https://sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
EXIF_PRIMARY_TAGS_DICT = {y:x for x,y in ExifTags.TAGS.iteritems()}
EXIF_GPS_TAGS_DICT = {y:x for x,y in ExifTags.GPSTAGS.iteritems()}

class ExifEditTests(unittest.TestCase):
    """tests for main functions."""
    
    def setUp(self):
        if not os.path.exists(os.path.join("tests", "data", "tmp")):
            os.makedirs(os.path.join("tests", "data", "tmp"))  
        shutil.copy2(EMPTY_EXIF_FILE, EMPTY_EXIF_FILE_TEST)     
        
    def tearDown(self):
        shutil.rmtree(os.path.join("tests", "data", "tmp"))
            
    def test_class_instance_unexisting_file(self):
        self.assertRaises(IOError, ExifEdit, "un_existing_file")
        
    def test_add_image_description(self):
        
        test_dictionary = {"key_numeric": 1,
                           "key_string": "one",
                           "key_list": [1,2],
                           "key_dict":{"key_dict1": 1, "key_dict2": 2}
                           }
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)   

        empty_exifedit.add_image_description(test_dictionary)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)   

        exif_data = self._load_exif()       
        self.assertEqual(str(test_dictionary), str(exif_data[EXIF_PRIMARY_TAGS_DICT['ImageDescription']]).replace('"','\''))
         
    def test_add_orientation(self):
        
        test_orientation = 2
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)   
        
        empty_exifedit.add_orientation(test_orientation)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual(test_orientation, exif_data[EXIF_PRIMARY_TAGS_DICT['Orientation']])
            
    def test_add_date_time_original(self):
        
        test_datetime = datetime.datetime.strptime("2016_08_31_08_29_26_249"+"000", "%Y_%m_%d_%H_%M_%S_%f")
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)        
       
        empty_exifedit.add_date_time_original(test_datetime)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual(test_datetime.strftime('%Y:%m:%d %H:%M:%S'), exif_data[EXIF_PRIMARY_TAGS_DICT['DateTimeOriginal']])
        
    def test_add_lat_lon(self):
        
        test_latitude = 50.5
        test_longitude = 15.5
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)        
        
        empty_exifedit.add_lat_lon(test_latitude, test_longitude)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual((decimal_to_deg_min_sec(test_latitude, 50000000), decimal_to_deg_min_sec(test_longitude, 50000000)), (exif_data[EXIF_PRIMARY_TAGS_DICT['GPSInfo']][EXIF_GPS_TAGS_DICT['GPSLatitude']], exif_data[EXIF_PRIMARY_TAGS_DICT['GPSInfo']][EXIF_GPS_TAGS_DICT['GPSLongitude']]))
        
    def test_add_camera_make_model(self):
        
        test_make = "test_make"
        test_model = "test_model"
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)

        empty_exifedit.add_camera_make_model(test_make, test_model)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)

        exif_data = self._load_exif()
        self.assertEqual((test_make, test_model), (exif_data[EXIF_PRIMARY_TAGS_DICT['Make']], exif_data[EXIF_PRIMARY_TAGS_DICT['Model']]))
    
    def test_add_dop(self):
        
        test_dop = 10.5
        test_dop_precision = 100
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)
 
        empty_exifedit.add_dop(test_dop, test_dop_precision)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual((test_dop*test_dop_precision, test_dop_precision), exif_data[EXIF_PRIMARY_TAGS_DICT['GPSInfo']][EXIF_GPS_TAGS_DICT['GPSDOP']])
        
    def test_add_altitude(self):
        
        test_altitude = 15.5
        test_altitude_precision = 100
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)

        empty_exifedit.add_altitude(test_altitude, test_altitude_precision)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual((test_altitude*test_altitude_precision, test_altitude_precision), exif_data[EXIF_PRIMARY_TAGS_DICT['GPSInfo']][EXIF_GPS_TAGS_DICT['GPSAltitude']])
    
    def test_add_direction(self):
        
        test_direction = 1
        test_direction_ref = "D"
        test_direction_precision = 100
        
        empty_exifedit = ExifEdit(EMPTY_EXIF_FILE_TEST)

        empty_exifedit.add_direction(test_direction, test_direction_ref, test_direction_precision)
        empty_exifedit.write(EMPTY_EXIF_FILE_TEST)
        
        exif_data = self._load_exif()
        self.assertEqual((test_direction*test_direction_precision, test_direction_precision), exif_data[EXIF_PRIMARY_TAGS_DICT['GPSInfo']][EXIF_GPS_TAGS_DICT['GPSImgDirection']])
    
    def _load_exif(self):   
            
        test_image = Image.open(EMPTY_EXIF_FILE_TEST)

        exif_data = test_image._getexif()
                
        return   exif_data
        
if __name__ == '__main__':
    unittest.main()