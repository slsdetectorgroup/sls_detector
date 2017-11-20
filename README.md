# sls_detector
Python interface to the sls detector software.

### Documentation ###
Sphinx built documentation is available here:
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
### Developer build ###

IF you if you are developing and are making constant changes to the code it's a bit cumbersome to build with conda and install. Then an easirer way is to build the C/C++ parts in the package directory and temporary add this to the path

```bash
#in path/to/sls_detector  
python setup.py build_ext --inplace
```
Then in your Python script
```python

import sys
sys.path.append('/path/to/sls_detector')
from sls_detector import Detector
```


**Prerequisites**
 * Pyton 3
 * gcc 4.8+
 * slsDetectorsPackage 3+ 

### Download conda package ###
This might work one day
