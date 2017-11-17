Installation
=========================


The software is developed and tested with `Python3.6`_ It is recommended to 
install Python using `Anaconda Python`_ to have a separated distribution but 
this is of course not needed. For controlling the detector use v3.0+ of the 
`slsDetectorsPackage`_. Backwards compatibility is possible but in no means 
guaranteed.

.. _Anaconda Python:  https://www.anaconda.com/download/
.. _Python3.6: https://www.python.org/
.. _slsDetectorsPackage: https://www.psi.ch/detectors/users-support


**Get the latest code from git:** ::

    git clone git@some.place.some.where

**Build using CMAKE** ::

    #in sls_detector
    mkdir build
    cmake ..
    build

**Add the build  directory to your $PYTHONPATH**:: 

     export PYTHONPATH=/path/to/sls_detector:$PYTHONPATH

To to make it permanent add it to your ~/.bashrc  


.. note::
     To easier update and modify the code adding py_sls to
     $PYTHONPATH is preferred over installing it in a general location    


--------------
Prerequisites
--------------

 * `Python3.6`_
 * `slsDetectorsPackage`_ 3.0+
 * gcc 4.8+
