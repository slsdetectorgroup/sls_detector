#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python - sls
=============

"""
import os
from collections import namedtuple, Iterable
from functools import partial
import numpy as np
from _sls_detector import DetectorApi # c++ api wrapping multiSlsDetector



class Dac:
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

        #Local copy to avoid calling the detector class every time
        self._n_modules = self._detector.n_modules

        #Bind functions to get and set the dac
        self.get = partial(self._detector._api.getDac, self.name)
        self.set = partial(self._detector._api.setDac, self.name)

    def __getitem__(self, key):
        """
        Get dacs either by slice, key or list
        """
        if key == slice(None, None, None):
            return [self.get(i) for i in range(self._n_modules)]
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
            if isinstance(value, int):
                for i in range(self._n_modules):
                    self.set(i, value)
            elif isinstance(value, Iterable):
                for i in range(self._n_modules):
                    self.set(i, value[i])

        elif isinstance(key, Iterable):
            if isinstance(value, Iterable):
                for k,v in zip(key, value):
                    self.set(k,v)

            elif isinstance(value, int):
                for k in key:
                    self.set(k, value)


        elif isinstance(key, int):
            self.set(key, value)

    def __repr__(self):
        """String representation for a single dac in all modules"""
        r_str = ['{:10s}: '.format(self.name)]
        r_str += [ '{:5d}, '.format(self.get(i)) for i in range(self._n_modules)]
        return ''.join(r_str).strip(', ')

class Adc:
    def __init__(self, name, detector):
        self.name = name
        self._detector = detector
        self._n_modules = self._detector.n_modules
        #Bind functions to get and set the dac
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
        degree_sign= u'\N{DEGREE SIGN}'
        r_str = ['{:14s}: '.format(self.name)]
        r_str += [ '{:6.2f}{:s}C, '.format(self.get(i)/1000, degree_sign) for i in range(self._n_modules)]
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
        #We need to at least initially know which detector we are connected to
        self._detector = detector

        #Index to support iteration
        self._current = 0

        #Popolate the dacs
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
            dac_array[i,:] = _d[:]
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


class Detector:
    """
    Python class that is used for controlling an sls detector.

    """
    _detector_dynamic_range = [4, 8, 16, 32]
    _speed_names = {0: 'Full Speed', 1: 'Half Speed', 2: 'Quarter Speed', 3: 'Super Slow Speed'}
    _speed_int = {'Full Speed': 0, 'Half Speed': 1, 'Quarter Speed': 2, 'Super Slow Speed': 3}
    def __init__(self):
        self._api = DetectorApi()

        self._dacs = DetectorDacs(self)
        """dacs = :py:sls`DetectorDacs`"""

        self._trimbit_limits = namedtuple('trimbit_limits', ['min', 'max'])(0,63)


        self._temp = DetectorAdcs()
        self._temp.fpga = Adc('temp_fpga', self)
        self._temp.fpgaext = Adc('temp_fpgaext', self)
        self._temp.t10ge = Adc('temp_10ge', self)
        self._temp.dcdc = Adc('temp_dcdc', self)
        self._temp.sodl = Adc('temp_sodl', self)
        self._temp.sodr = Adc('temp_sodr', self)
        self._temp.fpgafl = Adc('temp_fpgafl', self)
        self._temp.fpgafr = Adc('temp_fpgafr', self)

    def __len__(self):
        return self._api.getNumberOfDetectors()



    def acq(self):
        """
        Issue an aquire command to start the measurement
        """
        self._api.acq()


    @property
    def busy(self):
        """
        Checks the acquire flag of the detector.

        Returns
        --------
        bool
            :py:obj:`True` if the detector is acqiring otherwise :py:obj:`False`


        """
        return self._api.getAcquiringFlag()

    @property
    def temp(self):
        """
        An instance of DetectorAdcs used to read the temperature
        of different components
        
        Examples
        -----------
        
        :: 
            
            detector.temp
            >>
            temp_fpga     :  36.90°C,  45.60°C
            temp_fpgaext  :  31.50°C,  32.50°C
            temp_10ge     :   0.00°C,   0.00°C
            temp_dcdc     :  36.00°C,  36.00°C
            temp_sodl     :  33.00°C,  34.50°C
            temp_sodr     :  33.50°C,  34.00°C
            temp_fpgafl   :  33.81°C,  30.93°C
            temp_fpgafr   :  27.88°C,  29.15°C
        
            a = detector.temp_fpga[:]
            a
            >> [36.568, 45.542]
            
        
        """
        return self._temp

    @property
    def dacs(self):
        """

        An instance of DetectorDacs used for accessing the dacs of a single
        or multi detector.

        Examples
        ---------

        ::

            d = sls.Detector()

            #Set all vrf to 1500
            d.dacs.vrf = 1500

            #Check vrf
            d.dacs.vrf
            >> vrf       :  1500,  1500

            #Set a single vtr
            d.dacs.vtr[0] = 1800

            #Set vrf with multiple values
            d.dacs.vrf = [3500,3700]
            d.dacs.vrf
            >> vrf       :  3500,  3700

            #read into a variable
            var = d.dacs.vrf[:]

            #set multiple with multiple values, mostly used for large systems
            d.dacs.vcall[0,1] = [3500,3600]
            d.dacs.vcall
            >> vcall     :  3500,  3600

            d.dacs
            >>
            ========== DACS =========
            vsvp      :     0,     0
            vtr       :  4000,  4000
            vrf       :  1900,  1900
            vrs       :  1400,  1400
            vsvn      :  4000,  4000
            vtgstv    :  2556,  2556
            vcmp_ll   :  1500,  1500
            vcmp_lr   :  1500,  1500
            vcall     :  4000,  4000
            vcmp_rl   :  1500,  1500
            rxb_rb    :  1100,  1100
            rxb_lb    :  1100,  1100
            vcmp_rr   :  1500,  1500
            vcp       :  1500,  1500
            vcn       :  2000,  2000
            vis       :  1550,  1550
            iodelay   :   660,   660

        """
        return self._dacs


    @property
    def detector_type(self):
        """
        :py:obj:`str` Detector type

        * Eiger
        * Jungfrau
        * etc.

        """
        return self._api.getDetectorType()

    @property
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
    def dynamic_range(self, dr):
        if dr in self._detector_dynamic_range:
            self._api.setDynamicRange(dr)
            return
        else:
            raise ValueError('Cannot set dynamic range to: {:d} availble options: '.format(dr),
                             self._detector_dynamic_range)


    @property
    def eiger_matrix_reset(self):
        """
        Matrix reset bit for Eiger.

        :py:obj:`True` : Normal operation, the matrix is reset befor each acq.
        :py:obj:`False` : Matrix reset disableld. Used to not reset before
        reading out analog test pulses.
        """
        return self._api.getCounterBit()

    @eiger_matrix_reset.setter
    def eiger_matrix_reset(self, value):
        self._api.setCounterBit(value)

    @property
    def exposure_time(self):
        """
        :obj:`double` Exposure time in [s] of a single frame.
        """
        return self._api.getExposureTime() /1e9


    @exposure_time.setter
    def exposure_time(self, t):
        ns_time = int(t * 1e9)
        if ns_time <= 0:
            raise ValueError('Exposure time must be larger than 0')
        self._api.setExposureTime(ns_time)


    @property
    def file_index(self):
        """
        :obj:`int` Index for frames and filenames

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
    def file_index(self, i):
        if i < 0:
            raise ValueError('Index needs to be positive')
        self._api.setFileIndex(i)

    @property
    def file_name(self):
        """
        :obj:`str`: Base file name for writing images

        Examples
        ---------

        ::

            detector.file_name
            >> 'run'

            detector.file_name = 'myrun'

            #For a single acqusition the detector now writes
            # myrun_master_0.raw
            # myrun_d0_0.raw
            # myrun_d1_0.raw
            # myrun_d2_0.raw
            # myrun_d3_0.raw


        """
        return self._api.getFileName()

    @file_name.setter
    def file_name(self, fname):
        self._api.setFileName(fname)

    @property
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
    def file_path(self, path):
        if os.path.exists(path) is True:
            self._api.setFilePath(path)
        else:
            raise FileNotFoundError('File path does not exists')


    @property
    def file_write(self):
        """
        :obj:`bool` If True write files to disk
        """
        return self._api.getFileWrite()

    @file_write.setter
    def file_write(self, fwrite):
        self._api.setFileWrite(fwrite)

    @property
    def firmware_version(self):
        """
        :py:obj:`int` Firmware version of the detector
        """
        return self._api.getFirmwareVersion()

    def free_shared_memory(self):
        """
        Free the shared memory that contains the detector settings

        .. warning ::

            After doing this you can't access the detector until it is
            reconfigured

        """
        self._api.freeSharedMemory()

    @property
    def high_voltage(self):
        """
        High voltage applied to the sensor
        """
        return self._api.getDac('vhighvoltage', -1)

    @high_voltage.setter
    def high_voltage(self, voltage):
        voltage = int(voltage)
        if voltage < 0:
            raise ValueError('High voltage needs to be positive')
        self._api.setDac('vhighvoltage', -1, voltage)


    @property
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

    @property
    def image_size(self):
        """
        :py:obj:`collections.namedtuple` with the image size of the detector

        Examples
        ----------

        ::

            #Assuming 512x1024 detector size

            d.image_size
            >> ImageSize(rows=512, cols=1024)

            d.image_size.rows
            >> 512

            d.image_size.cols
            >> 1024

        """
        size = namedtuple('ImageSize', ['rows', 'cols'])
        return size(*self._api.getImageSize())

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

    def load_parameters(self, fname):
        """
        Setup detector by executing commands in a parameters file


        .. note ::

            If you are reling mainly on the Python API it is probably
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
        return Geometry(horizontal=_t[0], vertical =_t[1])

    @property
    def n_frames(self):
        """
        :obj:`int` Number of frames per acquisition
        """
        return self._api.getNumberOfFrames()

    @n_frames.setter
    def n_frames(self, n):
        if n >= 1:
            self._api.setNumberOfFrames(n)
        else:
            raise ValueError('Invalid value for n_frames: {:d}. Number of'\
                             ' frames should be an integer greater than 0'.format(n))

    @property
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
    def period(self):
        """
        :obj:`double` Period between start of frames. Set to 0 for the detector
        to choose the shortest possible
        """
        _t = self._api.getPeriod()
        return _t / 1e9

    @period.setter
    def period(self, t):
        ns_time = int(t * 1e9)
        if ns_time < 0:
            raise ValueError('Period must be 0 or positive')
        self._api.setPeriod(ns_time)


    def pulse_all_pixels(self, n):
        """
        Pulse each pixel of the chip **n** times using the analog test pulses.
        The pulse heigh is set using d.dacs.vcall with 4000 being 0 and 0 being
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

    def pulse_chip(self, n):
        """
        Advance the counter by toggeling enable. Gives 2*n+2 int the counter
        
        """
        n = int(n)
        if n>=-1:
            self._api.pulseChip(n)
        else:
            raise ValueError('n must be equal or larger than -1')

    @property
    def rate_correction(self):
        """
        :obj:`list` of :obj:`double` Rate correction for all modules.
        Set to 0 for **disabled**

        .. todo ::

            Should support individual assignments

        Raises
        -------
        ValueError
            If the passed list is not of the same lenght as the number of
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
    def rate_correction(self, tau_list):
        if len(tau_list) != self.n_modules:
            raise ValueError('List of tau needs the same length')
        self._api.setRateCorrection(tau_list)


    @property
    def readout_clock(self):
        speed = self._api.getReadoutClockSpeed()
        return self._speed_names[speed]

    @readout_clock.setter
    def readout_clock(self, value):
        speed = self._speed_int[value]
        self._api.setReadoutClockSpeed(speed)


    @property
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
    def rx_zmqip(self):
        """
        .. todo ::

            also set
        """
        return self._api.getNetworkParameter('rx_zmqip')

    @property
    def rx_zmqport(self):
        """
        Return the receiver zmq ports
        
        ::
            
            detector.rx_zmqport
            >> [30001, 30002, 30003, 30004]
            

        .. todo ::

            also set

        """
        _s = self._api.getNetworkParameter('rx_zmqport')
        if _s == '':
            return []
        return [int(_p)+i for _p in _s.strip('+').split('+') for i in range(2)]

#Add back when versioning is defined
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
    def settings(self):
        """
        Detector settings used to control for example calibration or gain
        switching. For EIGER almost always standard
        
        .. todo::
            
            check input depending on detector
        
        """
        return self._api.getSettings()
        
    @settings.setter
    def settings(self, s):
        #check input!
        self._api.setSettings(s)
        
    @property
    def settings_path(self):
        """
        The path where the slsDetectorSoftware looks for settings/trimbit files            
        """
        return self._api.getSettingsDir()
    
    @settings_path.setter
    def settings_path(self, path):
        if os.path.isdir(path):
            self._api.setSettingsDir(path)
        else:
            raise FileNotFoundError('Settings path does not exist')

    @property
    def status(self):
        """
        :py:obj`str` Status of the detector: idle, running,

        .. todo ::

            Check possible values


        """
        return self._api.getRunStatus()

    def start_acq(self):
        """
        Non blocking command to star acquisition. Needs to be used in combination
        with receiver start.
        """
        self._api.startAcquisition()

    def stop_acq(self):
        """
        Stop acquisition early or if the detector hangs
        """
        self._api.stopAcquisition()

    @property
    def sub_exposure_time(self):
        """
        Sub frame exposure time in *seconds* for Eiger in 32bit autosumming mode

        ::

            d.sub_exposure_time
            >> 0.0023

            d.sub_exposure_time = 0.002

        """
        return self._api.getSubExposureTime() /1e9

    @sub_exposure_time.setter
    def sub_exposure_time(self, t):
        ns_time = int(t * 1e9)
        if ns_time > 0:
            self._api.setSubExposureTime(ns_time)
        else:
            raise ValueError('Sub exposure time must be larger than 0')


    @property
    def threshold(self):
        """
        Detector threshold in eV
        """
        return self._api.getThresholdEnergy()
        
    @threshold.setter
    def threshold(self, eV):
        self._api.setThresholdEnergy(eV)

    @property
    def timing_mode(self):
        """
        :py:obj:`str` Timing mode of the detector

        * **auto** Something
        * **trigger** Something else

        .. todo ::

            settinng and reading!

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
        Threshold in DAC units for the detector
        """
        return self._api.getDac('vthreshold',-1)

    @vthreshold.setter
    def vthreshold(self, th):
        self._api.setDac('vthreshold', -1, th)

    @property
    def trimbits(self):
        """
        :py:obj`int` trimbits of the detector.
        """
        return self._api.getAllTrimbits()

    @trimbits.setter
    def trimbits(self, value):
        """
        test
        """
        if self._trimbit_limits.min <= value <= self._trimbit_limits.max:
            self._api.setAllTrimbits(value)
        else:
            raise ValueError('Trimbit setting {:d} is  outside of range:'\
                             '{:d}-{:d}'.format(value, self._trimbit_limits.min, self._trimbit_limits.max))

