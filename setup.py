#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="genling",
	version="1.0.1",
	
	author="Seán Hewitt",
	author_email="contact@2sh.me",
	
	description="Generatrum Linguarum, a conlang word generator library",
	long_description=long_description,
	long_description_content_type="text/markdown",
	
	url="https://github.com/2sh/genling",
	
	packages=["genling"],
	
	python_requires='>=3',
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent"
	)
)
