#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests specific for the firmware.

Check that register values are correct after starting an exposure

0x4 exposure time
0x5 period
0x6 sub exposure time

"""
import pytest
import config_test
from fixtures import detector, eiger, jungfrau, eigertest, jungfrautest
from sls_detector.errors import DetectorValueError
from sls_detector.utils import  eiger_register_to_time



@eigertest
def test_short_exposure_time(eiger):
    t = 1.23
    eiger.exposure_time = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    #Register 0x4 holds exposure time
    reg = eiger.register[0x4]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)

@eigertest
def test_short_minimal_exposure_time(eiger):
    t = 1e-8
    eiger.exposure_time = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    #Register 0x4 holds exposure time
    reg = eiger.register[0x4]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)


@eigertest
def test_long_exposure_time(eiger):
    t = 623
    eiger.exposure_time = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    # Register 0x4 holds exposure time
    reg = eiger.register[0x4]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)


@eigertest
def test_short_period(eiger):
    t = 0.1
    eiger.exposure_time = 0.001
    eiger.period = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    # Register 0x5 holds period
    reg = eiger.register[0x5]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)


@eigertest
def test_long_period(eiger):
    t = 8900
    eiger.exposure_time = 0.001
    eiger.period = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    # Register 0x5 holds period
    reg = eiger.register[0x5]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)

@eigertest
def test_zero_period_with_acq(eiger):
    t = 0
    eiger.exposure_time = 0.001
    eiger.period = t
    eiger.file_write = False
    eiger.acq()

    # Register 0x5 holds period
    reg = eiger.register[0x5]
    assert pytest.approx(t, 1e-9) == eiger_register_to_time(reg)

@eigertest
def test_subexptime(eiger):
    t = 0.001
    eiger.sub_exposure_time = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    # Register 0x6 holds sub exposure time
    # time is stored straight as n clocks
    reg = eiger.register[0x6]
    assert pytest.approx(t, 1e-9) == reg/100e6

@eigertest
def test_longer_subexptime(eiger):
    t = 0.0236
    eiger.sub_exposure_time = t
    eiger.file_write = False
    eiger.start_detector()
    eiger.stop_detector()

    # Register 0x6 holds sub exposure time
    # time is stored straight as n clocks
    reg = eiger.register[0x6]
    assert pytest.approx(t, 1e-9) == reg/100e6

@eigertest
def test_n_frames(eiger):
    t = 0.01
    n = 17
    eiger.exposure_time = t
    eiger.n_frames = n
    eiger.file_write = False
    eiger.acq()

    # Register 0x6 holds sub exposure time
    # time is stored straight as n clocks
    reg = eiger.register[0x3]
    assert reg == n