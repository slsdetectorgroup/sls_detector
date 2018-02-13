#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import pytest
import config_test

from sls_detector.errors import DetectorValueError

from sls_detector import Detector
detector_type = Detector().detector_type

@pytest.fixture
def detector():
    from sls_detector import Detector
    return Detector()


def test_get_hostname(detector):
    for detector_host, config_host in zip(detector.hostname, config_test.known_hostnames):
        assert detector_host == config_host

def test_hostname_has_same_length_as_n_modules(detector):
    assert len(detector.hostname) == detector.n_modules

def test_hostname_is_list(detector):
    assert isinstance(detector.hostname, list) == True