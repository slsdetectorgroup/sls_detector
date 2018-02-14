#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General tests for the Detector class. Should not depend on the connected detector. Aim is to have tests working
for both Jungfrau and Eiger.

NOTE! Uses hostnames from config_test
"""

import pytest
import config_test

from sls_detector.errors import DetectorValueError

@pytest.fixture
def detector():
    from sls_detector import Detector
    d = Detector()
    yield d
    #Reset to a good state
    d.busy = False
    d.period = 0


def test_not_busy(detector):
    """Test that the detector is not busy from the start"""
    assert detector.busy == False

def test_set_busy_true_then_false(detector):
    """Test both cases of assignment"""
    detector.busy = True
    assert detector.busy == True
    detector.busy = False
    assert detector.busy == False

def test_set_readout_speed(detector):
    for s in ['Full Speed', 'Half Speed', 'Quarter Speed', 'Super Slow Speed']:
        detector.readout_clock = s
        assert detector.readout_clock == s

def test_wrong_speed_raises_error(detector):
    with pytest.raises(KeyError):
        detector.readout_clock = 'Something strange'

def test_readout_clock_remains(detector):
    s = detector.readout_clock
    try:
        detector.readout_clock = 'This does not exists'
    except KeyError:
        pass
    assert detector.readout_clock == s

def test_len_method(detector):
    """to test this we need to know the length, this we get from the configuration of hostnames"""
    assert len(detector) == len(config_test.known_hostnames)

def test_setting_cycles_to_zero_gives_error(detector):
    with pytest.raises(DetectorValueError):
        detector.cycles = 0

def test_setting_cycles_to_negative_gives_error(detector):
    with pytest.raises(DetectorValueError):
        detector.cycles = -50

def test_set_cycles_frome_one_to_ten(detector):
    for i in range(1,11):
        detector.cycles = i
        assert detector.cycles == i

def test_get_detector_type(detector):
    assert detector.detector_type == config_test.detector_type

def test_set_exposure_time(detector):
    detector.exposure_time = 3.125
    assert detector.exposure_time == 3.125

def test_negative_exposure_time_raises_error(detector):
    with pytest.raises(DetectorValueError):
        detector.exposure_time = -15

def test_set_file_index(detector):
    detector.file_index = 5
    assert detector.file_index == 5

def test_negative_file_index_raises(detector):
    with pytest.raises(ValueError):
        detector.file_index = -8

def test_setting_file_name(detector):
    fname = 'hej'
    detector.file_name = fname
    assert detector.file_name == fname

def test_set_file_write(detector):
    detector.file_write = True
    assert detector.file_write == True

    detector.file_write = False
    assert detector.file_write == False



def test_set_high_voltage(detector):
    detector.high_voltage = 55
    assert detector.high_voltage == 55

def test_negative_voltage_raises(detector):
    with pytest.raises(DetectorValueError):
        detector.high_voltage = -5

def test_high_voltage_raises_on_to_high(detector):
    with pytest.raises(DetectorValueError):
        detector.high_voltage = 500



def test_get_image_size(detector):
    """Compares with the size in the config file"""
    assert detector.image_size.rows == config_test.image_size[0]
    assert detector.image_size.cols == config_test.image_size[1]

def test_get_module_geometry(detector):
    """Compares with the size in the config file"""
    assert detector.module_geometry.horizontal == config_test.module_geometry[0]
    assert detector.module_geometry.vertical == config_test.module_geometry[1]

def test_set_nframes(detector):
    detector.n_frames = 5
    assert detector.n_frames == 5

def test_negative_nframes_raises(detector):
    with pytest.raises(ValueError):
        detector.n_frames = -2

def test_nmodules(detector):
    """Assume that the number of modules should be the same as the number of hostnames"""
    assert detector.n_modules == len(config_test.known_hostnames)

def test_is_detector_online(detector):
    assert detector.online == True

def test_set_online(detector):
    detector.online = False
    assert detector.online == False
    detector.online = True
    assert detector.online == True

def test_last_client(detector):
    import socket
    myip = socket.gethostbyname_ex(socket.gethostname())[-1][0] #We probably should check for multiple ip
    assert detector.last_client_ip == myip

def test_receiver_is_online(detector):
    assert detector.receiver_online == True

def test_set_receiver_online(detector):
    detector.receiver_online = False
    assert detector.receiver_online == False
    detector.receiver_online = True
    assert detector.receiver_online == True

def test_set_receiver_online_raises_on_non_bool(detector):
    with pytest.raises(TypeError):
        detector.receiver_online = 'probably not this'

def test_set_period(detector):
    detector.period = 5.123
    assert detector.period == 5.123


def test_get_receiver_hostname(detector):
    """Assume that the receiver are on the local computer"""
    import socket
    host = socket.gethostname().split('.')[0]
    assert detector.rx_hostname == host

def test_set_receiver_hostname(detector):
    import socket
    host = socket.gethostname().split('.')[0]
    phony_host = 'madeup'
    detector.rx_hostname = phony_host
    assert detector.rx_hostname == phony_host
    detector.rx_hostname = host
    assert detector.rx_hostname == host

def test_set_rx_zmqport_single_value(detector):
    detector.rx_zmqport = 35000
    assert detector.rx_zmqport == [35000, 35001, 35002, 35003]

def test_set_rx_zmqport_list(detector):
    detector.rx_zmqport = [37000, 38000]
    assert detector.rx_zmqport == [37000, 37001, 38000, 38001]

def test_set_timing_mode(detector):
    detector.timing_mode = 'trigger'
    assert detector.timing_mode == 'trigger'
    detector.timing_mode = 'auto'
    assert detector.timing_mode == 'auto'


#     def test_one_frame(self):
#         self.detector.exposure_time = 0.1
#         self.detector.n_frames = 1
#         self.detector.acq()
#         self.assertEqual(self.detector.frames_caught, 1)
#
#     def test_ten_single_frames(self):
#         self.detector.exposure_time = 0.1
#         self.detector.n_frames = 1
#         for i in range(10):
#             self.detector.acq()
#             self.assertEqual(self.detector.frames_caught, 1)
#
# if __name__ == '__main__':
#     unittest.main()

