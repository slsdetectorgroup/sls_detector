#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing setting dynamic range for Eiger. If the detector is not Eiger the tests are skipped
"""
import pytest
import config_test
from fixtures import detector, eiger, jungfrau, eigertest, jungfrautest
from sls_detector.errors import DetectorValueError


@eigertest
def test_set_dynamic_range(eiger):
    for dr in [4,8,16,32]:
        eiger.dynamic_range = dr
        assert eiger.dynamic_range == dr
@eigertest
def test_set_dynamic_range_raises(eiger):
    with pytest.raises(DetectorValueError):
        eiger.dynamic_range = 75



