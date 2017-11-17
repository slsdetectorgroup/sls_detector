# sls_detector
Python interface to the sls detector software.


## Building using conda-build ##

The buid relies on two envoiremental variables to find the source code of the slsDetectorPackage and the shared libraries. So before starting set:

SLS_DETECTOR_SOURCE=/path/to/slsDetectorsPackage
LD_LIBRARY_PATH=/path/to/slsDetectorsPackage/build/bin

Clone the repository

conda-build sls_detector

conda install --use-local sls_detector


