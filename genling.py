#
#	Generatrum Linguarum, a conlang word generator library
#	Copyright (C) 2014-2017 Sean Hewitt <contact@SeanHewitt.com>
#
#	This library is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This library is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this library.  If not, see <http://www.gnu.org/licenses/>.
#

import random
import re

def _weighted_choice(choices):
	r = random.random() * sum(choices)
	for i, w in enumerate(choices):
		r -= w
		if r < 0:
			return i
	return None

class Phoneme:
	"""The phoneme of a segment.
	
	Args:
		grapheme: The graphical representation.
		weight: The likelihood of being chosen as a segment of a syllable.
	"""
	def __init__(self, grapheme, weight = 1):
		self.grapheme = grapheme
		self.weight = weight

class Segment:
	"""The segment within a syllable.
	
	Args:
		phonemes: The phonemes of the segment.
		prefix: The preceding string.
		suffix: The following string.
	"""
	def __init__(self, phonemes, prefix = "", suffix = ""):
		self.phonemes = phonemes
		self.prefix = prefix
		self.suffix = suffix

	def generate(self):
		"""Generate a segment by choosing one of its phonemes.
		
		Returns:
			The generated segment.
		"""
		weights = [phoneme.weight for phoneme in self.phonemes]
		return self.prefix + self.phonemes[_weighted_choice(weights)].grapheme + self.suffix

class Syllable:
	"""The syllable within a stem.
	
	Args:
		segments: The segments of the syllable.
		position: The position of the syllable with a stem.
		weight: The likelihood of being chosen as a syllable in a stem.
		prefix: The preceding string.
		suffix: The following string.
		infix: The string between the segments.
	"""
	def __init__(self, segments, position = 0, weight = 1,
			prefix = "", suffix = "", infix = ""):
		self.segments = segments
		self.position = position
		self.weight = weight
		self.prefix = prefix
		self.suffix = suffix
		self.infix = infix

	def is_permitted_position(self, i, length):
		"""Check if this syllable is permitted in the stem's position.
		
		Args:
			i: The position within the stem.
			length: The number of syllables with the stem.
			
		Returns:
			If this syllable is permitted.
		"""
		if self.position == 0:
			return True

		if isinstance(self.position, int):
			position = self.position if self.position > 0 else length+self.position+1
			if position == (i+1):
				return True

		elif(not isinstance(self.position, basestring) and
				len(self.position) > 1):
			minpos = self.position[0] if self.position[0] > 0 else l+self.position[0]+1
			maxpos = self.position[1] if self.position[1] > 0 else l+self.position[1]+1

			if minpos <= (i+1) <= maxpos:
				return True

		return False

	def generate(self):
		"""Generate a syllable by its segments.
		
		Returns:
			The generated syllable.
		"""
		string = [segment.generate() for segment in self.segments]
		return self.prefix + self.infix.join(string) + self.suffix

class Stem:
	"""The stem of a word.
	
	Args:
		syllables: The syllables of the stem.
		balance: The balance of stem length.
		filters: The filters for permitting or rejecting stems.
		prefix: The preceding string.
		suffix: The following string.
		infix: The string between the syllables.
	"""
	def __init__(self, syllables, balance = [1], filters = [],
			prefix = "", suffix = "", infix = ""):
		self.syllables = syllables
		self.balance = balance
		self.filters = filters
		self.prefix =  prefix
		self.suffix = suffix
		self.infix = infix

	def generate(self):
		"""Generate a stem by its syllables.
		
		Returns:
			The generated stem.
		"""
		for i in range(100):
			stem = self._generate()
			for f in self.filters:
				if f.is_rejected(stem):
					break
			else:
				return stem
		raise Exception("Too many filter rejected stems.")

	def _generate(self):
		syllable_amount = _weighted_choice(self.balance) + 1

		string = list()
		for i in range(syllable_amount):
			syllables = list()
			weights = list()
			for syllable in self.syllables:
				if not syllable.is_permitted_position(i, syllable_amount):
					continue
				syllables.append(syllable)
				weights.append(syllable.weight)
			
			if len(syllables) > 1:
				syllable = syllables[_weighted_choice(weights)]
			else:
				syllable = syllables[0]
			
			string.append(syllable.generate())

		return self.prefix + self.infix.join(string) + self.suffix

class SimpleFilter:
	"""A filter to permit or reject strings containing a string.
	
	Args:
		pattern: The pattern to match.
		probability: The probability that this filter takes effect.
		permit: If this filter should permit instead of reject.
	"""
	def __init__(self, pattern, probability = 1.0, permit = False):
		self.pattern = pattern
		self.probability = probability
		self.permit = permit

	def is_permitted(self, string):
		"""Check if the string is permitted.
		
		Args:
			string: The string to check.
			
		Returns:
			If the string is permitted.
		"""
		if random.random() > self.probability:
			return not self.permit
		if self._match(string):
			return self.permit
		else:
			return not self.permit

	def is_rejected(self, string):
		"""Check if the string is rejected.
		
		Args:
			string: The string to check.
			
		Returns:
			If the string is rejected.
		"""
		return not self.is_permitted(string)

	def _match(self, string):
		"""Overloadable match method.
		
		This method can be overloaded to define an alternative
		implementation of matching the pattern within an input string.
		
		Args:
			string: The string to check.
		"""
		return self.pattern in string
	
		
	def _prepare(self):
		"""Overloadable prepare method.
		
		This method is run after the filter pattern is defined.
		"""
		pass

	@property
	def pattern(self):
		return self._pattern

	@pattern.setter
	def pattern(self, pattern):
		self._pattern = pattern
		self._prepare()

class RegexFilter(SimpleFilter):
	"""A filter to permit or reject strings matching a regex pattern."""
	def _match(self, string):
		return self._regex.search(string)

	def _prepare(self):
		self._regex = re.compile(self.pattern)

class SimpleReplace:
	"""A checker for replacing a matching string within strings.
	
	Args:
		pattern: The pattern to match.
		repl: The replacement string.
		probability: The probability that the matched string is replaced.
	"""
	def __init__(self, pattern, repl, probability = 1.0):
		self.pattern = pattern
		self.repl = repl
		self.probability = probability

	def apply(self, string):
		"""Replace the matching parts of the string.
		
		Args:
			string: The string to check.
			
		Returns:
			The replaced string.
		"""
		if random.random() > self.probability:
			return string

		return self._replace(string)

	def _replace(self, string):
		"""Overloadable replace method.
		
		This method can be overloaded to define an alternative
		implementation of replacing the pattern within an input string.
		
		Args:
			string: The string to replace.
		"""
		return string.replace(self.pattern, self.repl)

	def _prepare(self):
		"""Overloadable prepare method.
		
		This method is run after the replace pattern is defined.
		"""
		pass

	@property
	def pattern(self):
		return self._pattern

	@pattern.setter
	def pattern(self, pattern):
		self._pattern = pattern
		self._prepare()

class RegexReplace(SimpleReplace):
	"""A checker for replacing a matching regex pattern within strings."""
	def _replace(self, string):
		return self._regex.sub(self.repl, string)

	def _prepare(self):
		self._regex = re.compile(self.pattern)
