"""
Miscellaneous utilities for use in writing and using commands.
"""

### IMPORTS

import re
from os import path
from datetime import datetime


### CONSTANTS & DEFINES

INTERP_RE = re.compile (r'\{([^}]+)\}')


### IMPLEMENTATION

def make_list (arg):
	"""
	Return argument as a list.
	
	A bit of syntactical sugar intended for use in method arguments, so that
	users can pass a list or a single item.
	
	For example::
	
		>>> make_list (1)
		[1]
		>>> make_list (1, 2)
		[1, 2]
		>>> make_list (None)
		[None]
		
	"""
	if (type (arg) in [types.ListType, types.TupleType]):
		return arg
	return [arg]



def interpolate (str, sub_hash):
	"""
	Interpolate the bracketed sections of the passed string as keyed substrings.
	
	For example::
		
		>>> d = {'foo': '123', 'bar': '456'}
		>>> interpolate ('abcdef', d)
		'abcdef'
		>>> interpolate ('abc{foo}def', d)
		'abc123def'
		>>> interpolate ('ab{foo}cd{bar}ef', d)
		'ab123cd456ef'
		
	"""
	return INTERP_RE.sub (lambda x: sub_hash[x.group(0)[1:-1].strip()], str)


def interpolate_from_path (p, tmpl, subs={}):
	"""
	Interpolate using qualities of a file path.
	
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
	

def dir_base (p):
	"""
	Return the directory and file name of a path.
	
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
	# ???: what happens when 
	d, b = path.split (p)
	if (d and (not d.endswith (path.sep))):
		d += path.sep
	return d, b

dirbase_from_path = dir_base

# TODO: rename as split?
def dir_stem_ext (p):
	"""
	Return the directory, stem of the file name and extension from a path.
	
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
		
	Note this uses the file seperator convention of ``dir_base``. The
	file name stripped of the directory and extension is called the "stem" (to
	distinguish it from the "base").
				
	"""
	dir, base = dir_base (p)
	stem, ext = path.splitext (base)
	return dir, stem, ext

dirstemext_from_path = dir_stem_ext

SUBSTEM_RE = re.compile (r'.([\.\-]\S+)$')

def substem_mod (s):
	"""
	Split the 'stem' of a file name into a core name and a trailing modifier.
	
	Many file names are structured as "foo-mod.ext" or "foo.mod.ext" where "mod"
	is some qualifier, e.g. "report-2.doc", "programme.20101201.txt". This
	sniffs out the common forms of these endings and if found, splits and
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
	# TODO: what about the windows 'foo (2).txt' pattern? Need multi regexes
	match = SUBSTEM_RE.search (s)
	if (match):
		return s[:match.start(1)], s[match.start(1):]
	else:
		return s, ''
	

### MAIN

if __name__ == "__main__":
	import doctest
	doctest.testmod()

### END
