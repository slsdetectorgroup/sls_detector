Examples
================

Some short hints on how to use the detector

------------------------
Simple threshold scan
------------------------

Assuming you have set up your detector with exposure time, period, enabled
file writing etc.

.. code-block:: python
 
    from sls_detector import Detector

    d = Detector()
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
    