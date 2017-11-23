#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
import random
from sls_detector import Detector
#Detector needs to be online


class TestTimers(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()

    def test_hasattr_exposure_time(self):
        self.assertTrue( hasattr(self.detector, 'exposure_time') )


    def test_set_and_get_exp_time_random(self):
        for _ in range(10):
            t = random.uniform(0.1, 5)
            self.detector.exp_time = t
            self.assertAlmostEqual(self.detector.exp_time, t,5)

            
    def test_set_and_get_exposure_time(self):
        t = 3.75
        self.detector.exposure_time = t
        self.assertAlmostEqual(self.detector.exposure_time, t,5)
    
    def test_hasattr_sub_exposure_time(self):
        self.assertTrue(hasattr(self.detector, 'sub_exposure_time'))
    
    def test_set_and_get_sub_exposure_time(self):
        t = 0.0023
        self.detector.sub_exposure_time = t
        self.assertAlmostEqual(self.detector.sub_exposure_time, t,5 )
    
    def test_hasattr_period(self):
        self.assertTrue( hasattr(self.detector, 'period') )
    
        
    def test_set_and_get_period(self):
        t = 3.75
        self.detector.period = t
        self.assertAlmostEqual(self.detector.period, t,5 )        

    def test_hasattr_n_frames(self):
        self.assertTrue( hasattr(self.detector, 'n_frames') )
        
    def test_set_and_get_nframes(self):
        self.detector.n_frames = 5
        self.assertEqual(self.detector.n_frames, 5)

    def test_if_n_frames_raise_on_neg_values(self):
        with self.assertRaises(Exception) as context:
            self.detector.n_frames = -1
            self.assertTrue('Invalid value for n_frames' in str(context.exception))

    def test_if_n_frames_raise_on_float(self):
        with self.assertRaises(Exception) as context:
            self.detector.n_frames = -1
            self.assertTrue('incompatible function arguments' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

