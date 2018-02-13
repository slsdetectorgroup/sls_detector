#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for trimbit and dac related functions
"""
import pytest
import config_test

from sls_detector.errors import DetectorValueError

from sls_detector import Detector
detector_type = Detector().detector_type



@pytest.fixture
def eiger():
    from sls_detector import Eiger
    return Eiger()

@pytest.fixture
def jungfrau():
    from sls_detector import Jungfrau
    return Jungfrau()

eigertest = pytest.mark.skipif(detector_type != 'Eiger', reason = 'Only valid for Eiger')
jungfrautest = pytest.mark.skipif(detector_type != 'Jungfrau', reason = 'Only valid for Jungfrau')

@eigertest
def test_set_trimbits(eiger):
    """Limited values due to time"""
    for i in [17, 32, 60]:
        print(i)
        eiger.trimbits = i
        assert eiger.trimbits == i

@eigertest
def test_set_trimbits_raises_on_too_big(eiger):
    with pytest.raises(DetectorValueError):
        eiger.trimbits = 75

@eigertest
def test_set_trimbits_raises_on_negative(eiger):
    with pytest.raises(DetectorValueError):
        eiger.trimbits = -5


@jungfrautest
def test_jungfrau(jungfrau):
    """Example of a test that is not run with Eiger connected"""
    pass
