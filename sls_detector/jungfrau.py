#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:51:18 2017

@author: l_frojdh
"""

from functools import partial
from collections import namedtuple

from .detector import Detector, DetectorDacs, DetectorAdcs, Adc


class Register:
    def __init__(self, detector):
        self._detector = detector
        
    def __getitem__(self, key):
        return hex(self._detector._api.readRegister(key))
    def __setitem__(self, key, value):
        self._detector._api.writeRegister(key, value)

class JungfrauDacs(DetectorDacs):
    _dacs = [('vb_comp',    0, 4000,    1220),
             ('vdd_prot',   0, 4000,    3000),
             ('vin_com',    0, 4000,    1053),
             ('vref_prech', 0, 4000,    1450),
             ('vb_pixbuff', 0, 4000,     750),
             ('vb_ds',      0, 4000,    1000),
             ('vref_ds',    0, 4000,     480),
             ('vref_comp',  0, 4000,     420),
             ]
    _dacnames = [_d[0] for _d in _dacs]
    


class Jungfrau(Detector):
    """
    Right dacs, etc.
    """
    _detector_dynamic_range = [4, 8, 16, 32]
    
    def __init__(self):
        #Init on base calss
        super().__init__()
        

        self._dacs = JungfrauDacs(self)
        
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
        

        self.register = Register(self)
        
    @property
    def power_chip(self):
        return self._api.isChipPowered()
    
    @power_chip.setter
    def power_chip(self, value):
        return self._api.powerChip(value)