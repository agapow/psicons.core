#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maintaining a list of new commands and initializing them.
"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

### CONSTANTS & DEFINES ###

NEW_COMMANDS = []


### IMPLEMENTATION ###	

def register (*args):
	for x in args:
		if x not in NEW_COMMANDS:
			NEW_COMMANDS.append (x)


def init_psicons (env):
	for c in NEW_COMMANDS:
		env.AddMethod ()


## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################
