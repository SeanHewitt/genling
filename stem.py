#
#	Copyright 2010 Sean Hewitt <contact@SeanHewitt.com>
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#	

from rand import weighted_choice
from random import random
from re import compile as re_compile

class Phoneme:
	def __init__(self, grapheme, weight=1):
		self.grapheme = grapheme
		self.weight = weight
		
class Segment:
	def __init__(self, phonemes, probability=1.0, prefix="", suffix=""):
		self.phonemes = phonemes
		self.probability = probability
		self.prefix = prefix
		self.suffix = suffix
		
	def generate(self):
		weights = [phoneme.weight for phoneme in self.phonemes]
		return self.prefix + self.phonemes[weighted_choice(weights)].grapheme + self.suffix
		
class Syllable:
	def __init__(self, segments, position=0, prefix="", suffix="", infix=""):
		self.segments = segments
		self.position = position
		self.prefix = prefix
		self.suffix = suffix
		self.infix = infix
	
	def generate(self):
		string = [segment.generate() for segment in self.segments if random() <= segment.probability]
		return self.prefix + self.infix.join(string) + self.suffix
		
class RegexFilter:
	def __init__(self, pattern, probability=1.0, allow=False):
		self.pattern = pattern
		self.probability = probability
		self.allow = allow
		
	def is_allowed(self, stem_string):
		if random() > self.probability:
			return not self.allow
		if self.regex.search(stem_string):
			return self.allow
		else:
			return not self.allow
			
	@property
	def pattern(self):
		return self._pattern
		
	@pattern.setter
	def pattern(self, pattern):
		self._pattern = pattern
		self.regex = re_compile(pattern)
		
class Stem:
	def __init__(self, syllables, syllable_balance, filters=[], prefix="", suffix="", infix=""):
		self.syllables = syllables
		self.syllable_balance = syllable_balance
		self.filters = filters
		self.prefix = prefix
		self.suffix = suffix
		self.infix = infix
		
	def generate(self):
		syllable_amount = weighted_choice(self.syllable_balance) + 1
		
		is_allowed = False
		while not is_allowed:
			string = list()
			is_allowed = True
			for i in range(syllable_amount):
				for syllable in self.syllables:
					if(syllable.position == 0 or
					   syllable.position == i + 1 or
					   syllable.position == i - syllable_amount):
						string.append(syllable.generate())
						break
					
			string = self.prefix + self.infix.join(string) + self.suffix
			
			for f in self.filters:
				if not f.is_allowed(string):
					is_allowed = False
					break
		return string
