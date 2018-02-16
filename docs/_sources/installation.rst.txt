Installation
=========================


The software is developed and tested with `Python3.6`_ It is recommended to 
install Python using `Anaconda Python`_ to have a separated environment, but
this is of course not mandatory. For controlling the detector use v3.0+ of the
`slsDetectorsPackage`_. Backwards compatibility is likely but in no means
guaranteed regarding Python and slsDetectorPackage.

.. _Anaconda Python:  https://www.anaconda.com/download/
.. _Python3.6: https://www.python.org/
.. _slsDetectorsPackage: https://github.com/slsdetectorgroup/slsDetectorPackage




---------------------
Install using conda
---------------------

Binaries are available using conda. This is from our experience the easiest and
most convenient way to install both the slsDetectorPackage and the Python API.
To install both run the following commands after having installed Anaconda/Miniconda.

::

    #Add conda channels
    conda config --add channels conda-forge
    conda config --add channels slsdetectorgroup

    #Install latest version
    conda install sls_detector

    #Install specific version
    conda install sls_detector=3.0.1

    #Scientific Linux 6 version (GLIBC2.12)
    conda install sls_detector=SL6_3.0.1


------------------------------
Local build using conda-build
------------------------------

Needs the `sls_detector_software`_ installed  in order to automatically find headers
and shared libraries.

.. _sls_detector_software: https://github.com/slsdetectorgroup/sls_detector_software

::

    #Clone source code
    git clone https://github.com/slsdetectorgroup/sls_detector.git

    #Checkout the branch needed
    git checkout 3.0.1

    #Build and install the local version
    conda-build sls_detector
    conda install --use-local sls_detector


-----------------------
Developer build
-----------------------

IF you if you are developing and are making constant changes to the code it's a bit cumbersome
to build with conda and install. Then an easier way is to build the C/C++ parts in the package
directory and temporary add this to the path

::

    #in path/to/sls_detector
    python setup.py build_ext --inplace

Then in your Python script

::

    import sys
    sys.path.append('/path/to/sls_detector')
    from sls_detector import Detector





--------------
Prerequisites
--------------

The default version of the software is distributed with the slsDetecorGui which depends
on Qwt and Qt. It is possible to compile without the Gui to reduce the dependencies. When
installing trough conda, conda manages all dependencies.

 * `Python3.6`_
 * `slsDetectorsPackage`_ 3.0+
 * gcc 4.8+
 * Qwt 6
 * Qt 4.8
