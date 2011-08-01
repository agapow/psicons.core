#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A hack to subvert the scons build system for scientific analysis.

Psicons allows scripts and external programs for analysis to be incorporated into
a build procedure.  Every stage of analysis is a command-line call to a script
or executable that takes *inputs* and produces *outputs*. When scons is called, 
dependencies between outputs and inputs are tested and only those stages are run
that are necessary to update outputs. In addition, the exact sequence of 
analyses recorded by the build file.
"""

__docformat__ = 'restructuredtext en'
__version__ = '0.1'
__author__ = "Paul-Michael Agapow (pma@agapow.net)"


### IMPORTS ###

from commands import *
from utils import *


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################
