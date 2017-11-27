Error handling
=========================


Check input in Python
----------------------

As far as possible we try to check the input on the Python side
before calling the slsDeteectorsSoftware. Errors should not pass
silently but raise an exception

::

    #Trimbit range for Eiger is 0-63
    detector.trimbits = 98
    (...)
    ValueError: Trimbit setting 98 is  outside of range:0-63
    
Errors in slsDetectorsSoftware
-------------------------------

The slsDetectorsSoftware uses a mask to record errors from the different
detectors. If an error is found we raise a RuntimeError at the end of the 
call using the error message from slsDetectorsSoftware

.. todo ::

    Implement this for all functions

::

    detector.settings = 'bananas'
    (...)
    RuntimeError: Detector 0:
    Could not set settings.
    Detector 1:
    Could not set settings.
    Detector 2:
    Could not set settings.