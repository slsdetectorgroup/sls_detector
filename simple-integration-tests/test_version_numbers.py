#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
from sls_detector import Detector


import config_test as cfg

class TestVersionNumbersAndNames(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()

    def test_hasattr_firmware_version(self):
        self.assertTrue( hasattr(self.detector, 'firmware_version') )

    def test_firmware_version(self):
        self.assertEqual(self.detector.firmware_version, cfg.fw_version)

    def tess_type_of_detector(self):
        a = self.detector.detector_type
        self.assertEqual(a, cfg.detector_type)

if __name__ == '__main__':
    unittest.main()
