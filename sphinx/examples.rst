Examples
================

Some short hints on how to use the detector

------------------------
Simple threshold scan
------------------------

Assuming you have set up your detector with exposure time, period, enabled
file writing etc.

.. code-block:: python
 
    from sls_detector import Eiger

    d = Eiger()
    threshold = range(0, 2000, 200)
    for th in threshold:
        d.vthreshold = th
        d.acq()
    

If we want to control the shutter of for example, the big X-ray box we can add
this line in our code. It then opens the shutter just befre the measurement
and closes is afterwards.
    
::

    with xray_box.shutter_open:
        for th in threshold:
            d.vthreshold = th
            d.acq()
        
        
-----------------------
Reading temperatures
-----------------------       

::

    d.temp
    >>
    temp_fpga     :  40.81°C,  39.13°C
    temp_fpgaext  :  38.50°C,  35.50°C
    temp_10ge     :   0.00°C,   0.00°C
    temp_dcdc     :  41.50°C,  41.00°C
    temp_sodl     :  39.50°C,  37.00°C
    temp_sodr     :  36.50°C,  39.50°C
    temp_fpgafl   :  41.30°C,  34.08°C
    temp_fpgafr   :  41.20°C,  41.43°C
    
    d.temp.fpga
    >> temp_fpga     :  40.84°C,  39.31°C
    
    t = d.temp.fpga[0]
    t
    >> 40.551
    
    t = d.temp.fpga[:]
    t
    >> [40.566, 39.128]


-----------------------
Non blocking acquire
-----------------------


::

    import time
    from sls_detector import Eiger
    d = Eiger()

    n = 10
    t = 1

    d.exposure_time = t
    d.n_frames = n
    d.reset_frames_caught()

    #Start the measurement
    t0 = time.time()
    d.start_receiver()
    d.start_detector()

    #Wait for the detector to be ready or do other important stuff
    time.sleep(t*n)

    #check if the detector is ready otherwise wait a bit longer
    while d.status != 'idle':
        time.sleep(0.1)

    #Stop the receiver after we got the frames
    #Detector is already idle so we don't need to stop it
    d.stop_receiver()

    lost = d.frames_caught - n
    print(f'{n} frames of {t}s took {time.time()-t0:{.3}}s with {lost} frames lost ')

    #Reset to not interfere with a potential next measurement
    d.reset_frames_caught()

