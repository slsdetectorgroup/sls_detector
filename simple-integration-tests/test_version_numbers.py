#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for hostname related functions of the detector
"""
import pytest
import config_test

from sls_detector.errors import DetectorValueError

@pytest.fixture
def detector():
    from sls_detector import Detector
    d = Detector()
    return d


def test_firmware_version(detector):
    assert detector.firmware_version == config_test.fw_version


