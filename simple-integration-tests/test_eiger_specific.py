import pytest
import config_test

from sls_detector.errors import DetectorValueError

from sls_detector import Detector
detector_type = Detector().detector_type
eigertest = pytest.mark.skipif(detector_type != 'Eiger', reason = 'Only valid for Eiger')

@pytest.fixture
def detector():
    from sls_detector import Detector
    d = Detector()
    return d

@pytest.fixture
def eiger():
    from sls_detector import Eiger
    return Eiger()

@eigertest
def test_set_subexptime(eiger):
    eiger.sub_exposure_time = 0.0025
    assert eiger.sub_exposure_time == 0.0025

@eigertest
def test_set_matrix_reset(eiger):
    eiger.eiger_matrix_reset = False
    assert eiger.eiger_matrix_reset == False
    eiger.eiger_matrix_reset = True
    assert eiger.eiger_matrix_reset == True