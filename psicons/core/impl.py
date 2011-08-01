#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Internal implementation utilities and details.

This module contains various odds and ends to make development easier. None of
the code within should be relied upon as it is subject to change at a whim.
"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import types

__all__ = [
	'make_list',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

def make_list (x):
	"""
	If this isn't a list, make it one.
	
	:Parameters:
		x : list, tuple, other
			a sequence, or a single element to be placed in a sequence
			
	:Returns:
		Either the original a parameter if a sequence, or the parameter placed in
		a list.
	
	Syntactic sugar for allowing method calls to be single elements or lists of
	elements.
	
	For example::
	
		>>> make_list (1)
		[1]
		>>> make_list ('1')
		['1']
		>>> make_list ([1, 2])
		[1, 2]
		>>> make_list ((1, 2))
		(1, 2)
		
	"""
	# TODO: should be a more general way of doing this
	if (type (x) not in (types.ListType, types.TupleType)):
		x = [x]
	return x


## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################
