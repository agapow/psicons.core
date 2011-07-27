

def Script (path, interpreter=None, args=[], infiles=[], output=[], depends=[],
		capture_stdout=None):
	interpreter = interpreter or '$PY'
	infiles = make_list (infiles or [])
	# TODO: flatten tuples to make arg list like [('-a', 'b'), ('--c', 'd')] to
	# ['-a', 'b', '--c', 'd']?
	# if dict do "--x=foo"
	# TODO: autoescape/quote strings?
	# TODO: have a "SrcFile" class for use in arguments that can be picked up
	# in a scan
	# TOOD: make a "chain" where every script depends on the output of the previous
	args = make_list (args or [])
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
	Depends (new_command, depends)
	return new_command

	
def External (exe, args=[], infiles=[], output=[], depends=[]):
	infiles = make_list (infiles or [])
	args = make_list (args or [])
	cmdline = exe % {
		'args': ' '.join (args),
		'infiles': ' '.join (infiles)
	}
	new_command = env.Command (
		output,
		infiles,
		cmdline,
	)
	depends = depends + infiles
	Depends (new_command, depends)
	return new_command
