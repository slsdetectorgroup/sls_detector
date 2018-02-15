Getting started
================


------------------------
Setting up the detector
------------------------
        
Currently there is no support for setting up the detector, starting 
receivers etc. Configure your detector as normal and then launch a
Python terminal. The detector is the discovered automatically.        
        
---------------------------------
Setting and getting attributes
---------------------------------        

Most of the detector and software setting are implemented as attributes
in the Detector class. When something is assigned it is also set 
in the detector and when the attribute is called using dot notation it
it looked up from the detector.

::

    #Currently Eiger and Jungfrau but Detector should work for all
    from sls_detector import Eiger()
    d = Eiger()
    
    d.file_write = True
    d.vthreshold = 1500
    
    d.frame_index
    >> 12
    
    d.file_name
    >> 'run'
    
---------------------------------
Working with DACs
---------------------------------  

The following examples assumes an Eiger500k detector. But the same syntax
works for other detector sizes and models.

::

    d.dacs
    >>
    ========== DACS =========
    vsvp      :     0,     0
    vtr       :  4000,  4000
    vrf       :  2000,  2300
    vrs       :  1400,  1400
    vsvn      :  4000,  4000
    vtgstv    :  2556,  2556
    vcmp_ll   :  1500,  1500
    vcmp_lr   :  1500,  1500
    vcall     :  3500,  3600
    vcmp_rl   :  1500,  1500
    rxb_rb    :  1100,  1100
    rxb_lb    :  1100,  1100
    vcmp_rr   :  1500,  1500
    vcp       :  1500,  1500
    vcn       :  2000,  2000
    vis       :  1550,  1550
    iodelay   :   660,   660
    
    #Read dac values to a variable
    vrf = d.dacs.vrf[:]
    
    #Set a dac in a module
    d.dacs.vrf[0] = 1500
    d.dacs.vrf[0]
    >> 1500
    
    #Set vrf to the same value in all moduels
    d.dacs.vrf = 1500
    
    #Set a dac using an iterable
    d.dacs.vrf = [1500, 1600]
    d.dacs.vrf
    >> vrf       :  1500,  1600
    
    #Set dacs iterating on index and values
    d.dacs.vrf[0,1] = 1300,1400