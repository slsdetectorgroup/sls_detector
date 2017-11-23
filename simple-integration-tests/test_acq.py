#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
from sls_detector import Detector
import random
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

        
#    def test_set_and_get_exp_time(self):
#        t = 3.75
#        self.detector.exp_time = t
#        self.assertAlmostEqual(self.detector.exp_time, t,5)
#        
#    def test_set_and_get_period(self):
#        t = 3.75
#        self.detector.frame_period = t
#        self.assertAlmostEqual(self.detector.frame_period, t,5)        
#        
#    def test_set_and_get_nframes(self):
#        self.detector.n_frames = 5
#        self.assertEqual(self.detector.n_frames, 5)
#
#    def test_if_n_frames_raise_on_neg_values(self):
#        with self.assertRaises(Exception) as context:
#            self.detector.n_frames = -1
#            self.assertTrue('Invalid value for n_frames' in str(context.exception))
#
#    def test_if_n_frames_raise_on_float(self):
#        with self.assertRaises(Exception) as context:
#            self.detector.n_frames = -1
#            self.assertTrue('incompatible function arguments' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

