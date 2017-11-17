#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
from sls_detector import Detector
#Detector needs to be online


class TestFileIndexAndNames(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()
        self.NMOD = 2
        self.NMODY = 2
        self.NMODX= 1


    def test_set_file_index(self):
        self.detector.file_index = 3
        self.assertEqual(self.detector.file_index, 3)

    def test_if_raising_on_negative(self):
        with self.assertRaises(Exception) as context:
            self.detector.file_index = -75
            self.assertTrue('Index needs to be positive ' in str(context.exception))

    def test_set_file_name(self):
        fname = 'sapmi'
        self.detector.file_name = fname
        self.assertEqual(self.detector.file_name, fname)
        
        
    def test_get_number_of_modules(self):
        self.assertEqual(self.detector.n_modules, self.NMOD)
        
    def test_module_geometry_vertical(self):
        self.assertEqual(self.detector.module_geometry.vertical, self.NMODY)

    def test_module_geometry_horizontal(self):
        self.assertEqual(self.detector.module_geometry.horizontal, self.NMODX)
        
    def test_file_path_type(self):
        self.assertTrue(isinstance(self.detector.file_path, str))
    
    def test_set_and_get_file_path(self):
        path = '/home/l_frojdh/out'
        self.detector.file_path = path
        self.assertEqual(self.detector.file_path, path)
        
    def test_if_raising_on_non_existing_path(self):
        with self.assertRaises(Exception) as context:
            self.detector.file_path = '/asiv/aksurva/oirjoa/'
            self.assertTrue('File path does not exists' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

