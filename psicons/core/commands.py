#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
New scons commands.
"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import impl
Command = impl.scons_lib.Environment.Command


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

def External (exe, args=[], infiles=[], output=[], depends=[]):
	"""
	Create a task for doing analysis with an external (fixed) program.
	
	:Parameters:
		exe : str
			name of executable to be called
		args : str or list
			either a string giving the whole string that is used to pass arguments
			to the executable or a list of srtrings that can be joined to do the
			same.
		infiles : str or list
			a string or list of strings giving the paths of the files that this
			task depends on. 
		outputs : str or list
			a string or list of strings giving the paths of the files that this
			task produces.
	
	This is a command that runs a local script, 
	
		
	"""
	# TODO: should be "outputs"?
	infiles = impl.make_list (infiles or [])
	args = impl.make_list (args or [])
	cmdline = exe % {
		'args': ' '.join (args),
		'infiles': ' '.join (infiles)
	}
	output = impl.make_list (output or [])
	new_command = Command (
		output,
		infiles,
		cmdline,
	)
	depends = depends + infiles
	Depends (new_command, depends)
	return new_command


def Script (path, interpreter=None, args=[], infiles=[], output=[], depends=[],
		capture_stdout=None):
	"""
	Create a task for running a local script.
	
	This is a command that runs a local script, 
	
	"""
	interpreter = interpreter or '$PY'
	infiles = impl.make_list (infiles or [])
	# TODO: flatten tuples to make arg list like [('-a', 'b'), ('--c', 'd')] to
	# ['-a', 'b', '--c', 'd']?
	# if dict do "--x=foo"
	# TODO: autoescape/quote strings?
	# TODO: have a "SrcFile" class for use in arguments that can be picked up
	# in a scan
	# TOOD: make a "chain" where every script depends on the output of the previous
	args = impl.make_list (args or [])
	cmdline = ' '.join ([interpreter, path] + args + infiles)
	if capture_stdout:
		cmdline = ' '.join ([cmdline, '>', capture_stdout])
		output.append (capture_stdout)
	new_command = Command (
		output,
		[path] + infiles,
		cmdline,
	)
	depends = depends + infiles
	Depends (new_command, depends)
	return new_command


## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################

