from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='psicons.core',
	version=version,
	description="A tool for documentable and reproducible analysis and research",
	long_description=open("README.txt").read() + "\n" +
		open(os.path.join("docs", "HISTORY.txt")).read(),
	# Get more strings from
	# http://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		"Programming Language :: Python",
		"Development Status :: 3 - Alpha",
		"Environment :: Console",
		"License :: OSI Approved :: MIT License",
		"Topic :: Scientific/Engineering",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Information Analysis",
		"Topic :: Software Development :: Build Tools",
	],
	keywords='reproducibility documentable',
	author='',
	author_email='',
	url='http://svn.plone.org/svn/collective/',
	license='GPL',
	packages=find_packages(exclude=['ez_setup']),
	namespace_packages=['psicons'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
	'setuptools',
		# -*- Extra requirements: -*-
	],
	entry_points="""
		# -*- Entry points: -*-
	""",
	test_suite='nose.collector',
)
