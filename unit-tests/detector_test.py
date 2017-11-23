#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monkeypatched tests to decode the return values and check calling values of 
the Python class
"""
from unittest.mock import Mock
import pytest
from pytest_mock import mocker

import sys
sys.path.append('/home/l_frojdh/slsdetectorgrup/sls_detector')

import _sls_detector

@pytest.fixture
def d():
    from sls_detector import Detector
    return Detector()

#def test_has_hostname_attribute(d):
#    assert True == hasattr(d, 'hostname')

#def test_hostname_two_names(d, monkeypatch):
#    def mockreturn(str):
#        return 'beb059+beb048+'
#    monkeypatch.setattr(_sls_detector.DetectorApi, 'getHostname', mockreturn)
#    assert d.hostname == ['beb059', 'beb048']


def test_acq_call(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.acq')
    d.acq()
    mock_det.assert_called_once_with()
    
def test_busy_call(d, mocker):  
    mock_det = mocker.patch('_sls_detector.DetectorApi.getAcquiringFlag')
    mock_det.return_value = False
    assert d.busy == False

def test_assign_to_busy(d,mocker):
    with pytest.raises(AttributeError):
        d.busy = True

def test_assign_to_detector_type(d,mocker):
    with pytest.raises(AttributeError):
        d.detector_type = 'Eiger'
 
def test_det_type(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getDetectorType')
    mock_det.return_value = 'Eiger'
    assert d.detector_type == 'Eiger'  

def test_set_dynamic_range_4(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDynamicRange')
    d.dynamic_range = 4
    mock_det.assert_called_with(4)

def test_set_dynamic_range_8(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDynamicRange')
    d.dynamic_range = 8
    mock_det.assert_called_with(8)


def test_set_dynamic_range_16(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDynamicRange')
    d.dynamic_range = 16
    mock_det.assert_called_with(16)

def test_set_dynamic_range_32(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDynamicRange')
    d.dynamic_range = 32
    mock_det.assert_called_with(32)

def test_set_dynamic_range_raises_exception(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDynamicRange')
    with pytest.raises(ValueError):
        d.dynamic_range = 17

def test_get_dynamic_range_32(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getDynamicRange')
    mock_det.return_value = 32
    dr = d.dynamic_range
    assert dr == 32    

def test_eiger_matrix_reset(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getCounterBit')
    mock_det.return_value = True
    assert d.eiger_matrix_reset == True

def test_set_eiger_matrix_reset(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setCounterBit')
    d.eiger_matrix_reset = True
    mock_det.assert_called_once_with(True)
 

def test_get_exposure_time(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getExposureTime')
    mock_det.return_value = 100000000
    assert d.exposure_time == 0.1

def test_set_exposure_time(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setExposureTime')
    d.exposure_time = 1.5   
    mock_det.assert_called_once_with(1500000000)
    
def test_set_exposure_time_less_than_zero(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setExposureTime')
    with pytest.raises(ValueError):
        d.exposure_time = -7       
        
    
def test_get_file_index(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getFileIndex')
    mock_det.return_value = 8
    assert d.file_index == 8  

def test_set_file_index(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFileIndex')
    d.file_index = 9
    mock_det.assert_called_with(9)


def test_set_file_index_raises_on_neg(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFileIndex')
    with pytest.raises(ValueError):
        d.file_index = -9


def test_get_file_name(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getFileName')
    fn = d.file_name
    mock_det.assert_called_once_with()

def test_set_file_name(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFileName')
    d.file_name = 'hej'
    mock_det.assert_called_once_with('hej')

def test_get_file_path(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getFilePath')
    fp = d.file_path
    mock_det.assert_called_once_with()

def test_set_file_path_when_path_exists(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFilePath')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.exists')
    mock_os.return_value = True
    d.file_path = '/path/to/something/'
    mock_det.assert_called_once_with('/path/to/something/')

def test_set_file_path_raises_when_not_exists(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFilePath')
    mock_os = mocker.patch('os.path.exists')
    mock_os.return_value = False
    with pytest.raises(FileNotFoundError):
        d.file_path = '/path/to/something/'
        
def test_get_file_write(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.getFileWrite')
    mock_det.return_value = False
    assert d.file_write == False

def test_set_file_write(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.setFileWrite')
    d.file_write = True
    mock_det.assert_called_once_with(True)


def test_get_firmware_version(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.getFirmwareVersion')
    mock_det.return_value = 20
    assert d.firmware_version == 20

def test_cannot_set_fw_version(d, mocker):
    with pytest.raises(AttributeError):
        d.firmware_version = 20

def test_get_high_voltage_call_signature(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.getDac')
    hv = d.high_voltage
    mock_det.assert_called_once_with('vhighvoltage', -1)

def test_get_high_voltage(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.getDac')
    mock_det.return_value = 80
    assert d.high_voltage == 80

#self._api.setDac('vhighvoltage', -1, voltage)
def test_set_high_voltage(d, mocker):   
    mock_det = mocker.patch('_sls_detector.DetectorApi.setDac')
    d.high_voltage = 80
    mock_det.assert_called_once_with('vhighvoltage', -1, 80)  
    
def test_decode_hostname_two_names(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getHostname')
    mock_det.return_value = 'beb059+beb048+'
    assert d.hostname == ['beb059', 'beb048']

def test_decode_hostname_four_names(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getHostname')
    mock_det.return_value = 'beb059+beb048+beb120+beb153+'
    assert d.hostname == ['beb059', 'beb048', 'beb120', 'beb153']

def test_decode_hostname_blank(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getHostname')
    mock_det.return_value = ''
    assert d.hostname == []

def test_get_image_size_gives_correct_size(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.getImageSize')
    mock_det.return_value = (512,1024)
    im_size = d.image_size
    assert im_size.rows == 512
    assert im_size.cols == 1024

def test_cannot_set_image_size(d, mocker):
    with pytest.raises(AttributeError):
        d.image_size = (20, 50)


def test_load_config(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.readConfigurationFile')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = True
    d.load_config('/path/to/my/file.config')
    mock_det.assert_called_once_with('/path/to/my/file.config')

def test_load_config_raises_when_file_is_not_found(d, mocker):
    mock_det = mocker.patch('_sls_detector.DetectorApi.readConfigurationFile')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = False
    with pytest.raises(FileNotFoundError):
        d.load_config('/path/to/my/file.config')
