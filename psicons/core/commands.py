#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
New scons commands.

The process of installing a new tool or module for use by SCons is fiddly, 
involves copying libraries in a tool directory, registering 
their use in build files, voids the ease of using ``easy_install`` and makes 
development a pain. Thus, these additional "commands" are real scons commands, so
much as functions that generate commands. But they are easy to use.


"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import impl


### CONSTANTS & DEFINES ###

INPUT_SUB_STRS = ['input %s', 'input-%s', 'input[%s]']

OUTPUT_SUB_STRS = ['output %s', 'output-%s', 'output[%s]']


### IMPLEMENTATION ###	

def Cline (env, cline, inputs=[], outputs=[], capture_stdout=None):
	"""
	Create a task for doing analysis with an external (fixed) program.
	
	:Parameters:
		env : Environment
			The environment created for the build
		cline : str or list
			either the commandline to be called or a list of strings that can be
			joined to do the same (e.g. ``["--foo", "5", "-t", "one.txt"]``). The
			string is trimmed, newlines removed, and substitutions
			removed before using.
		inputs : str or list
			a string or list of strings giving the paths of the files that this
			task depends on. This will be substituted into the commandline.
		outputs : str or list
			a string or list of strings giving the paths of the files that this
			task produces. This will be substituted into the commandline.
		capture_stdout : None or str
			Record the output of the tool. If a string is provided, this will be
			used as the path of the file to save it in.
	
	This is a command that runs a commandline, intended for processing input
	datafiles to output data files. It calls the named executable with the
	passed arguments. Infiles and any others listed in `depends` are recorded
	as dependencies. outfiles and the captured output are listed as outputs.
	These will be used in dependency tracking.
	
	"""
	## Preconditions:
	if isinstance (inputs, basestring):
		inputs = [inputs]
	if isinstance (outputs, basestring):
		outputs = [outputs]
		
		
	# build commandline
	if not isinstance (cline, basestring):
		# assume sequence, and join together stripped components
		# XXX: use a regex to clean up?
		cline = ' '.join ([c.strip() for x in cline])
	# cleanup string - probably unnecessary, but allows cline components to be
	# pretty-printed over multiple lines
	cline = ' '.join (cline.strip().split('\n'))
	
	# build substitution dictionary
	subs = {}
	if isinstance (inputs, dict):
		subs.update (inputs)
		input_list = inputs.values()
	else:
		for i, f in enumerate (inputs):
			for s in INPUT_SUB_STRS:
				subs[s % i] = f
		input_list = list(inputs)
	if isinstance (outputs, dict):
		subs.update (outputs)
		output_list = outputs.values()
	else:
		for i, f in enumerate (outputs):
			for s in OUTPUT_SUB_STRS:
				subs[s % i] = f
		output_list = list(outputs)	
	
	# build cline with substitutions
	subbed_cline = cline % subs
	
	if capture_stdout:
		cline = ' '.join ([cmdline, '>', capture_stdout])
		output_list.append (capture_stdout)
	
	# actually make command
	new_command = env.Command (
		output_list,
		input_list,
		subbed_cline,
	)
	depends = depends + input_list
	env.Depends (new_command, depends)
	return new_command


register (Cline)

# external calls
# Cline (env, [exe] + make_list(args), inputs=[], outputs=[], capture_stdout=None)
# scripts calls
# Cline (env, [interp, script] + make_list(args), inputs=[], outputs=[], depends=[scitps],
# capture_stdout=None)



def External (env, exe, args=[], infiles=[], output=[], depends=[],
		capture_stdout=None):
	"""
	Create a task for doing analysis with an external (fixed) program.
	
	:Parameters:
		env : Environment
			The environment created for the build
		exe : str
			name of executable to be called
		args : str or list
			either a string that is used to pass arguments to the executable 
			(e.g. ``"--foo 5 -t one.txt"``) or a list of strings that can be joined to
			do the same (e.g. ``["--foo", "5", "-t", "one.txt"]``).
		infiles : str or list
			a string or list of strings giving the paths of the files that this
			task depends on. 
		output : str or list
			a string or list of strings giving the paths of the files that this
			task produces.
		capture_stdout : None or str
			Record the output of the tool. If a string is provided, this will be
			used as the path of the file to save it in.
	
	This is a command that runs an executable, intended for processing input
	datafiles to output data files. It calls the named executable with the
	passed arguments. Infiles and any others listed in `depends` are recorded
	as dependencies. outfiles and the captured output are listed as outputs.
	These will be used in dependency tracking.
	
	"""
	# TODO: should be "outputs"?
	infiles = impl.make_list (infiles or [])
	args = impl.make_list (args or [])
	cmdline = exe % {
		'args': ' '.join (args),
		'infiles': ' '.join (infiles)
	}
	output = impl.make_list (output or [])
	new_command = env.Command (
		output,
		infiles,
		cmdline,
	)
	depends = depends + infiles
	env.Depends (new_command, depends)
	return new_command


register (External)



def Script (env, path, interpreter=None, args=[], infiles=[], output=[], 
		depends=[], capture_stdout=None):
	"""
	Create a task for running a local script.
	
	:Parameters:
		path : str
			Pathway to the script
		interpreter
			Interpreter to run the script with. If None, assume it is python.
			
		

	This is a command that runs a local script, intended for processing input
	datafiles to output data files. It work like `External`, except that the 
	script itself is made a dependency for this step. Thus ,alterations in the
	script will trigger rerunning. All undescribed parameters are as per `External`.
	
	For example::
	
		>>> env = SconsEnv()
		>>> make_clean_data = Script ('Scripts/clean.py',
			...	args = ['--save-as', 'output.txt'],
			...	infiles = ['indata.txt'],
			...	output = 'output.txt',
		...	)
		>>> type_data = Script ('count_types.pl',
		...		interpreter = 'perl',
		...		args = ['--use-types', 'type_data.csv'],
		...		infiles = ['clean_data.txt'],
		...		depends = 'type_config.txt',
		...		capture_stdout='captured-types.txt',
		...	)
	
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
	new_command = env.Command (
		output,
		[path] + infiles,
		cmdline,
	)
	depends = depends + infiles
	env.Depends (new_command, depends)
	return new_command


register (Script)

def Final (env, f):
	pass


register (Cline, Script, External, File)



## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################

