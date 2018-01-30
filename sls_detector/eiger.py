#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:51:18 2017

@author: l_frojdh
"""

from functools import partial
from collections import namedtuple
import socket

from .detector import Detector, DetectorDacs, DetectorAdcs, Adc, DetectorProperty, element_if_equal
from .decorators import error_handling

class EigerVcmp:
    """
    Convenience class to be able to loop over vcmp for Eiger
    
    
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


class DetectorDelays:
    _delaynames = ['frame', 'left', 'right']
    def __init__(self, detector):
        #We need to at least initially know which detector we are connected to
        self._detector = detector
        
        setattr(self, '_frame', DetectorProperty(detector._api.getDelayFrame,
                                        detector._api.setDelayFrame,
                                        detector._api.getNumberOfDetectors,
                                        'frame'))

        setattr(self, '_left', DetectorProperty(detector._api.getDelayLeft,
                                        detector._api.setDelayLeft,
                                        detector._api.getNumberOfDetectors,
                                        'left'))

        setattr(self, '_right', DetectorProperty(detector._api.getDelayRight,
                                        detector._api.setDelayRight,
                                        detector._api.getNumberOfDetectors,
                                        'right'))
        #Index to support iteration
        self._current = 0

    def __getattr__(self, name):
        return self.__getattribute__('_' + name)


    def __setattr__(self, name, value):
        if name in self._delaynames:
            return self.__getattribute__('_' + name).__setitem__(slice(None, None, None), value)
        else:
            super().__setattr__(name, value)

    def __next__(self):
        if self._current >= len(self._delaynames):
            self._current = 0
            raise StopIteration
        else:
            self._current += 1
            return self.__getattr__(self._delaynames[self._current-1])

    def __iter__(self):
        return self

    def __repr__(self):
        hn = self._detector.hostname
        r_str = ['Transmission delay [ns]\n'
                 '{:11s}{:>8s}{:>8s}{:>8s}'.format('', 'left', 'right', 'frame')]
        for i in range(self._detector.n_modules):
            r_str.append( '{:2d}:{:8s}{:>8d}{:>8d}{:>8d}'.format(i, hn[i], self.left[i], self.right[i], self.frame[i]))
        return '\n'.join(r_str)


class Eiger(Detector):
    """
    Subclassing Detector to set up correct dacs and detector specific 
    functions. 
    """
    _detector_dynamic_range = [4, 8, 16, 32]
    
    def __init__(self):
        #Init on base calss
        super().__init__()
        
        self._vcmp = EigerVcmp(self)
        self._dacs = EigerDacs(self)
        self._trimbit_limits = namedtuple('trimbit_limits', ['min', 'max'])(0,63)
        self._delay = DetectorDelays(self)
        
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
   

    @property
    @error_handling
    def active(self):
        """
        Is the detector active? Can be used to enable or disable a detector
        module
        
        Examples
        ----------
        
        ::
            
            d.active
            >> active: [True, True]
            
            d.active[1] = False
            >> active: [True, False]
        """
        return self._active
    
    @active.setter
    @error_handling
    def active(self, value):
        self._active[:] = value

#   Currently only supported in the developer branch of sls
#
#    @property
#    @error_handling
#    def add_gappixels(self):
#        """Enable or disable the (virual) pixels between ASICs
#        
#        Examples
#        ----------
#        
#        ::
#            
#            d.add_gappixels = True
#            
#            d.add_gappixels
#            >> True
#        
#        """
#        return self._api.getGapPixels()
#    
#    @add_gappixels.setter
#    @error_handling
#    def add_gappixels(self, value):
#        self._api.setGapPixels(value)



    @property
    @error_handling
    def delay(self):
        """
        Transmission delay of the modules to allow running the detector
        in a network not supporting the full speed of the detector.


        ::
            
            d.delay
            >>
            Transmission delay [ns]
                           left   right   frame
             0:beb048         0   15000       0
             1:beb049       100  190000     100
             
             d.delay.left = [2000,5000]
        """
        return self._delay

        
    def default_settings(self):
        """
        reset the detector to some type of standard settings
        """
        
        self.n_frames = 1
        self.exposure_time = 1
        self.period = 0
        self.dynamic_range = 16

    @property
    @error_handling
    def eiger_matrix_reset(self):
        """
        Matrix reset bit for Eiger.

        :py:obj:`True` : Normal operation, the matrix is reset before each acq.
        :py:obj:`False` : Matrix reset disabled. Used to not reset before
        reading out analog test pulses.
        """
        return self._api.getCounterBit()

    @eiger_matrix_reset.setter
    @error_handling
    def eiger_matrix_reset(self, value):
        self._api.setCounterBit(value)


    @property
    @error_handling
    def flowcontrol_10g(self):
        """
        :py:obj:`True` - Flow control enabled :py:obj:`False` flow control disabled.
        Sets for all moduels, if for some reason access to a single module is needed
        this can be done trough the C++ API.

        """
        fc = self._api.getNetworkParameter('flow_control_10g')
        return element_if_equal([bool(int(e)) for e in fc])

    @flowcontrol_10g.setter
    @error_handling
    def flowcontrol_10g(self, value):
        if value is True:
            v = '1'
        else:
            v = '0'
        self._api.setNetworkParameter('flow_control_10g', v, -1)

    @error_handling
    def pulse_all_pixels(self, n):
        """
        Pulse each pixel of the chip **n** times using the analog test pulses.
        The pulse height is set using d.dacs.vcall with 4000 being 0 and 0 being
        the highest pulse.
        
        ::
            
            #Pulse all pixels ten times
            d.pulse_all_pixels(10)
            
            #Avoid resetting before acq
            d.eiger_matrix_reset = False
            
            d.acq() #take frame
            
            #Restore normal behaviour
            d.eiger_matrix_reset = True
        
        
        """
        self._api.pulseAllPixels(n)
        
    @error_handling
    def pulse_diagonal(self, n):
        """
        Unsed for calibraiton
        """
        self._api.pulseDiagonal(n)

    @error_handling
    def pulse_chip(self, n):
        """
        Advance the counter by toggling enable. Gives 2*n+2 int the counter
        
        """
        n = int(n)
        if n>=-1:
            self._api.pulseChip(n)
        else:
            raise ValueError('n must be equal or larger than -1')


    @property
    def vcmp(self):
        """
        Convenience function to get and set the individual vcmp of chips
        Used mainly in the calibration code.

        Examples
        ---------

        ::

            #Reading
            d.vcmp[:]
            >> [500, 500, 500, 500, 500, 500, 500, 500]

            #Setting
            d.vcmp = [500, 500, 500, 500, 500, 500, 500, 500]


        """

        return self._vcmp
    
    @vcmp.setter
    @error_handling
    def vcmp(self, values):
        if len(values)==len(self._vcmp.set):
            for i,v in enumerate(values):
                self._vcmp.set[i](v)
        else:
            raise ValueError('vcmp only compatible with setting all')


     
    @property
    @error_handling
    def rx_udpport(self):
        """
        UDP port for the receiver. Each module has two ports referred to
        as rx_udpport and rx_udpport2 in the command line interface
        here they are grouped for each detector
        
        ::
            
            [0:rx_udpport, 0:rx_udpport2, 1:rx_udpport ...]
        
        Examples
        -----------
        
        ::
        
            d.rx_udpport
            >> [50010, 50011, 50004, 50005]
            
            d.rx_udpport = [50010, 50011, 50012, 50013]
        
        """
        p0 = self._api.getNetworkParameter('rx_udpport')
        p1 = self._api.getNetworkParameter('rx_udpport2')
        return [int(val) for pair in zip(p0,p1) for val in pair]
    
    @rx_udpport.setter
    @error_handling
    def rx_udpport(self, ports):
        #Iterable with port numbers
        p0 = '+'.join(str(p) for p in ports[0::2])+'+'
        p1 = '+'.join(str(p) for p in ports[1::2])+'+'
#        print(p0,p1)
        self._api.setNetworkParameter('rx_udpport', p0)
        self._api.setNetworkParameter('rx_udpport2', p1)

    @property
    @error_handling
    def tengiga(self):
        """Enable 10Gbit/s data output
        
        Examples
        ----------
        
        ::
            
            d.tengiga
            >> False
            
            d.tengiga = True
            
        """
        return self._api.getTenGigabitEthernet()
    
    @tengiga.setter
    @error_handling
    def tengiga(self, value):
        self._api.setTenGigabitEthernet(value)
        
    def setup500k(self, hostnames):
        """
        Setup the Eiger detector to run on the local machine
        """
        
        self.hostname = hostnames
        self.image_size = (512,1024)
        self.rx_tcpport = [1954,1955]
        self.rx_udpport = [50010, 50011, 50004, 50005]
        self.rx_hostname = socket.gethostname().split('.')[0]
        self.rx_datastream = False
        self.file_write = False
        self.online = True
        self.receiver_online = True
        