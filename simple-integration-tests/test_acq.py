#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
from sls_detector import Detector
#Detector needs to be online


class TestAcquire(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()

    @classmethod
    def tearDown(self):
        self.detector.eiger_matrix_reset = True

    def test_not_busy(self):
        self.assertFalse(self.detector.busy)
        
    def test_set_eiger_resmat_false(self):
        self.detector.eiger_matrix_reset = False
        self.assertFalse(self.detector.eiger_matrix_reset) 

           
    def test_set_eiger_resmat_true(self):
        self.detector.eiger_matrix_reset = True
        self.assertTrue(self.detector.eiger_matrix_reset)
        
    def test_set_full_speed(self):
        self.detector.readout_clock = 'Full Speed'
        self.assertEqual(self.detector.readout_clock, 'Full Speed')

    def test_set_half_speed(self):
        self.detector.readout_clock = 'Half Speed'
        self.assertEqual(self.detector.readout_clock, 'Half Speed')
        
    def test_set_quarter_speed(self):
        self.detector.readout_clock = 'Quarter Speed'
        self.assertEqual(self.detector.readout_clock, 'Quarter Speed')        

    def test_set_super_slow_speed(self):
        self.detector.readout_clock = 'Super Slow Speed'
        self.assertEqual(self.detector.readout_clock, 'Super Slow Speed')     

        
if __name__ == '__main__':
    unittest.main()

