# sls_detector
Python interface to the sls detector software.


## Building using conda-build ##

The buid relies on two envoiremental variables to find the source code of the slsDetectorPackage and the shared libraries.

```bash
#Setting variables
export SLS_DETECTOR_SOURCE=/path/to/slsDetectorsPackage
export LD_LIBRARY_PATH=/path/to/slsDetectorsPackage/build/bin:$LD_LIBRARY_PATH

#Clone the rep
git clone https://github.com/slsdetectorgroup/sls_detector.git

#Build and install
conda-build sls_detector
conda install --use-local sls_detector
```

