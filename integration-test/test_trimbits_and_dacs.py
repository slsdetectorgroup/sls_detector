#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
import random
from sls_detector import Detector



class TestTrimbitsAndDacs(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()

#    @classmethod
#    def tearDown(self):
#        self.detector.eiger_matrix_reset = True

    def test_set_and_get_trimbits_32(self):
        self.detector.trimbits = 32
        self.assertEqual(self.detector.trimbits, 32)
    
    def test_set_and_get_trimbits_17(self):
        self.detector.trimbits = 17
        self.assertEqual(self.detector.trimbits, 17)       
    
    def test_raises_when_tb_is_too_large(self):
        with self.assertRaises(Exception) as context:
            self.detector.trimbits = 89
            self.assertTrue('Trimbit setting 89' in str(context.exception))
            
    def test_raises_when_tb_is_too_small(self):
        with self.assertRaises(Exception) as context:
            self.detector.trimbits = -10
            self.assertTrue('Trimbit setting -10' in str(context.exception))



if __name__ == '__main__':
    unittest.main()

