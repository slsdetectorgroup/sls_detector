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

#
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

