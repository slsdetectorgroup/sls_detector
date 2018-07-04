# sls_detector: Python interface to slsDetectorPackage
Python interface to the Sls Detector Software. 

### Documentation ###
Sphinx built documentation is available here:
[https://slsdetectorgroup.github.io/sls_detector/](https://slsdetectorgroup.github.io/sls_detector/)


### Install using conda ###

Binaries are available using conda. This installs both the sls_detector_lib and the Python
interface.

```bash
#Add conda channels
conda config --add channels conda-forge
conda config --add channels slsdetectorgroup

#Install latest version
conda install sls_detector

#Install specific version
conda install sls_detector=3.2.0

#Optionally add the GUI
conda install sls_detector_gui=3.2.0
```

### Building using conda-build ###

Needs [sls_detector_software](https://github.com/slsdetectorgroup/sls_detector_software) installed.

```bash
#Clone source code
git clone https://github.com/slsdetectorgroup/sls_detector.git

#Checkout the branch needed
git checkout 3.2.0

#Build and install the local version
conda-build sls_detector
conda install --use-local sls_detector


```
### Developer build ###

IF you if you are developing and are making constant changes to the code it's a bit cumbersome 
to build with conda and install. Then an easier way is to build the C/C++ parts in the package 
directory and temporary add this to the path. Make sure that you have a gcc around 4.8..

```bash
#in path/to/sls_detector  
python setup.py build_ext --inplace
```
Then in your Python script
```python

import sys
sys.path.append('/path/to/sls_detector')
from sls_detector import Eiger
```

