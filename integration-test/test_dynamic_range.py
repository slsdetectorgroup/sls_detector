#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit testing of sls_detector.plot
TODO! Far from complete
"""
import unittest
from sls_detector import Detector
#Detector needs to be online

class TestDynamicRange(unittest.TestCase):
    
    def setUp(self):
        self.detector = Detector()
        self.detector.dynamic_range = 4
        
    def test_setting_to_32(self):
        self.detector.dynamic_range = 32
        self.assertEqual(self.detector.dynamic_range, 32)

    def test_setting_to_16(self):
        self.detector.dynamic_range = 16
        self.assertEqual(self.detector.dynamic_range, 16)
        
    def test_setting_to_8(self):
        self.detector.dynamic_range = 8
        self.assertEqual(self.detector.dynamic_range, 8)
        
    def test_setting_to_4(self):
        self.detector.dynamic_range = 4
        self.assertEqual(self.detector.dynamic_range, 4)
        
    def test_if_raising_on_wrong_value(self):
        with self.assertRaises(Exception) as context:
            self.detector.dynamic_range = 75
            self.assertTrue('Cannot set dynamic range ' in str(context.exception))


if __name__ == '__main__':
    unittest.main()

