#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:51:18 2017

@author: l_frojdh
"""

from functools import partial
from collections import namedtuple

from .detector import Detector, DetectorDacs, DetectorAdcs, Adc
from .decorators import error_handling

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

        self._register = Register(self)
        
    @property
    @error_handling
    def power_chip(self):
        return self._api.isChipPowered()
    
    @power_chip.setter
    @error_handling
    def power_chip(self, value):
        return self._api.powerChip(value)


    @property
    @error_handling
    def delay(self):
        return self._api.getDelay()/1e9

    @delay.setter
    @error_handling
    def delay(self, t):
        ns_time = int(t * 1e9)
        self._api.setDelay(ns_time)

    @property
    @error_handling
    def n_gates(self):
        return self._api.getNumberOfGates()

    @n_gates.setter
    @error_handling
    def n_gates(self, n):
        self._api.setNumberOfGates()

    @property
    @error_handling
    def n_probes(self):
        return self._api.getNumberOfProbes()

    @n_gates.setter
    @error_handling
    def n_probes(self, n):
        self._api.setNumberOfProbes()

    @property
    def temperature_threshold(self):
        return self._api.getThresholdTemperature()

    @temperature_threshold.setter
    def temperature_threshold(self, t):
        self._api.setThresholdTemperature(t)

    @property
    def temperature_control(self):
        return self._api.getTemperatureControl()

    @temperature_control.setter
    def temperature_control(self, v):
        self._api.setTemperatureControl(v)

    @property
    def temperature_event(self):
        return self._api.getTemperatureEvent()

    def reset_temperature_event(self):
        self._api.resetTemperatureEvent()

    @property
    @error_handling
    def register(self):
        """Directly manipulate registers on the readout board
        
        Examples
        ---------
        
        ::
            
            d.register[0x5d] = 0xf00
        
        """
        
        
        return self._register