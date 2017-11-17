#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import unittest
from sls_detector import Detector
import config_test as cfg


class TestHostname(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.detector = Detector()


    def test_hostname_has_same_length_as_n_modules(self):
        self.assertEqual(self.detector.n_modules, len(self.detector.hostname))

    def test_first_hostname_is_correct(self):
        self.assertEqual(cfg.known_hostnames[0], self.detector.hostname[0])
        
    def test_second_hostname_is_correct(self):
        self.assertEqual(cfg.known_hostnames[1], self.detector.hostname[1])
        
    def test_return_type_is_list(self):
        self.assertTrue(isinstance(self.detector.hostname, list))

if __name__ == '__main__':
    unittest.main()

