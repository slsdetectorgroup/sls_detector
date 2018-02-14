
import pytest
import config_test
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
from sls_detector.detector import element_if_equal
from sls_detector.errors import DetectorValueError

from sls_detector import Detector
detector_type = Detector().detector_type
eigertest = pytest.mark.skipif(detector_type != 'Eiger', reason = 'Only valid for Eiger')

@pytest.fixture
def eiger():
    from sls_detector import Eiger
    return Eiger()

@eigertest
def test_load_config_file_eiger(eiger):
    """Load a settings file and assert all settings"""
    eiger.load_config(os.path.join(dir_path, 'test.config'))


    assert eiger.rx_tcpport == [1954, 1955]
    assert eiger.lock == False
    assert eiger.rx_udpport == [50010, 50011, 50004, 50005]
    assert eiger.rx_hostname == 'mpc2048'
    assert eiger.flipped_data_x[:] == [False, True]
    assert eiger.settings_path == config_test.settings_path
    assert eiger.file_path == config_test.file_path
    assert eiger.vthreshold == 1500
    assert element_if_equal(eiger.dacs.vtr[:]) == 4000
    assert eiger.dynamic_range == 32
    assert eiger.tengiga == False
    assert eiger.high_voltage == 150
    assert element_if_equal(eiger.dacs.iodelay[:]) == 660

@eigertest
def test_load_parameters_file_eiger(eiger):
    """Load a parametes file and assert the settings in the file"""
    eiger.load_parameters(os.path.join(dir_path, 'test.par'))
    assert element_if_equal(eiger.dacs.vrf[:]) == 3000
    assert eiger.vthreshold == 1800