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
	def __init__(self, phonemes, **prop):
		self.phonemes = phonemes
		self.probability = prop.get("probability", 1.0)
		self.prefix = prop.get("prefix", "")
		self.suffix = prop.get("suffix", "")
		
	def generate(self):
		weights = [phoneme.weight for phoneme in self.phonemes]
		return self.prefix + self.phonemes[weighted_choice(weights)].grapheme + self.suffix
		
class Syllable:
	def __init__(self, segments, **prop):
		self.segments = segments
		self.position = prop.get("position", 0)
		self.weight = prop.get("weight", 1)
		self.prefix = prop.get("prefix", "")
		self.suffix = prop.get("suffix", "")
		self.infix = prop.get("infix", "")
	
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
	def __init__(self, syllables, **prop):
		self.syllables = syllables
		self.filters = prop.get("filters", [])
		self.syllable_balance = prop.get("syllable-balance", [1])
		self.prefix =  prop.get("prefix", "")
		self.suffix = prop.get("suffix", "")
		self.infix = prop.get("infix", "")
		
	def generate(self):
		syllable_amount = weighted_choice(self.syllable_balance) + 1
		
		tries = 0
		while tries < 100:
			tries+=1
			string = list()
			for i in range(syllable_amount):
				syllables = [syllable for syllable in self.syllables if syllable.position in [0, i+1, i - syllable_amount]]
				if(len(syllables) > 1):
					weights = [syllable.weight for syllable in syllables]
					syllable = self.syllables[weighted_choice(weights)]
				else:
					syllable = syllables[0]
					
				string.append(syllable.generate())
					
			string = self.prefix + self.infix.join(string) + self.suffix
			
			for f in self.filters:
				if not f.is_allowed(string):
					break
			else:
				break
		else:
			string = None
		return string
