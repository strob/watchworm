#!/usr/bin/env python

import distutils.core
distutils.core.setup(
    name='watchworm',
    version='7.0',
    url='http://github.com/strob/watchworm',
    description='why watch worms?',
    author='Robert M Ochshorn',
    author_email='mail@RMOZONE.COM',
    packages=['watchworm'],
    scripts=['bin/wormwatch'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    keywords='opencv blobs tracking motion analysis',
    license='GPL')
