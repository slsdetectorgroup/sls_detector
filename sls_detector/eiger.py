#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:51:18 2017

@author: l_frojdh
"""

from functools import partial
from collections import namedtuple

from .detector import Detector, DetectorDacs, DetectorAdcs, Adc


class EigerVcmp:
    """
    Convenience class to be able to loop over vcmp for eiger
    
    
    .. todo::
        
        Support single assignment and perhaps unify with Dac class
    
    """
    
    def __init__(self, detector):
        _names = ['vcmp_ll',
              'vcmp_lr',
              'vcmp_rl',
              'vcmp_rr']
        self.set = []
        self.get = []
        for i in range(detector.n_modules):
            if i%2 == 0:
                name = _names
            else:
                name = _names[::-1]
            for n in name:
                self.set.append( partial(detector._api.setDac, n, i ))
                self.get.append( partial(detector._api.getDac, n, i ))
    
    def __getitem__(self, key):
        if key == slice(None, None, None):
            return [_d() for _d in self.get]
        return self.get[key]()
    
    def __setitem__(self, i, value):
        self.set[i](value)


class EigerDacs(DetectorDacs):
    _dacs = [('vsvp',    0, 4000,    0),
             ('vtr',     0, 4000, 2500),
             ('vrf',     0, 4000, 3300),
             ('vrs',     0, 4000, 1400),
             ('vsvn',    0, 4000, 4000),
             ('vtgstv',  0, 4000, 2556),
             ('vcmp_ll', 0, 4000, 1500),
             ('vcmp_lr', 0, 4000, 1500),
             ('vcall',   0, 4000, 4000),
             ('vcmp_rl', 0, 4000, 1500),
             ('rxb_rb',  0, 4000, 1100),
             ('rxb_lb',  0, 4000, 1100),
             ('vcmp_rr', 0, 4000, 1500),
             ('vcp',     0, 4000,  200),
             ('vcn',     0, 4000, 2000),
             ('vis',     0, 4000, 1550),
             ('iodelay', 0, 4000,  660)]
    _dacnames = [_d[0] for _d in _dacs]

class Eiger(Detector):
    """
    Right dacs, etc.
    """
    _detector_dynamic_range = [4, 8, 16, 32]
    
    def __init__(self):
        #Init on base calss
        super().__init__()
        
        self._vcmp = EigerVcmp(self)
        self._dacs = EigerDacs(self)
        self._trimbit_limits = namedtuple('trimbit_limits', ['min', 'max'])(0,63)
        
        #Eiger specific adcs
        self._temp = DetectorAdcs()
        self._temp.fpga = Adc('temp_fpga', self)
        self._temp.fpgaext = Adc('temp_fpgaext', self)
        self._temp.t10ge = Adc('temp_10ge', self)
        self._temp.dcdc = Adc('temp_dcdc', self)
        self._temp.sodl = Adc('temp_sodl', self)
        self._temp.sodr = Adc('temp_sodr', self)
        self._temp.fpgafl = Adc('temp_fpgafl', self)
        self._temp.fpgafr = Adc('temp_fpgafr', self)
        

        