#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing setting dynamic range for Eiger. If the detector is not Eiger the tests are skipped
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

@pytest.fixture
def eiger():
    from sls_detector import Eiger
    return Eiger()

eigertest = pytest.mark.skipif(detector_type != 'Eiger', reason = 'Only valid for Eiger')

@eigertest
def test_set_dynamic_range(eiger):
    for dr in [4,8,16,32]:
        eiger.dynamic_range = dr
        assert eiger.dynamic_range == dr
@eigertest
def test_set_dynamic_range_raises(eiger):
    with pytest.raises(DetectorValueError):
        eiger.dynamic_range = 75



