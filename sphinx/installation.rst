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


**Get the latest code from git:** 

.. code-block:: bash

   git clone https://github.com/slsdetectorgroup/sls_detector.git


**Build using conda-build**

The prefered way to build and install is using the conda. 
Since the installation depends on the slsDetectorsPackage download 
and build this first.

.. code-block:: bash

    #Setting variables for source and shared libraries
    export SLS_DETECTOR_SOURCE=/path/to/slsDetectorsPackage
    export LD_LIBRARY_PATH=/path/to/slsDetectorsPackage/build/bin:$LD_LIBRARY_PATH
    
    #Clone the rep
    git clone https://github.com/slsdetectorgroup/sls_detector.git
    
    #Build and install
    conda-build sls_detector
    conda install --use-local sls_detector


**Developer build**

IF you if you are developing and are making constant changes to the code it's a bit cumbersome to build with conda and install. Then an easirer way is to build the C/C++ parts 
in the package directory and temporary add this to the path


.. code-block:: bash

    #in path/to/sls_detector  
    python setup.py build_ext --inplace
    
Then in your Python script
    
.. code-block:: python

    import sys
    sys.path.append('/path/to/sls_detector')
    from sls_detector import Detector


--------------
Prerequisites
--------------

 * `Python3.6`_
 * `slsDetectorsPackage`_ 3.0+
 * gcc 4.8+
