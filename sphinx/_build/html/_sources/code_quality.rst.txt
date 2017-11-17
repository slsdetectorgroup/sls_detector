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
Tested with a detector
-----------------------

Last but not least... *actually last just because of the long list included.*
All code that goes in should have adequate tests. If a new function does not
have a minimum of one test it does not get added. Focus is on tests with a 
detector connected instead of using a mock. 

**Current status**

 ::
 
    #2017-11-14
    test_not_busy (test_acq.TestAcquire) ... ok
    test_set_eiger_resmat_false (test_acq.TestAcquire) ... ok
    test_set_eiger_resmat_true (test_acq.TestAcquire) ... ok
    test_set_full_speed (test_acq.TestAcquire) ... ok
    test_set_half_speed (test_acq.TestAcquire) ... ok
    test_set_quarter_speed (test_acq.TestAcquire) ... ok
    test_set_super_slow_speed (test_acq.TestAcquire) ... ok
    test_if_raising_on_wrong_value (test_dynamic_range.TestDynamicRange) ... ok
    test_setting_to_16 (test_dynamic_range.TestDynamicRange) ... ok
    test_setting_to_32 (test_dynamic_range.TestDynamicRange) ... ok
    test_setting_to_4 (test_dynamic_range.TestDynamicRange) ... ok
    test_setting_to_8 (test_dynamic_range.TestDynamicRange) ... ok
    test_file_path_type (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_get_number_of_modules (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_if_raising_on_negative (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_if_raising_on_non_existing_path (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_module_geometry_horizontal (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_module_geometry_vertical (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_set_and_get_file_path (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_set_file_index (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_set_file_name (test_file_index_and_names.TestFileIndexAndNames) ... ok
    test_first_hostname_is_correct (test_hostname.TestHostname) ... ok
    test_hostname_has_same_length_as_n_modules (test_hostname.TestHostname) ... ok
    test_return_type_is_list (test_hostname.TestHostname) ... ok
    test_second_hostname_is_correct (test_hostname.TestHostname) ... ok
    test_hasattr_exposure_time (test_timers.TestTimers) ... ok
    test_hasattr_n_frames (test_timers.TestTimers) ... ok
    test_hasattr_period (test_timers.TestTimers) ... ok
    test_hasattr_sub_exposure_time (test_timers.TestTimers) ... ok
    test_if_n_frames_raise_on_float (test_timers.TestTimers) ... ok
    test_if_n_frames_raise_on_neg_values (test_timers.TestTimers) ... ok
    test_set_and_get_exp_time_random (test_timers.TestTimers) ... ok
    test_set_and_get_exposure_time (test_timers.TestTimers) ... ok
    test_set_and_get_nframes (test_timers.TestTimers) ... ok
    test_set_and_get_period (test_timers.TestTimers) ... ok
    test_set_and_get_sub_exposure_time (test_timers.TestTimers) ... ok
    test_raises_when_tb_is_too_large (test_trimbits_and_dacs.TestTrimbitsAndDacs) ... ok
    test_raises_when_tb_is_too_small (test_trimbits_and_dacs.TestTrimbitsAndDacs) ... ok
    test_set_and_get_trimbits_17 (test_trimbits_and_dacs.TestTrimbitsAndDacs) ... ok
    test_set_and_get_trimbits_32 (test_trimbits_and_dacs.TestTrimbitsAndDacs) ... ok
    test_firmware_version (test_version_numbers.TestVersionNumbers) ... ok
    test_hasattr_firmware_version (test_version_numbers.TestVersionNumbers) ... ok
    
    ----------------------------------------------------------------------
    Ran 42 tests in 5.081s
    
    OK

    
