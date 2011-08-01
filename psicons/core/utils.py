"""
Miscellaneous utilities for use in writing and using commands.

Often we will want to name or create a file based on  from pre-existing file
paths:

* create an output file in the same directory as an input file
* clean up some data and save it in a file of the same name with "-clean"
  appended, but before the extension.
* use the same extension for an output file as an input file.
* what is the extension or name of this file anyway?

Thus, here we provide a set of functions for extracting components from a file
path and extrapolating new names from the same. For consistency, here is the
terminology used:

dir
	the path of the directory a file is in
base
	the local name of a file, e.g. "foo.txt", "schedule.doc"
ext
	the extension of a file, e.g. ".txt", ".doc". Note this includes the
	separating period, so that the extensions of files "foo.txt", "foo." and
	"foo" and ".txt", "." and "" respectively.
stem
	the base file name, without the extension, e.g. "foo" and "schedule" for
	"foo.txt", "schedule.doc" respectively.
substem
	the stem of a file name, less the final "word" e.g. "foo" and "schedule_abc"
	for "foo-bar.txt" and "schedule_abc_2011.doc" respectively.

"""

### IMPORTS

import re
from os import path
from datetime import datetime


### CONSTANTS & DEFINES

INTERP_RE = re.compile (r'\{([^}]+)\}')
SUBSTEM_RE = re.compile (r'.([\.\-]\S+)$')


### IMPLEMENTATION

def dir_base (p):
	"""
	Return the directory and file name of a path.
	
	:Parameters:
		p
			a file name or path
			
	:Returns:
		the directory and base name of the file path
	
	For example::
		
		>>> dir_base ('bar.foo')
		('', 'bar.foo')
		>>> dir_base ('/bar.foo')
		('/', 'bar.foo')
		>>> dir_base ('baz/bar.foo')
		('baz/', 'bar.foo')
		>>> dir_base ('/quux/baz/bar.foo')
		('/quux/baz/', 'bar.foo')
		
	We use here the Python convention of referring to the file name (as opposed
	to path) as the "base". Also, there's an apparent oddity in the native
	splitting of paths, to do with the parent directory::
	
		>>> path.split ('bar.foo')
		('', 'bar.foo')
		>>> path.split ('/bar.foo')
		('/', 'bar.foo')
		>>> path.split ('baz/bar.foo')
		('baz', 'bar.foo')
		
	That is, the dividing filesep only appears if there is nothing else in the
	directory component. This makes things difficult if you are trying to pick
	apart a file path and reassemble it - do I need a file separator? was there
	one there before? Fortunately path.join is reasonably clever about fusing
	paths, but this is still an inconsistency and so is fixed here. 
	
	"""
	# TODO: adapt to work with non-Unix file systems (use filesep)
	d, b = path.split (p)
	if (d and (not d.endswith (path.sep))):
		d += path.sep
	return d, b

dirbase_from_path = dir_base

# TODO: rename as split?
def dir_stem_ext (p):
	"""
	Return the directory, stem of the file name and extension from a path.
	
	:Parameters:
		p
			a file name or path
			
	:Returns:
		the directory and base name stem and extension of the file path
	
	For example::
		
		>>> dir_stem_ext ('bar.foo')
		('', 'bar', '.foo')
		>>> dir_stem_ext ('bar.')
		('', 'bar', '.')
		>>> dir_stem_ext ('bar')
		('', 'bar', '')
		>>> dir_stem_ext ('baz/bar.foo')
		('baz/', 'bar', '.foo')
		>>> dir_stem_ext ('/quux/baz/bar.foo')
		('/quux/baz/', 'bar', '.foo')
		
	Note this uses the file separator convention of ``dir_base``.
	
	"""
	dir, base = dir_base (p)
	stem, ext = path.splitext (base)
	return dir, stem, ext

dirstemext_from_path = dir_stem_ext


def substem_mod (s):
	"""
	Split the 'stem' of a file name into a core name and a trailing modifier.
	
	:Parameters:
		s
			a file (base) name
			
	:Returns:
		the substem and modifier (trailing word) of the file name
	
	Many file names are structured as "foo-mod.ext" or "foo.mod.ext" where "mod"
	is some qualifier, e.g. "report-2.doc", "programme.20101201.txt". This
	sniffs out the usual forms of these endings and if found, splits and
	returns the name there.
	
	For example::
	
		>>> substem_mod ('report-2')
		('report', '-2')
		>>> substem_mod ('programme.20101201')
		('programme', '.20101201')
		>>> substem_mod ('report 2')
		('report 2', '')
		>>> substem_mod ('programme_20101201')
		('programme_20101201', '')
		
	"""
	# TODO: what do Macs do with file copies?
	# TODO: what about the windows 'foo (2).txt' pattern? Need multi regexes?
	# XXX: do we need the word separator?
	# XXX: actually would it just be more consistent to split into words and
	#   return [:-1], [-1]
	# TODO: what is there's no end word, only one word?
	# XXX: substem and mod are horrible names. Use words?
	match = SUBSTEM_RE.search (s)
	if (match):
		return s[:match.start(1)], s[match.start(1):]
	else:
		return s, ''


def interpolate (str, sub_hash):
	"""
	Interpolate the bracketed sections of the passed string as keyed substrings.
	
	:Parameters:
		str
			a string containing parens delimited locations for substitution
		sub_hash : dict
			words and substitutions to be used on the string
			
	:Returns:
		the string with substitutions made
		
	The intent for this is as a very simple templating or substitution system to
	be used in configurations and the like. 
	
	For example::
		
		>>> d = {'foo': '123', 'bar': '456'}
		>>> interpolate ('abcdef', d)
		'abcdef'
		>>> interpolate ('abc{foo}def', d)
		'abc123def'
		>>> interpolate ('ab{foo}cd{bar}ef', d)
		'ab123cd456ef'
		
	"""
	# XXX: actually, do we need to do this? are python keywords all that bad?
	#  maybe we should just use a proper templating system?
	# TODO: what does this do with proper python substitutions?
	return INTERP_RE.sub (lambda x: sub_hash[x.group(0)[1:-1].strip()], str)


def interpolate_from_path (p, tmpl, subs={}):
	"""
	Interpolate using qualities of a file path.
	
	:Parameters:
		p : str
			a file name or path
		tmpl : str
			the template for the output, containing parens delimited locations 
			for substitution
		subs : dict
			additional words and substitutions to be used on the string
			
	:Returns:
		the template string with substitutions made
		
	This allows a new file name or path (or actually any string) to be generated
	by interpolation from a file path. This allows construction of paths to files
	in the same directory, files with the same name but different extension, 
	files with the same name except for a suffix, etc.
	
	The substitution keywords are:
	
		ext
			input path file extension, e.g. ".txt"
		base
			input path file base (name), e.g. "foo-bar.txt"
		stem
			input path file name stem, e.g. "foo-bar"
		dir
			input path directory, e.g. "quux/"
		dirstem
			input path directory and stem, e.g. "quux/foo-bar"
		substem
			input path substem, e.g. "foo"
		mod
			input path modifier, e.g. "-bar"
		date
			current date
		time
			current time
			
					
	For example::
		
		>>> pth = '/foo/bar.baz'
		>>> interpolate_from_path (pth, '{stem}.new{ext}')
		'bar.new.baz'
		>>> d = {'prefix': 'PRFX', 'ext': '.txt'}
		>>> interpolate_from_path (pth, '{prefix}{stem}.new{ext}', d)
		'PRFXbar.new.txt'
		
	"""
	# ???: order args as they are used
	# TODO: some sort of number up (tested or untested) or counter
	# TODO: a default output template (so you only need to def subs?)
	_, b = dir_base (p)
	d, s, e = dir_stem_ext (p)
	ss, m = substem_mod (s)
	now = datetime.now()
	default_subs = {
		"ext": e,
		"base": b,
		"stem": s,
		"dir": d,
		"dirstem": d+s,
		"substem": ss,
		"mod": m,
		"date": now.strftime ("%Y%m%d"),
		"time": now.strftime ("%H%M%S"),
		"datetime": now.strftime ("%Y%m%dT%H%M%S"),
	}
	default_subs.update (subs)
	return interpolate (tmpl, default_subs)
	



### MAIN

if __name__ == "__main__":
	import doctest
	doctest.testmod()

### END
