#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monkeypatched tests to decode the return values and check calling values of 
the Python class
"""

import pytest


import _sls_detector

@pytest.fixture
def d():
    from sls_detector import Detector
    return Detector()

def test_has_hostname_attribute(d):
    assert True == hasattr(d, 'hostname')

def test_hostname_two_names(d, monkeypatch):
    def mockreturn(str):
        return 'beb059+beb048+'
    monkeypatch.setattr(_sls_detector.DetectorApi, 'getHostname', mockreturn)
    assert d.hostname == ['beb059', 'beb048']

def test_hostname_three_names(d, monkeypatch):
    def mockreturn(str):
        return 'beb059+beb048+beb123+'
    monkeypatch.setattr(_sls_detector.DetectorApi, 'getHostname', mockreturn)
    assert d.hostname == ['beb059', 'beb048', 'beb123']
    
def test_not_busy_without_detector(d):
    assert d.busy == False
    
def test_has_attribute_n_modules(d):
    assert True == hasattr(d, 'n_modules')
    
def test_n_moduels_without_detector(d):
    assert d.n_modules == 0
    
def test_n_modules_mock_api(d, monkeypatch):
    def mockreturn(int):
        return 2
    monkeypatch.setattr(_sls_detector.DetectorApi, 'getNumberOfDetectors', mockreturn)
    assert d.n_modules == 2
    
def test_len_det_with_mock_api(d, monkeypatch):
    def mockreturn(int):
        return 4
    monkeypatch.setattr(_sls_detector.DetectorApi, 'getNumberOfDetectors', mockreturn)
    assert len(d) == 4
    
    
def test_hasattr_dacs(d):
    assert True == hasattr(d, 'dacs')
    
def test_hasattr_file_index(d):
    assert True == hasattr(d, 'file_index')
    
def test_file_index_uninitialized(d):
    assert d.file_index == -100
    
def test_file_index_with_mock_api(d, monkeypatch):
    def mockreturn(int):
        return 52
    monkeypatch.setattr(_sls_detector.DetectorApi, 'getFileIndex', mockreturn)
    
    assert d.file_index == 52
    
    
def test_hasattr_file_write(d):
    assert True == hasattr(d, 'file_write')
    
def test_file_write_uninitialized(d):
    assert False == d.file_write
    
def test_fw_version(d):
    assert -1 == d.firmware_version
    
def test_high_voltage(d):
    assert -1 == d.high_voltage
    
    
    
def test_status(d):
    assert 'idle' == d.status
    
