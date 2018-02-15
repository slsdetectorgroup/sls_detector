import pytest

from sls_detector import Detector

@pytest.fixture
def detector():
    from sls_detector import Detector
    return Detector()

@pytest.fixture
def eiger():
    from sls_detector import Eiger
    return Eiger()


detector_type = Detector().detector_type
eigertest = pytest.mark.skipif(detector_type != 'Eiger', reason = 'Only valid for Eiger')
