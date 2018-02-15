Code quality
=============================

For usability and reliability of the software the code needs to be high quality. For this
project it means meeting the four criteria described below. Any addition should pass all of 
them. 

.. todo::
	Investigate continuous integration pipelines


--------------------------------
Look, read and feel like Python
--------------------------------

When using classes and functions from the 
package it should feel like you are using Python tools and be forces
to write C++ style code with Python syntax.

::
	
    with xray_box.shutter_open():
        for th in threshold:
            d.vthreshold = th
            d.acq()

should be preferred over

::

    N = len(threshold)
    xray_box.open_shutter()
    for i in range(N):
        d.dacs.set_dac('vthreshold', threshold[i])
        d.acq()
    xray_box.close_shutter()
    
even if the difference might seem small.

--------------------
Have documentation
--------------------

Classes and functions should be documented with doc-strings
in the source code. Preferably with examples. The syntax to be used
is numpy-sphinx.

::

    def function(arg):
        """
        This is a function that does something
        
        Parameters
        ----------
        arg: int
            An argument
            
        Returns
        --------
        value: double
            Returns a value
            
        """
        return np.sin(arg+np.pi)

---------------------------------
Pass static analysis with pylint
---------------------------------

Yes, anything less than 9/10 just means that you are lazy. If 
there is a good reason why to diverge, then we can always 
add an exception.

Currently the following additions are made:

 * good-names: x, y, ax, im etc. 
 * function arguments 10
 * Whitelist: numpy, _sls



-----------------------
Tested code
-----------------------

Last but not least... *actually last just because of the long list included.*
All code that goes in should have adequate tests. If a new function does not
have a minimum of one test it does not get added.
 
**Unit-tests with pytest and mocker**

 ::
 
    ----------- coverage: platform linux, python 3.6.3-final-0 -----------
    Name                       Stmts   Miss  Cover
    ----------------------------------------------
    sls_detector/__init__.py       2      0   100%
    sls_detector/detector.py     272     28    90%
    ----------------------------------------------
    TOTAL                        274     28    90%
    
    
    ===================== 92 passed in 0.59 seconds =====================


    
**Simple integration tests**

These tests require a detector connected. Performs simple tasks like setting 
exposure time and reading back to double check the value

**Complex integration test**

Typical measurements. Might require X-rays. Tests are usually evaluated from 
plots