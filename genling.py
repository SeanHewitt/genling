#
#	Generatrum Linguarum, a conlang word generator library
#	Copyright (C) 2014-2016 Sean Hewitt <contact@SeanHewitt.com>
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

from random import random
from re import compile as re_compile

def _weighted_choice(choices):
	r = random() * sum(choices)
	for i, w in enumerate(choices):
		r -= w
		if r < 0:
			return i
	return None

class Phoneme:
	"""The phoneme of a segment."""
	def __init__(self,
			grapheme: "the graphical representation",
			weight: "the likelihood of being chosen as a segment of a syllable" = 1):
		self.grapheme = grapheme
		self.weight = weight

class Segment:
	"""The segment within a syllable."""
	def __init__(self,
			phonemes: "the phonemes of the segment",
			prefix: "the preceding string" = "",
			suffic: "the following string" = ""):
		self.phonemes = phonemes
		self.prefix = prefix
		self.suffix = suffix

	def generate(self) -> "the generated segment":
		"""Generate a segment by choosing one of its phonemes."""
		weights = [phoneme.weight for phoneme in self.phonemes]
		return self.prefix + self.phonemes[_weighted_choice(weights)].grapheme + self.suffix

class Syllable:
	"""The syllable within a stem."""
	def __init__(self,
			segments: "the segments of the syllable",
			position: "the position of the syllable with a stem" = 0,
			weight: "the likelihood of being chosen as a syllable in a stem" = 1,
			prefix: "the preceding string" = "",
			suffix: "the following string" = "",
			infix: "the string between the segments" = ""):
		self.segments = segments
		self.position = position
		self.weight = weight
		self.prefix = prefix
		self.suffix = suffix
		self.infix = infix

	def is_permitted_position(self,
			i: "the position within the stem",
			length: "the number of syllables with the stem"
		) -> "if this syllable is permitted":
		"""Check if this this syllable is permitted in the stem's position."""
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

	def generate(self) -> "the generated syllable":
		"""Generate a syllable by its segments."""
		string = [segment.generate() for segment in self.segments]
		return self.prefix + self.infix.join(string) + self.suffix

class Stem:
	"""The stem of a word."""
	def __init__(self,
			syllables: "the syllables of the stem",
			balance: "the balance of stem length" = [1],
			filters: "the filters for permitting or rejecting stems" = [],
			prefix: "the preceding string" = "",
			suffix: "the following string" = "",
			infix: "the string between the syllables" = ""):
		self.syllables = syllables
		self.balance = balance
		self.filters = filters
		self.prefix =  prefix
		self.suffix = suffix
		self.infix = infix

	def generate(self) -> "the generated stem":
		"""Generate a stem by its syllables."""
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
	"""A filter to permit or reject strings containing a string."""
	def __init__(self,
			pattern: "the pattern to match",
			probability: "the probability that this filter takes effect" = 1.0,
			permit: "if this filter should permit instead of reject" = False):
		self.pattern = pattern
		self.probability = probability
		self.permit = permit

	def is_permitted(self,
			string: "the string to check") -> "if the string is permitted":
		"""Check if the string is permitted."""
		if random() > self.probability:
			return not self.permit
		if self._match(string):
			return self.permit
		else:
			return not self.permit

	def is_rejected(self,
			string: "the string to check") -> "if the string is rejected":
		"""Check if the string is rejected."""
		return not self.is_permitted(string)

	def _match(self, string):
		return self.pattern in string

	def _prepare(self):
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
		self._regex = re_compile(self.pattern)

class SimpleReplace:
	"""A checker for replacing a matching string within strings."""
	def __init__(self,
			pattern: "the pattern to match",
			replacement: "the replacement string",
			probability: "the probability that the matched string is replaced" = 1.0):
		self.pattern = pattern
		self.replacement = replacement
		self.probability = probability

	def replace(self,
			string: "the string to check") -> "the replaced string":
		"""Replace the matching parts of the string."""
		if random() > self.probability:
			return string

		return self._replace(string, self.replacement)

	def _replace(self, string, replacement):
		return string.replace(self.pattern, replacement)

	def _prepare(self):
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
	def _replace(self, string, replacement):
		return self._regex.sub(replacement, string)

	def _prepare(self):
		self._regex = re_compile(self.pattern)
