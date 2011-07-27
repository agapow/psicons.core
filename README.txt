==================
About psicons.core
==================

Background
----------

Scientific analysis can be problematic:

* It may involve multiple steps, each using the results of the previous stage. Making a mistake often means repeating the whole series for safety.
* Sometimes analysis chains have to be repeated on different datasets. Sometimes, even within a single analysis, the same manipulation or test has to be repeated with slightly different parameters.
* But even immediately after the fact, it's easy to forget what was done. 9 months later when responding to a referee's report, it may be impossible.
* Collaborators, clients or bosses may demand accountability.
* With long but routine tasks, it's easy to get bored and make mistakes.

It this light, *psicons* is a quick and dirty hack to subvert the scons build system for scientific analysis. Every stage of analysis is a command-line call to a script or executable that takes *inputs* and produces *outputs*. When scons is called, dependencies between outputs and inputs are tested and only those stages are run that are necessary to update outputs. In addition, analysis steps are documented by
the build file. In summary, *psicons* provides:

* Repeatability: running a build file repeats the analysis
* Reproducibility: the build file (and custom scripts) document the steps of the analysis
* Minimization of effort: if inputs or analysis steps are changed, only the necessary (dependent) steps of the analysis are rerun
* Mistake-resistant: errors don't derail analysis due to reproducibility ("what did I do") and minimization of effort (only dependent steps are repeated)


Status
------

*psicons* is very much a hack-and-see project, having been produced in the aftermath of the 2009 H1N1 pandemic from the need for complex processing of large amounts of sequence data. It is by no means

, having been produced to support another
package and see if use can be got out of generalising conversion. As such. it 
is still an early release and the API may change. Comment is invited.


Installation
------------

The simplest way to install *konval* is via ``easy_install`` [setuptools]_ or an
equivalent program::

	% easy_install konval

Alternatively the tarball can be downloaded, unpacked and ``setup.py`` run::

	% tar zxvf konval.tgz
	% cd konval
	% python set.py install

*konval* has no prerequisites and should work with just about any version of
Python.


Using konval
------------

A full API is included in the source distribution.


Examples
~~~~~~~~

Most commonly, konval will be used to check or clean values. Failures result in
exceptions being thrown::

	# convert user input to a actual integer
	>>> from konval import *
	>>> sanitize ('1.0', ToInt())
	1
	>>> sanitize ('one', ToInt())
	Traceback (most recent call last)
	...
	ValueError: can't convert 'one' to integer
	
A single validator or list can be passed to `sanitize`. Failure in any will
result in any exception::

	# check a list has no more than 3 members
	>>> sanitize (['a', 'b', 'c'], [ToLength(),IsEqualOrLess(3)])
	3
	# check a password is long enough
	>>> sanitize ('mypass', [ToLength(),IsEqualOrMore(8)])
	Traceback (most recent call last)
	...
	ValueError: 6 is lower than 8

Any callable object that accepts and returns a single value can be used as a
validator::
	
	>>> from string import *
	>>> sanitize (" my title ", [strip, capitalize])
	'My title'

A rich library of prebuilt validators is supplied::

	>>> sanitize ('abcde', IsNonblank())
	'abcde'
	>>> sanitize (5, IsInRange(1,6))
	5
	>>> sanitize ('foo', Synonyms({'foo': 'bar', 'baz': 'quux'}))
	'bar'

Custom validators can easily be subclassed from a supplied base class::

	class IsFoo (BaseValidator):
		def validate_value (self, value):
			if value != 'foo':
				self.raise_validation_error (value)
			return True


Limitations
-----------

Certainly, far, far more complicated reproducibility tools are out there (see `here <http://csdl2.computer.org/comp/mags/cs/2009/01/mcs2009010005.pdf>__`) but many are based around certain disciplines (e.g. geophysics, computational math) or require working through web interfaces or using very standard sets of analysis tools. *psicons* is written from the point of view of a bioinformatician doing sequence
and phylogenetic analysis, working on the commandline using a lot of custom scripts and an endlessly changing lineup of supplied tools. As sometimes happens, other tools didn't fit, so I wrote one that did. It's served well in a limited
role. However, the API and future direction is completely up for grabs.


Credit
------

Thanks to the architects of Scons, of course.

While this project was started before encountering Madagascar, it has inevitably
shaped development. It's a remarkably powerful system, although ill-suited to
my current purposes. You should check it out.


References
----------

.. [konval-home] `konval home page <http://www.agapow.net/software/py-konval>`__

.. [konval-pypi] `konval on PyPi <http://pypi.python.org/pypi/konval>`__

.. [setuptools] `Setuptools & easy_install <http://packages.python.org/distribute/easy_install.html>`__

.. [konval-github] `konval on github <https://github.com/agapow/py-konval>`__

.. [formencode] `FormEncode <http://formencode.org>`__




