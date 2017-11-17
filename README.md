# sls_detector
Python interface to the sls detector software.

### Documentation ###
Sphinx build documentation is available here:
[https://slsdetectorgroup.github.io/sls_detector/](https://slsdetectorgroup.github.io/sls_detector/)

### Building using conda-build ###

The prefered way to build and install is using the conda.  Since the installation depends on the slsDetectorsPackage download and build this first.

```bash
#Setting variables for source and shared libraries
export SLS_DETECTOR_SOURCE=/path/to/slsDetectorsPackage
export LD_LIBRARY_PATH=/path/to/slsDetectorsPackage/build/bin:$LD_LIBRARY_PATH

#Clone the rep
git clone https://github.com/slsdetectorgroup/sls_detector.git

#Build and install
conda-build sls_detector
conda install --use-local sls_detector
```

### Download conda package ###
This might work one day
