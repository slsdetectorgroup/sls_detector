#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests specific for the firmware.
"""
import pytest
import config_test
from fixtures import detector, eiger, jungfrau, eigertest, jungfrautest
from sls_detector.errors import DetectorValueError




@eigertest
def test_short_exposure_time(eiger):
    t = 1.23
    eiger.exposure_time = t
    eiger.file_write = False
    eiger.acq()

    #Check the regiser holding the exposure time
    reg = eiger.register[0x4]

    assert pytest.approx(t) == decode(reg)

# @eigertest
# def test_set_dynamic_range_raises(eiger):
#     with pytest.raises(DetectorValueError):
#         eiger.dynamic_range = 75



