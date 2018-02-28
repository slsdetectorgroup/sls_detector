#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python - sls
=============

"""
import os
import numpy as np
from collections import namedtuple, Iterable
from functools import partial

from _sls_detector import DetectorApi  # c++ api wrapping multiSlsDetector
from .decorators import error_handling
from .errors import DetectorError, DetectorValueError


def all_equal(mylist):
    """If all elements are equal return true otherwise false"""
    return all(x == mylist[0] for x in mylist)


def element_if_equal(mylist):
    """If all elements are equal return only one element"""
    if all_equal(mylist):
        if len(mylist) == 0:
            return None
        else:
            return mylist[0]
    else:
        return mylist


class DetectorProperty:
    """
    Class to access detector properties that should be indexed per item
    Used as base class for dacs etc.
    """
    def __init__(self, get_func, set_func, nmod_func, name):
        
        # functions to get and set the parameter
        self.get = get_func
        self.set = set_func
        self.get_nmod = nmod_func
        self.__name__ = name
        
    def __getitem__(self, key):
        if key == slice(None, None, None):
            return [self.get(i) for i in range(self.get_nmod())]
        elif isinstance(key, Iterable):
            return [self.get(k) for k in key]
        else:
            return self.get(key)        

    def __setitem__(self, key, value):
        """
        Set dacs either by slice, key or list. Supports values that can
        be iterated over.
        """
        
        if key == slice(None, None, None):
            if isinstance(value, (np.integer, int)):
                for i in range(self.get_nmod()):
                    self.set(i, value)
            elif isinstance(value, Iterable):
                for i in range(self.get_nmod()):
                    self.set(i, value[i])
            else:
                raise ValueError('Value should be int or np.integer not', type(value))

        elif isinstance(key, Iterable):
            if isinstance(value, Iterable):
                for k, v in zip(key, value):
                    self.set(k, v)

            elif isinstance(value, int):
                for k in key:
                    self.set(k, value)

        elif isinstance(key, int):
            self.set(key, value)

    def __repr__(self):
        s = ', '.join(str(v) for v in self[:])
        return '{}: [{}]'.format(self.__name__, s)


# noinspection PyProtectedMember
class Dac(DetectorProperty):
    """
    This class represents a dac on the detector. One instance handles all
    dacs with the same name for a multi detector instance.

    .. note ::

        This class is used to build up DetectorDacs and is in general
        not directly accessed to the user.


    """
    def __init__(self, name, low, high, default, detector):
        self.name = name
        self._detector = detector

        self.min_value = low
        self.max_value = high
        self.default = default

        # Local copy to avoid calling the detector class every time
        self.get_nmod = self._detector._api.getNumberOfDetectors

        # Bind functions to get and set the dac
        self.get = partial(self._detector._api.getDac, self.name)
        self.set = partial(self._detector._api.setDac, self.name)

    def __repr__(self):
        """String representation for a single dac in all modules"""
        r_str = ['{:10s}: '.format(self.name)]
        r_str += ['{:5d}, '.format(self.get(i)) for i in range(self.get_nmod())]
        return ''.join(r_str).strip(', ')


class Adc:
    def __init__(self, name, detector):
        self.name = name
        self._detector = detector
        self._n_modules = self._detector.n_modules
        # Bind functions to get and set the dac
        self.get = partial(self._detector._api.getAdc, self.name)

    def __getitem__(self, key):
        """
        Get dacs either by slice, key or list
        """
        if key == slice(None, None, None):
            return [self.get(i) / 1000 for i in range(self._n_modules)]
        elif isinstance(key, Iterable):
            return [self.get(k) / 1000 for k in key]
        else:
            return self.get(key) / 1000

    def __repr__(self):
        """String representation for a single adc in all modules"""
        degree_sign = u'\N{DEGREE SIGN}'
        r_str = ['{:14s}: '.format(self.name)]
        r_str += ['{:6.2f}{:s}C, '.format(self.get(i)/1000, degree_sign) for i in range(self._n_modules)]
        return ''.join(r_str).strip(', ')


class DetectorAdcs:
    """
    Interface to the ADCs on the readout board
    """
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield value

    def __repr__(self):
        return '\n'.join([str(t) for t in self])


class DetectorDacs:
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

    def __init__(self, detector):
        # We need to at least initially know which detector we are connected to
        self._detector = detector

        # Index to support iteration
        self._current = 0

        # Populate the dacs
        for _d in self._dacs:
            setattr(self, '_'+_d[0], Dac(*_d, detector))

    def __getattr__(self, name):
        return self.__getattribute__('_' + name)

    def __setattr__(self, name, value):
        if name in self._dacnames:
            return self.__getattribute__('_' + name).__setitem__(slice(None, None, None), value)
        else:
            super().__setattr__(name, value)

    def __next__(self):
        if self._current >= len(self._dacs):
            self._current = 0
            raise StopIteration
        else:
            self._current += 1
            return self.__getattr__(self._dacnames[self._current-1])

    def __iter__(self):
        return self

    def __repr__(self):
        r_str = ['========== DACS =========']
        r_str += [repr(dac) for dac in self]
        return '\n'.join(r_str)

    def get_asarray(self):
        """
        Read the dacs into a numpy array with dimensions [ndacs, nmodules]
        """
        dac_array = np.zeros((len(self._dacs), self._detector.n_modules))
        for i, _d in enumerate(self):
            dac_array[i, :] = _d[:]
        return dac_array

    def set_from_array(self, dac_array):
        """
        Set the dacs from an numpy array with dac values. [ndacs, nmodules]
        """
        dac_array = dac_array.astype(np.int)
        for i, _d in enumerate(self):
            _d[:] = dac_array[i]

    def set_default(self):
        """
        Set all dacs to their default values
        """
        for _d in self:
            _d[:] = _d.default
            
    def update_nmod(self):
        """
        Update the cached value of nmod, needs to be run after adding or 
        removing detectors
        """
        for _d in self:
            _d._n_modules = self._detector.n_modules


class Detector:
    """
    Base class used as interface with the slsDetectorSoftware. To control a specific detector use the
    derived classes such as Eiger and Jungfrau. Functions as an interface to the C++ API

    """

    _speed_names = {0: 'Full Speed', 1: 'Half Speed', 2: 'Quarter Speed', 3: 'Super Slow Speed'}
    _speed_int = {'Full Speed': 0, 'Half Speed': 1, 'Quarter Speed': 2, 'Super Slow Speed': 3}

    def __init__(self):
        # C++ API interfacing slsDetector and multiSlsDetector

        self._api = DetectorApi()

        self._flippeddatax = DetectorProperty(self._api.getFlippedDataX,
                                              self._api.setFlippedDataX,
                                              self._api.getNumberOfDetectors,
                                              'flippeddatax')
        self._flippeddatay = DetectorProperty(self._api.getFlippedDataY,
                                              self._api.setFlippedDataY,
                                              self._api.getNumberOfDetectors,
                                              'flippeddatay')
        try:
            self.online = True
            self.receiver_online = True
        except DetectorError:
            print('Waring cannot connect to detector')

    def __len__(self):
        return self._api.getNumberOfDetectors()
    
    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def acq(self):
        """
        Blocking command. Acquire the number of frames specified by frames, cycles etc.
        """
        self._api.acq()

    @property
    @error_handling
    def busy(self):
        """
        Checks the detector is acquiring. Can also be set but should only be used if the acquire fails and
        leaves the detector with busy == True

        .. note ::

            Only works when the measurement is launched using acquire, not with status start!

        Returns
        --------
        bool
            :py:obj:`True` if the detector is acquiring otherwise :py:obj:`False`

        Examples
        ----------

        d.busy
        >> True

        #If the detector is stuck
        d.busy = False


        """
        return self._api.getAcquiringFlag()

    @busy.setter
    @error_handling
    def busy(self, value):
        self._api.setAcquiringFlag(value)



    def clear_errors(self):
        """Clear the error mask for the detector. Used to reset after checking."""
        self._api.clearErrorMask()

    @property
    @error_handling
    def detector_number(self):
        """
        Get all detector numbers, return as list


        Examples
        ---------

        ::

            #for beb083 and beb098
            detector.detector_number
            >> [83, 98]

        """
        return [self._api.getDetectorNumber(i) for i in range(self.n_modules)]



    @property
    def detector_type(self):
        """
        list if the type is different otherwise string

        * Eiger
        * Jungfrau
        * etc.

        """
        return element_if_equal(self._api.getDetectorType())

    @property
    @error_handling
    def dynamic_range(self):
        """
        :obj:`int`: Dynamic range of the detector.

        +----+-------------+------------------------------+
        | dr |  max counts |    comments                  |
        +====+=============+==============================+
        | 4  |       15    |                              |
        +----+-------------+------------------------------+
        | 8  |      255    |                              |
        +----+-------------+------------------------------+
        |16  |     4095    | 12 bit internally            |
        +----+-------------+------------------------------+
        |32  |  4294967295 | Autosumming of 12 bit frames |
        +----+-------------+------------------------------+

        Raises
        -------
        ValueError
            If the dynamic range is not available in the detector


        """
        return self._api.getDynamicRange()

    @dynamic_range.setter
    @error_handling
    def dynamic_range(self, dr):
        if dr in self._detector_dynamic_range:
            self._api.setDynamicRange(dr)
            return
        else:
            raise DetectorValueError('Cannot set dynamic range to: {:d} availble options: '.format(dr),
                                    self._detector_dynamic_range)

    @property
    def error_mask(self):
        """Read the error mask from the slsDetectorSoftware"""
        return self._api.getErrorMask()
    
    @property
    def error_message(self):
        """Read the error message from the slsDetectorSoftware"""
        return self._api.getErrorMessage()

    @property
    @error_handling
    def exposure_time(self):
        """
        :obj:`double` Exposure time in [s] of a single frame.
        """
        return self._api.getExposureTime() / 1e9

    @exposure_time.setter
    @error_handling
    def exposure_time(self, t):
        ns_time = int(t * 1e9)
        if ns_time <= 0:
            raise DetectorValueError('Exposure time must be larger than 0')
        self._api.setExposureTime(ns_time)

    @property
    @error_handling
    def file_index(self):
        """
        :obj:`int` Index for frames and file names

        Raises
        -------
        ValueError
            If the user tries to set an index less than zero

        Examples
        ---------

        ::

            detector.file_index
            >> 0

            detector.file_index = 10
            detector.file_index
            >> 10


        """
        return self._api.getFileIndex()

    @file_index.setter
    @error_handling
    def file_index(self, i):
        if i < 0:
            raise ValueError('Index needs to be positive')
        self._api.setFileIndex(i)

    @property
    @error_handling
    def file_name(self):
        """
        :obj:`str`: Base file name for writing images

        Examples
        ---------

        ::

            detector.file_name
            >> 'run'

            detector.file_name = 'myrun'

            #For a single acquisition the detector now writes
            # myrun_master_0.raw
            # myrun_d0_0.raw
            # myrun_d1_0.raw
            # myrun_d2_0.raw
            # myrun_d3_0.raw


        """
        return self._api.getFileName()

    @file_name.setter
    @error_handling
    def file_name(self, fname):
        self._api.setFileName(fname)

    @property
    @error_handling
    def file_path(self):
        """
        :obj:`str`: Path where images are written

        Raises
        -------
        FileNotFoundError
            If path does not exists

        Examples
        --------

        ::

            detector.file_path
            >> '/path/to/files'

            detector.file_path = '/new/path/to/other/files'
        """
        return self._api.getFilePath()

    @file_path.setter
    @error_handling
    def file_path(self, path):
        if os.path.exists(path) is True:
            self._api.setFilePath(path)
        else:
            raise FileNotFoundError('File path does not exists')

    @property
    @error_handling
    def file_write(self):
        """
        :obj:`bool` If True write files to disk
        """
        return self._api.getFileWrite()

    @file_write.setter
    @error_handling
    def file_write(self, fwrite):
        self._api.setFileWrite(fwrite)

    @property
    @error_handling
    def firmware_version(self):
        """
        :py:obj:`int` Firmware version of the detector
        """
        return self._api.getFirmwareVersion()

    @property
    def flags(self):
        """Read and set flags. Accepts both single flag as
        string or list of flags.

        Raises
        --------
        RuntimeError
            If flag not recognized


        Examples
        ----------

        ::

            #Eiger
            detector.flags
            >> ['storeinram', 'parallel']

            detector.flags = 'nonparallel'
            detector.flags
            >> ['storeinram', 'nonparallel']

            detector.flags = ['continous', 'parallel']


        """
        return self._api.getReadoutFlags()

    @flags.setter
    def flags(self, flags):
        if isinstance(flags, str):
            self._api.setReadoutFlag(flags)
        elif isinstance(flags, Iterable):
            for f in flags:
                self._api.setReadoutFlag(f)

    @property
    def frames_caught(self):
        """
        Number of frames caught by the receiver. Can be used to check for
        package loss.
        """
        return self._api.getFramesCaughtByReceiver()

    def free_shared_memory(self):
        """
        Free the shared memory that contains the detector settings

        .. warning ::

            After doing this you can't access the detector until it is
            reconfigured

        """
        self._api.freeSharedMemory()

    @property
    def flipped_data_x(self):
        """Flips data on x axis. Set for eiger bottom modules"""
        return self._flippeddatax

    @property
    def flipped_data_y(self):
        """Flips data on y axis."""
        return self._flippeddatax

    @property
    @error_handling
    def high_voltage(self):
        """
        High voltage applied to the sensor
        """
        return self._api.getDac('vhighvoltage', -1)

    @high_voltage.setter
    @error_handling
    def high_voltage(self, voltage):
        voltage = int(voltage)
        if voltage < 0 or voltage > 200:
            raise DetectorValueError('High voltage {:d}V is out of range.  Should be between 0-200V'.format(voltage))
        self._api.setDac('vhighvoltage', -1, voltage)

    @property
    @error_handling
    def hostname(self):
        """
        :obj:`list` of :obj:`str`: hostnames of all connected detectors

        Examples
        ---------

        ::

            detector.hostname
            >> ['beb059', 'beb058']

        """
        _hm = self._api.getHostname()
        if _hm == '':
            return []
        return _hm.strip('+').split('+')

    @hostname.setter
    @error_handling
    def hostname(self, hn):
        if isinstance(hn, str):
            self._api.setHostname(hn)
        else:
            name = ''.join([''.join((h, '+')) for h in hn])
            self._api.setHostname(name)

    @property
    def image_size(self):
        """
        :py:obj:`collections.namedtuple` with the image size of the detector
        Also works setting using a normal tuple
        
        .. note ::
            
            Follows the normal convention in Python of (rows, cols)

        Examples
        ----------

        ::

            d.image_size = (512, 1024)

            d.image_size
            >> ImageSize(rows=512, cols=1024)

            d.image_size.rows
            >> 512

            d.image_size.cols
            >> 1024

        """
        size = namedtuple('ImageSize', ['rows', 'cols'])
        return size(*self._api.getImageSize())

    @image_size.setter
    @error_handling
    def image_size(self, size):
        self._api.setImageSize(*size)

    @error_handling
    def load_config(self, fname):
        """
        Load detector configuration from a configuration file

        Raises
        --------
        FileNotFoundError
            If the file does not exists

        """
        if os.path.isfile(fname):
            self._api.readConfigurationFile(fname)
        else:
            raise FileNotFoundError('Cannot find settings file')

    @error_handling
    def load_parameters(self, fname):
        """
        Setup detector by executing commands in a parameters file


        .. note ::

            If you are relying mainly on the Python API it is probably
            better to track the settings from Python. This function uses
            parameters stored in a text file and the command line commands.

        Raises
        --------
        FileNotFoundError
            If the file does not exists

        """
        if os.path.isfile(fname):
            self._api.readParametersFile(fname)
        else:
            raise FileNotFoundError('Cannot find parameters file')

    @error_handling
    def load_trimbits(self, fname, idet=-1):
        """
        Load trimbit file or files. Either called with detector number or -1
        to try to load detector specific trimbit files
        
        Parameters
        -----------
        fname:
            :py:obj:`str` Filename (including path) to the trimbit files
            
        idet 
            :py:obj:`int` Detector to load trimbits to, -1 for all
        
        
        ::
            
            #Assuming 500k consisting of beb049 and beb048
            # 0 is beb049
            # 1 is beb048
            
            #Load name.sn049 to beb049 and name.sn048 to beb048
            detector.load_trimbits('/path/to/dir/name')
            
            #Load one file to a specific detector
            detector.load_trimbits('/path/to/dir/name.sn049', 0)
        
        """
        self._api.loadTrimbitFile(fname, idet)

    @property
    @error_handling
    def lock(self):
        """Lock the detector to this client


        ::

            detector.lock = True

        """
        return self._api.getServerLock()

    @lock.setter
    def lock(self, value):
        self._api.setServerLock(value)

    @property
    @error_handling
    def lock_receiver(self):
        """Lock the receivers to this client

        ::

            detector.lock_receiver = True

        """

        return self._api.getReceiverLock()

    @lock_receiver.setter
    def lock_receiver(self, value):
        self._api.setReceiverLock(value)

    @property
    @error_handling
    def module_geometry(self):
        """
        :obj:`namedtuple` Geometry(horizontal=nx, vertical=ny)
         of the detector modules.

         Examples
         ---------

         ::

             detector.module_geometry
             >> Geometry(horizontal=1, vertical=2)

             detector.module_geometry.vertical
             >> 2

             detector.module_geometry[0]
             >> 1

        """
        _t = self._api.getDetectorGeometry()
        Geometry = namedtuple('Geometry', ['horizontal', 'vertical'])
        return Geometry(horizontal=_t[0], vertical=_t[1])

    @property
    @error_handling
    def n_frames(self):
        """
        :obj:`int` Number of frames per acquisition
        """
        return self._api.getNumberOfFrames()

    @n_frames.setter
    @error_handling
    def n_frames(self, n):
        if n >= 1:
            self._api.setNumberOfFrames(n)
        else:
            raise ValueError('Invalid value for n_frames: {:d}. Number of'\
                             ' frames should be an integer greater than 0'.format(n))

    @property
    @error_handling
    def n_cycles(self):
        """Number of cycles for the measurement (exp*n_frames)*n_cycles"""
        return self._api.getCycles()

    @n_cycles.setter
    @error_handling
    def n_cycles(self, n_cycles):
        if n_cycles > 0:
            self._api.setCycles(n_cycles)
        else:
            raise DetectorValueError('Number of cycles must be positive')

    @property
    @error_handling
    def n_measurements(self):
        """
        Number of times to repeat the programmed measurement.
        This is the outer most part. Real time operation is not
        guaranteed since this is software controlled.

        Examples
        ----------

        ::

            detector.n_frames = 1
            detector.n_cycles = 1
            detector.n_measurements = 3

            detector.acq() # 1 frame 3 times

            detector.n_frames = 5
            detector.n_cycles = 3
            detector.n_measurements = 2

            detector.acq() # 5x3 frames 2 times total 30 frames

        """
        return self._api.getNumberOfMeasurements()

    @n_measurements.setter
    @error_handling
    def n_measurements(self, value):
        self._api.setNumberOfMeasurements(value)

    @property
    @error_handling
    def n_modules(self):
        """
        :obj:`int` Number of (half)modules in the detector

        Examples
        ---------

        ::

            detector.n_modules
            >> 2

        """
        return self._api.getNumberOfDetectors()

    @property
    @error_handling
    def online(self):
        """Online flag for the detector
        
        Examples
        ----------
        
        ::
            
            d.online 
            >> False
            
            d.online = True
        
        """
        return self._api.getOnline()
    
    @online.setter
    @error_handling
    def online(self, value):
        self._api.setOnline(value)

    @property
    @error_handling
    def last_client_ip(self):
        """Returns the ip address of the last client
        that accessed the detector

        Returns
        -------

        :obj:`str` last client ip

        Examples
        ----------

        ::

            detector.last_client_ip
            >> '129.129.202.117'

        """
        return self._api.getLastClientIP()

    @property
    @error_handling
    def receiver_online(self):
        """
        Online flag for the receiver. Is set together with detector.online when creating the detector object

        Examples
        ---------

        ::

            d.receiver_online
            >> True

            d.receiver_online = False

        """
        return self._api.getReceiverOnline()
    
    @receiver_online.setter
    @error_handling
    def receiver_online(self, value):
        self._api.setReceiverOnline(value)

    def reset_frames_caught(self):
        """
        Reset the number of frames caught by the receiver. 
        
        .. note ::
            
            Automatically done when using d.acq()
            
            
        """
        self._api.resetFramesCaught()

    @property
    @error_handling
    def period(self):
        """
        :obj:`double` Period between start of frames. Set to 0 for the detector
        to choose the shortest possible
        """
        _t = self._api.getPeriod()
        return _t / 1e9

    @period.setter
    @error_handling
    def period(self, t):
        ns_time = int(t * 1e9)
        if ns_time < 0:
            raise ValueError('Period must be 0 or larger')
        self._api.setPeriod(ns_time)

    @property
    @error_handling
    def rate_correction(self):
        """
        :obj:`list` of :obj:`double` Rate correction for all modules.
        Set to 0 for **disabled**

        .. todo ::

            Should support individual assignments

        Raises
        -------
        ValueError
            If the passed list is not of the same length as the number of
            detectors

        Examples
        ---------

        ::

            detector.rate_correction
            >> [125.0, 155.0]

            detector.rate_correction = [125, 155]


        """
        return self._api.getRateCorrection()

    @rate_correction.setter
    @error_handling
    def rate_correction(self, tau_list):
        if len(tau_list) != self.n_modules:
            raise ValueError('List of tau needs the same length')
        self._api.setRateCorrection(tau_list)

    @property
    @error_handling
    def readout_clock(self):
        """
        Speed of the readout clock relative to the full speed

        * Full Speed
        * Half Speed
        * Quarter Speed
        * Super Slow Speed

        Examples
        ---------

        ::

            d.readout_clock
            >> 'Half Speed'

            d.readout_clock = 'Full Speed'


        """
        speed = self._api.getReadoutClockSpeed()
        return self._speed_names[speed]

    @readout_clock.setter
    @error_handling
    def readout_clock(self, value):
        speed = self._speed_int[value]
        self._api.setReadoutClockSpeed(speed)

    @property
    def receiver_frame_index(self):
        return self._api.getReceiverCurrentFrameIndex()

    @property
    @error_handling
    def rx_datastream(self):
        """
        Zmq datastream from receiver. :py:obj:`True` if enabled and :py:obj:`False`
        otherwise
        
        ::
            
            #Enable data streaming from receiver
            detector.rx_datastream = True
            
            #Check data streaming
            detector.rx_datastream
            >> True
            
        """
        return self._api.getRxDataStreamStatus()

    @rx_datastream.setter
    def rx_datastream(self, status):
        self._api.setRxDataStreamStatus(status)

    @property
    @error_handling
    def rx_hostname(self):
        s = self._api.getNetworkParameter('rx_hostname')
        return element_if_equal(s)
            
    @property
    @error_handling
    def rx_udpip(self):
        s = self._api.getNetworkParameter('rx_udpip')
        return element_if_equal(s)

    @rx_udpip.setter
    def rx_udpip(self, ip):
        if isinstance(ip, list):
            for i, addr in enumerate(ip):
                self._api.setNetworkParameter('rx_udpip', addr, i)
        else:
            self._api.setNetworkParameter('rx_udpip', ip, -1)
    
    @rx_hostname.setter
    @error_handling
    def rx_hostname(self, names):
        # if we pass a list join the list
        if isinstance(names, list):
            names = '+'.join(n for n in names)+'+'

        self._api.setNetworkParameter('rx_hostname', names, -1)

    @property
    def rx_udpmac(self):
        return element_if_equal(self._api.getNetworkParameter('rx_udpmac'))

    @rx_udpmac.setter
    def rx_udpmac(self, mac):
        if isinstance(mac, list):
            for i, m in enumerate(mac):
                self._api.setNetworkParameter('rx_udpmac', m, i)
        else:
            self._api.setNetworkParameter('rx_udpmac', mac, -1)

    @property
    @error_handling
    def rx_tcpport(self):
        return [self._api.getRxTcpport(i) for i in range(self.n_modules)]

    @rx_tcpport.setter
    @error_handling
    def rx_tcpport(self, ports):
        if len(ports) != len(self):
            raise ValueError('Number of ports: {} not equal to number of '
                             'detectors: {}'.format(len(ports), len(self)))
        else:
            for i, p in enumerate(ports):
                self._api.setRxTcpport(i, p)

    @property
    @error_handling
    def rx_zmqip(self):
        """
        .. todo ::

            also set
        """
        ip = self._api.getNetworkParameter('rx_zmqip')
        return element_if_equal(ip)

    @property
    @error_handling
    def rx_zmqport(self):
        """
        Return the receiver zmq ports.
        
        ::
            
            detector.rx_zmqport
            >> [30001, 30002]
            



        """
        _s = self._api.getNetworkParameter('rx_zmqport')
        if _s == '':
            return []
        else:
            return [int(_p) for _p in _s]

    @rx_zmqport.setter
    @error_handling
    def rx_zmqport(self, port):
        if isinstance(port, Iterable):
            for i, p in enumerate(port):
                self._api.setNetworkParameter('rx_zmqport', str(p), i)
        else:
            self._api.setNetworkParameter('rx_zmqport', str(port), -1)

# Add back when versioning is defined
#    @property
#    def software_version(self):
#        return self._api.getSoftwareVersion();

#    case STANDARD:      return string("standard");		\
#    case FAST:      	return string("fast");			\
#    case HIGHGAIN:      return string("highgain");		\
#    case DYNAMICGAIN:   return string("dynamicgain");	\
#    case LOWGAIN:    	return string("lowgain");		\
#    case MEDIUMGAIN:    return string("mediumgain");	\
#    case VERYHIGHGAIN:  return string("veryhighgain");	\
#    case LOWNOISE:      return  string("lownoise");		\
#    case DYNAMICHG0:    return  string("dynamichg0");	\
#    case FIXGAIN1:      return  string("fixgain1");		\
#    case FIXGAIN2:      return  string("fixgain2");		\
#    case FORCESWITCHG1: return  string("forceswitchg1");\
#    case FORCESWITCHG2: return  string("forceswitchg2");\
#    case VERYLOWGAIN: return  string("verylowgain");\
#    default:    		return string("undefined");

    @property
    @error_handling
    def settings(self):
        """
        Detector settings used to control for example calibration or gain
        switching. For EIGER almost always standard
        
        .. todo::
            
            check input depending on detector
        
        """
        return self._api.getSettings()
        
    @settings.setter
    @error_handling
    def settings(self, s):
        # check input!
        self._api.setSettings(s)
        
    @property
    @error_handling
    def settings_path(self):
        """
        The path where the slsDetectorSoftware looks for settings/trimbit files            
        """
        return self._api.getSettingsDir()
    
    @settings_path.setter
    @error_handling
    def settings_path(self, path):
        if os.path.isdir(path):
            self._api.setSettingsDir(path)
        else:
            raise FileNotFoundError('Settings path does not exist')

    @property
    @error_handling
    def status(self):
        """
        :py:obj:`str` Status of the detector: idle, running,

        .. todo ::

            Check possible values


        """
        return self._api.getRunStatus()

    def start_detector(self):
        """
        Non blocking command to star acquisition. Needs to be used in combination
        with receiver start.
        """
        self._api.startAcquisition()

    def stop_detector(self):
        """
        Stop acquisition early or if the detector hangs
        """
        self._api.stopAcquisition()

    def start_receiver(self):
        self._api.startReceiver()
        
    def stop_receiver(self):
        self._api.stopReceiver()

    @property
    def sub_exposure_time(self):
        """
        Sub frame exposure time in *seconds* for Eiger in 32bit autosumming mode

        ::

            d.sub_exposure_time
            >> 0.0023

            d.sub_exposure_time = 0.002

        """
        return self._api.getSubExposureTime() / 1e9

    @sub_exposure_time.setter
    def sub_exposure_time(self, t):
        ns_time = int(t * 1e9)
        if ns_time > 0:
            self._api.setSubExposureTime(ns_time)
        else:
            raise ValueError('Sub exposure time must be larger than 0')

    @property
    def threaded(self):
        """
        Enable parallel execution of commands to the different detector modules

        Examples
        ----------

        ::

            d.threaded
            >> True

            d.threaded = False

        """
        return self._api.getThreadedProcessing()
    
    @threaded.setter
    def threaded(self, value):
        self._api.setThreadedProcessing(value)

    @property
    @error_handling
    def threshold(self):
        """
        Detector threshold in eV
        """
        return self._api.getThresholdEnergy()
        
    @threshold.setter
    @error_handling
    def threshold(self, eV):
        self._api.setThresholdEnergy(eV)

    @property
    def timing_mode(self):
        """
        :py:obj:`str` Timing mode of the detector

        * **auto** Something
        * **trigger** Something else


        """
        return self._api.getTimingMode()

    @timing_mode.setter
    def timing_mode(self, mode):
        self._api.setTimingMode(mode)

    @property
    def trimmed_energies(self):
        """
        EIGER: the energies at which the detector was trimmed. This also sets
        the range for which the calibration of the detector is valid.
        
            
        ::
            
            detector.trimmed_energies = [5400, 6400, 8000]
            
            detector.trimmed_energies
            >> [5400, 6400, 8000]
        
        """
        
        return self._api.getTrimEnergies()
    
    @trimmed_energies.setter
    def trimmed_energies(self, energy_list):
        self._api.setTrimEnergies(energy_list)

    @property
    def vthreshold(self):
        """
        Threshold in DAC units for the detector. Sets the individual vcmp of 
        all chips in the detector.
        """
        return self._api.getDac('vthreshold', -1)

    @vthreshold.setter
    def vthreshold(self, th):
        self._api.setDac('vthreshold', -1, th)

    @property
    def trimbits(self):
        """
        Set or read trimbits of the detector.

        Examples
        ---------

        ::

            #Set all to 32
            d.trimbits = 32

            d.trimbits
            >> 32

            #if undefined or different
            d.trimbits
            >> -1

        """
        return self._api.getAllTrimbits()

    @trimbits.setter
    def trimbits(self, value):
        if self._trimbit_limits.min <= value <= self._trimbit_limits.max:
            self._api.setAllTrimbits(value)
        else:
            raise DetectorValueError('Trimbit setting {:d} is  outside of range:'\
                             '{:d}-{:d}'.format(value, self._trimbit_limits.min, self._trimbit_limits.max))

    @property
    def client_zmqport(self):
        """zmq port of the client"""
        _s = self._api.getNetworkParameter('client_zmqport')
        if _s == '':
            return []
        return [int(_p)+i for _p in _s for i in range(2)]

    @error_handling
    def _provoke_error(self):
        self._api.setErrorMask(1)


def free_shared_memory():
    """
    Function to free the shared memory. After this
    we need to create a new detector object. 
    """
    d = Detector()
    d.free_shared_memory()
