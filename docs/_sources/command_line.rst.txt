Command line to Python
=========================

If you are already familiar with the command line interface to the
slsDetectorSoftware here is a quick reference translating to Python commands


 .. note ::
     
     Commands labeled Mythen only  or Gotthard only are currently not implemented in the 
     Python class. If you need this functionallity please contact the SLS Detector Group

.. py:currentmodule:: sls_detector

.. |resmat| replace:: :py:attr:`Eiger.eiger_matrix_reset`
.. |stat| replace:: :py:attr:`Detector.status`
.. |ro| replace:: *(read only)* 
.. |start| replace:: :py:func:`Detector.start_detector` 
.. |stop| replace:: :py:func:`Detector.stop_detector` 
.. |conf| replace:: :py:func:`Detector.load_config` 
.. |pars| replace:: :py:func:`Detector.load_parameters` 
.. |free| replace:: :py:func:`Detector.free_shared_memory` 
.. |speed| replace:: :py:attr:`Detector.readout_clock` 
.. |firmv| replace:: :py:attr:`Detector.firmware_version`
.. |sub| replace:: :py:attr:`Detector.sub_exposure_time` 
.. |tb| replace:: :py:attr:`Detector.trimbits`
.. |mg| replace:: Mythen and Gotthard only
.. |g| replace:: Gotthard only
.. |m| replace:: Mythen only
.. |new_chiptest| replace:: New chip test board only
.. |chiptest| replace:: Chip test board only
.. |dr| replace::  :py:attr:`Detector.dynamic_range` 
.. |j| replace:: Jungfrau only
.. |rate| replace:: :py:attr:`Detector.rate_correction`
.. |te| replace:: :py:attr:`Detector.trimmed_energies`
.. |rxd| replace:: :py:attr:`Detector.rx_datastream`
.. |temp_fpgaext| replace:: :py:attr:`Detector.temp`.fpgaext
.. |epa| replace:: :py:func:`Eiger.pulse_all_pixels` 
.. |rfc| replace:: :py:func:`Detector.reset_frames_caught` 
.. |rfi| replace:: :py:attr:`Detector.receiver_frame_index` 
.. |ron| replace:: :py:attr:`Detector.receiver_online`

------------------------
Commands
------------------------

===================== ================================= ================== =========
Command               Python                              Implementation     Tests
===================== ================================= ================== =========
sls_detector_acquire   :py:func:`Detector.acq`               OK               No
test                   Also not in the cmdline?
help                   help(Detector.acq)
exitserver
exitreceiver
flippeddatay           Also not in the cmdline?
digitet                Which detector?
bustest                |m|
digibittest            Which detector?
reg                   :py:attr:`Jungfrau.register`          OK
adcreg
setbit
clearbit
getbit
r_compression          Also not in the cmdline?
acquire               :py:func:`Detector.acq`
busy                  :py:attr:`Detector.busy`                OK              Partial
status                |stat|                                  OK |ro|
status start          |start|                                 OK
status stop           |stop|                                  OK
data                  |m|                   
frame                 |m|                
readctr               |g|                 
resetctr              |g|               
resmat                |resmat|                                OK               OK
free                  |free|
add
remove
type                  :py:attr:`Detector.detector_type`       OK               OK
hostname              :py:attr:`Detector.hostname`            OK               OK
id
master
sync
online                :py:attr:`Detector.online`               OK
checkonline
activate
nmod                   |m|
maxmod                 |m|
dr                     |dr|                                    OK              OK
roi                    |g|
detsizechan           :py:attr:`Detector.image_size`           OK
roimask                ??
flippeddatax
tengiga               :py:attr:`Eiger.tengiga`
gappixels             :py:attr:`Eiger.add_gappixels`       OK
flags
extsig                 |mg|
programfpga            |j|
resetfpga              |j|
powerchip              |j|
led                    Moench?
pulse                 Used in |epa|                           OK
pulsenmove            Used in |epa|                           OK
pulsechip             :py:func:`Eiger.pulse_chip`             OK
moduleversion         |m|
detectornumber
modulenumber          |m|
detectorversion       |firmv|                                OK               OK
softwareversion
thisversion
receiverversion
timing                :py:attr:`Detector.timing_mode`
exptime               :py:attr:`Detector.exposure_time`      OK               OK
subexptime            |sub|                                  OK               OK
period                :py:attr:`Detector.period`             OK               OK
delay                 |mg|
gates                 |mg|
frames                :py:attr:`Detector.n_frames`           OK               OK
cycles                :py:attr:`Detector.cycles`            OK
probes                |m|
measurements
samples               Chip test board only (new?)
exptimel              |mg|
periodl               |mg|
delayl                |mg|
gatesl                |mg|
framesl               |mg|
cyclesl               |mg|
probesl               |mg|
now
timestamp             |m|
nframes                ??
clkdivider            |speed|                            OK                   OK
setlength             |m|
waitstates            |m|
totdivider            |m|
totdutycycle          |m|
phasestep             |g|
oversampling          |new_chiptest|
adcclk                |new_chiptest|
adcphase              |new_chiptest|
adcpipeline           |new_chiptest|
dbitclk               |new_chiptest|
dbitphase             |new_chiptest|
dbitpipeline          |new_chiptest|
config                |conf|                             OK (set)
rx_printconfig
parameters            |pars|                             OK (set)
setup
flatfield
ffdir
ratecorr              |rate|
badchannels
angconv
globaloff
fineoff
binsize
angdir
moveflag
samplex
sampley
threaded              :py:attr:`Detector.threaded`
darkimage
gainimage 
settingsdir           :py:attr:`Detector.settings_path`
trimdir
caldir
trimen                |te|
settings              :py:attr:`Detector.settings`
threshold             :py:attr:`Detector.threshold`
thresholdnotb
trimbits              :py:func:`Detector.load_trimbits`
trim
trimval               |tb|                                    OK             OK
pedestal
vthreshold            :py:attr:`Detector.vthreshold`
vhighvoltage          :py:attr:`Detector.high_voltage`         OK
temp_adc
temp_fpga              :py:attr:`Detector.temp`.fpga           OK
temp_fpgaext           |temp_fpgaext|                          OK
temp_10ge              :py:attr:`Detector.temp`.t10ge          OK
temp_dcdc              :py:attr:`Detector.temp`.dcdc           OK
temp_sodl              :py:attr:`Detector.temp`.sodl           OK
temp_sodr              :py:attr:`Detector.temp`.sodr           OK
adc
temp_fpgafl            :py:attr:`Detector.temp`.fpgafl         OK
temp_fpgafr            :py:attr:`Detector.temp`.fpgafr         OK
outdir                 :py:attr:`Detector.file_path`           OK            OK
fname                  :py:attr:`Detector.file_name`           OK            OK
index                  :py:attr:`Detector.file_index`          OK            OK
enablefwrite           :py:attr:`Detector.file_write`          OK            OK
overwrite
currentfname
fileformat
positions
startscript
startscriptpar
stopscript
stopscriptpar
scriptbefore
scriptbeforepar
scriptafter
scriptafterpar
headerafter
headerbefore
headerbeforepar
headerafterpar
encallog
angcallog
scan0script
scan0par
scan0prec
scan0steps
scan0range
scan1script
scan1par
scan1prec
scan1steps
scan1range
rx_hostname           :py:attr:`Detector.rx_hostname`
rx_udpip              :py:attr:`Detector.rx_udpip`
rx_udpmac
rx_udpport            :py:attr:`Detector.rx_udpport`
rx_udpport2           :py:attr:`Detector.rx_udpport`
detectormac
detectorip
txndelay_left
txndelay_right
txndelay_frame
flowcontrol_10g
zmqport
rx_zmqport              :py:attr:`Detector.rx_zmqport`             Read
rx_datastream           |rxd|                                   OK
zmqip
rx_zmqip                :py:attr:`Detector.rx_zmqip`            Read
configuremac
rx_tcpport             :py:attr:`Detector.rx_tcpport`
port
stopport
lock
lastclient
receiver
r_online              |ron|
r_checkonline
framescaught          :py:attr:`Detector.frames_caught`
resetframescaught     |rfc|
frameindex            |rfi|
r_lock
r_lastclient
r_readfreq
rx_fifodepth
r_silent
adcinvert             |chiptest|
adcdisable            |chiptest|
pattern               |chiptest|
patword               |chiptest|
patioctrl             |chiptest|
patclkctrl            |chiptest|
patlimits             |chiptest|
patloop0              |chiptest|
patnloop0             |chiptest|
patwait0              |chiptest|
patwaittime0          |chiptest|
patloop1              |chiptest|
patnloop1             |chiptest|
patwait1              |chiptest|
patwaittime1          |chiptest|
patloop2              |chiptest|
patnloop2             |chiptest|
patwait2              |chiptest|
patwaittime2          |chiptest|
dut_clk               |chiptest|
===================== ================================= ================== =========

