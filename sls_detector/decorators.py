#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 17:12:06 2017

@author: l_frojdh
"""
from .errors import DetectorError

def error_handling(func):
    """
    decorator to check for errors in the detector layer
    """
    def wrapper(self, *args, **kwargs):
        #clear error mask to remove old errors
        self._api.clearErrorMask()
        
        #original function call
        result = func(self, *args, **kwargs)
        
        #now check the error mask
        m = self.error_mask
        if m != 0:
            msg = self.error_message
            self._api.clearErrorMask()
            raise DetectorError(msg)
        return result
    return wrapper