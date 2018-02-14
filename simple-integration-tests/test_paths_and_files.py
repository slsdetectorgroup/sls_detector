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
def test_set_path(eiger, tmpdir):
    import os
    path = os.path.join(tmpdir.dirname, tmpdir.basename)
    eiger.file_path = path
    assert eiger.file_path == path

@eigertest
def test_set_path_and_write_files(eiger, tmpdir):
    import os
    prefix = 'testprefix'
    path = os.path.join(tmpdir.dirname, tmpdir.basename)
    eiger.file_path = path
    eiger.file_write = True
    eiger.exposure_time = 0.1
    eiger.n_frames = 1
    eiger.timing_mode = 'auto'
    eiger.file_name = prefix
    eiger.file_index = 0
    eiger.acq()

    files = [f.basename for f in tmpdir.listdir()]

    assert len(files) == 5
    assert (prefix+'_d0_0.raw' in files) == True
    assert (prefix+'_d1_0.raw' in files) == True
    assert (prefix+'_d2_0.raw' in files) == True
    assert (prefix+'_d3_0.raw' in files) == True