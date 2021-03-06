#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing parameters and methods of the Detector class using mocks
"""
from unittest.mock import Mock
import pytest
from pytest_mock import mocker

import sys
sys.path.append('/home/l_frojdh/slsdetectorgrup/sls_detector')

import _sls_detector
from sls_detector.errors import DetectorValueError, DetectorError
from sls_detector.utils import all_equal, element_if_equal
@pytest.fixture
def d():
    from sls_detector import Detector
    return Detector()


def test_length_zero(d):
    assert len(d) == 0

def test_acq_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.acq')
    d.acq()
    m.assert_called_once_with()



def test_busy_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getAcquiringFlag')
    m.return_value = False
    assert d.busy == False

def test_set_busy(d):
    d.busy = True
    assert d.busy == True
    assert d._api.getAcquiringFlag() == True
    d.busy = False
    assert d.busy == False
    assert d._api.getAcquiringFlag() == False

def test_error_mask(d):
    d._api.setErrorMask(1)
    assert d.error_mask == 1
    d.clear_errors()

def test_error_handling(d):
    with pytest.raises(DetectorError):
        d._provoke_error()

def test_assign_to_detector_type(d):
    with pytest.raises(AttributeError):
        d.detector_type = 'Eiger'

def test_det_type(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDetectorType')
    m.return_value = 'Eiger'
    assert d.detector_type == 'Eiger'


def test_get_exposure_time(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getExposureTime')
    m.return_value = 100000000
    assert d.exposure_time == 0.1

def test_set_exposure_time(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setExposureTime')
    d.exposure_time = 1.5
    m.assert_called_once_with(1500000000)

def test_set_exposure_time_less_than_zero(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setExposureTime')
    with pytest.raises(DetectorValueError):
        d.exposure_time = -7


def test_get_file_index(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getFileIndex')
    m.return_value = 8
    assert d.file_index == 8

def test_set_file_index(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setFileIndex')
    d.file_index = 9
    m.assert_called_with(9)


def file_index_with_no_detector(d):
    assert d.file_index == -100

def dr_with_no_detector(d):
    assert d.dynamic_range == -100

def test_set_file_index_raises_on_neg(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setFileIndex')
    with pytest.raises(ValueError):
        d.file_index = -9


def test_get_file_name(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getFileName')
    d.file_name
    m.assert_called_once_with()

def test_set_file_name(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setFileName')
    d.file_name = 'hej'
    m.assert_called_once_with('hej')

def test_get_file_path(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getFilePath')
    d.file_path
    m.assert_called_once_with()

def test_set_file_path_when_path_exists(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setFilePath')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.exists')
    mock_os.return_value = True
    d.file_path = '/path/to/something/'
    m.assert_called_once_with('/path/to/something/')

def test_set_file_path_raises_when_not_exists(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setFilePath')
    mock_os = mocker.patch('os.path.exists')
    mock_os.return_value = False
    with pytest.raises(FileNotFoundError):
        d.file_path = '/path/to/something/'

def test_get_file_write(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getFileWrite')
    m.return_value = False
    assert d.file_write == False

def test_set_file_write(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setFileWrite')
    d.file_write = True
    m.assert_called_once_with(True)


def test_get_firmware_version(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getFirmwareVersion')
    m.return_value = 20
    assert d.firmware_version == 20

def test_cannot_set_fw_version(d):
    with pytest.raises(AttributeError):
        d.firmware_version = 20

def test_get_high_voltage_call_signature(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDac')
    d.high_voltage
    m.assert_called_once_with('vhighvoltage', -1)

def test_get_high_voltage(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDac')
    m.return_value = 80
    assert d.high_voltage == 80

#self._api.setDac('vhighvoltage', -1, voltage)
def test_set_high_voltage(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setDac')
    d.high_voltage = 80
    m.assert_called_once_with('vhighvoltage', -1, 80)

def test_decode_hostname_two_names(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getHostname')
    m.return_value = 'beb059+beb048+'
    assert d.hostname == ['beb059', 'beb048']

def test_decode_hostname_four_names(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getHostname')
    m.return_value = 'beb059+beb048+beb120+beb153+'
    assert d.hostname == ['beb059', 'beb048', 'beb120', 'beb153']

def test_decode_hostname_blank(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getHostname')
    m.return_value = ''
    assert d.hostname == []

def test_get_image_size_gives_correct_size(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getImageSize')
    m.return_value = (512,1024)
    im_size = d.image_size
    assert im_size.rows == 512
    assert im_size.cols == 1024



def test_load_config(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.readConfigurationFile')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = True
    d.load_config('/path/to/my/file.config')
    m.assert_called_once_with('/path/to/my/file.config')

def test_load_config_raises_when_file_is_not_found(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.readConfigurationFile')
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = False
    with pytest.raises(FileNotFoundError):
        d.load_config('/path/to/my/file.config')

def test_load_parameters(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.readParametersFile')
    #To avoid raising an exception because path is not there
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = True
    d.load_parameters('/path/to/my/file.par')
    m.assert_called_once_with('/path/to/my/file.par')

def test_load_parameters_raises_when_file_is_not_found(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.readParametersFile')
    mock_os = mocker.patch('os.path.isfile')
    mock_os.return_value = False
    with pytest.raises(FileNotFoundError):
        d.load_parameters('/path/to/my/file.par')

#getDetectorGeometry
def test_get_module_geometry_gives_correct_size(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDetectorGeometry')
    m.return_value = (13,7)
    g = d.module_geometry
    assert g.vertical == 7
    assert g.horizontal == 13

def test_get_module_geometry_access(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDetectorGeometry')
    m.return_value = (12,3)
    assert d.module_geometry[0] == 12
    assert d.module_geometry[1] == 3
    assert d.module_geometry.vertical == 3
    assert d.module_geometry.horizontal == 12

def test_module_geometry_without_detectors(d):
    t = d.module_geometry
    assert t.horizontal == 0
    assert t.vertical == 0

def test_get_n_frames(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNumberOfFrames')
    m.return_value = 3
    assert d.n_frames == 3

def test_set_n_frames(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setNumberOfFrames')
    d.n_frames = 9
    m.assert_called_once_with(9)

def test_nframes_without_detector(d):
    assert d.n_frames == -100

def test_set_n_frames_raises_on_neg(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setNumberOfFrames')
    with pytest.raises(DetectorValueError):
        d.n_frames = -1

def test_set_n_frames_raises_on_zero(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setNumberOfFrames')
    with pytest.raises(DetectorValueError):
        d.n_frames = 0

def test_n_cycles_without_detector(d):
    assert d.n_cycles == -100

def test_set_n_cycles_raises_on_zero(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setCycles')
    with pytest.raises(DetectorValueError):
        d.n_cycles = 0

def test_set_n_cycles(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setCycles')
    d.n_cycles = 56
    m.assert_called_once_with(56)



def test_n_measurements_without_detector(d):
    assert d.n_measurements == -100

def test_set_n_measurements_raises_on_zero(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setNumberOfMeasurements')
    with pytest.raises(DetectorValueError):
        d.n_measurements = 0

def test_set_n_measurements(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setNumberOfMeasurements')
    d.n_measurements = 560
    m.assert_called_once_with(560)

def test_get_n_modules_no_detector(d):
    assert d.n_modules == 0

def test_get_n_modules(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNumberOfDetectors')
    m.return_value = 12
    assert d.n_modules == 12

def test_get_period_time(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getPeriod')
    m.return_value = 130000000
    assert d.period == 0.13

def test_set_period_time(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setPeriod')
    d.period = 1.953
    m.assert_called_once_with(1953000000)

def test_set_period_time_less_than_zero(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setPeriod')
    with pytest.raises(ValueError):
        d.period = -7


def test_get_online(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getOnline')
    d.online
    m.assert_called_once_with()

def test_set_online(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setOnline')
    d.online = True
    m.assert_called_once_with(True)

def test_last_client_ip_no_detector(d):
    assert d.last_client_ip == ''

def test_last_cliten_ip_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getLastClientIP')
    d.last_client_ip
    m.assert_called_once_with()

#-------------------------------------------------------------Rate correction
def test_get_rate_correction(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getRateCorrection')
    m.return_value = [132,129]
    assert d.rate_correction == [132,129]

def test_set_rate_correction(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setRateCorrection')
    mock_n = mocker.patch('_sls_detector.DetectorApi.getNumberOfDetectors')
    mock_n.return_value = 3
    d.rate_correction = [123,90,50]
    m.assert_called_once_with([123,90,50])

def test_set_rate_correction_raises_on_wrong_number_of_values(d, mocker):
    mocker.patch('_sls_detector.DetectorApi.setRateCorrection')
    mock_n = mocker.patch('_sls_detector.DetectorApi.getNumberOfDetectors')
    mock_n.return_value = 4
    with pytest.raises(ValueError):
        d.rate_correction = [123,90,50]

#----------------------------------------------------------------Readout clock
def test_get_readout_clock_0(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getReadoutClockSpeed')
    m.return_value = 0
    assert d.readout_clock == 'Full Speed'

def test_get_readout_clock_1(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getReadoutClockSpeed')
    m.return_value = 1
    assert d.readout_clock == 'Half Speed'

def test_get_readout_clock_2(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getReadoutClockSpeed')
    m.return_value = 2
    assert d.readout_clock == 'Quarter Speed'

def test_get_readout_clock_3(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getReadoutClockSpeed')
    m.return_value = 3
    assert d.readout_clock == 'Super Slow Speed'

def test_set_readout_clock_0(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setReadoutClockSpeed')
    d.readout_clock = 'Full Speed'
    m.assert_called_once_with(0)

def test_set_readout_clock_1(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setReadoutClockSpeed')
    d.readout_clock = 'Half Speed'
    m.assert_called_once_with(1)

def test_set_readout_clock_2(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setReadoutClockSpeed')
    d.readout_clock = 'Quarter Speed'
    m.assert_called_once_with(2)

def test_set_readout_clock_3(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setReadoutClockSpeed')
    d.readout_clock = 'Super Slow Speed'
    m.assert_called_once_with(3)

#----------------------------------------------------------------rx_datastream
def test_get_rx_datastream(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getRxDataStreamStatus')
    m.return_value = False
    assert d.rx_datastream == False

def test_set_rx_datastream(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setRxDataStreamStatus')
    d.rx_datastream = True
    m.assert_called_once_with(True)

def test_get_rx_zmqip(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNetworkParameter')
    d.rx_zmqip
    m.assert_called_once_with('rx_zmqip')

def test_get_rx_zmqport_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNetworkParameter')
    d.rx_zmqport
    m.assert_called_once_with('rx_zmqport')

def test_get_rx_zmqport_decode(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNetworkParameter')
    m.return_value = ['30001', '30003']
    assert d.rx_zmqport == [30001, 30003]

def test_get_rx_zmqport_empty(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getNetworkParameter')
    m.return_value = ''
    assert d.rx_zmqport == []


#--------------------------------------------------------------------status
def test_status_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getRunStatus')
    d.status
    m.assert_called_once_with()

def test_start_detecor(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.startAcquisition')
    d.start_detector()
    m.assert_called_once_with()

def test_stop_acq_call(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.stopAcquisition')
    d.stop_detector()
    m.assert_called_once_with()



#------------------------------------------------------------------timing mode
def test_get_timing_mode(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getTimingMode')
    d.timing_mode
    m.assert_called_once_with()

def test_set_timing_mode(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setTimingMode')
    d.timing_mode = 'auto'
    m.assert_called_once_with('auto')

#----------------------------------------------------------------vthreshold
def test_get_vthreshold(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.getDac')
    d.vthreshold
    m.assert_called_once_with('vthreshold', -1)

def test_set_vthreshold(d, mocker):
    m = mocker.patch('_sls_detector.DetectorApi.setDac')
    d.vthreshold = 1675
    m.assert_called_once_with('vthreshold', -1, 1675)




