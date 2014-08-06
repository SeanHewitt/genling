#
#	Copyright 2014 Sean Hewitt <contact@SeanHewitt.com>
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

from random import random
from re import compile as re_compile

class RegexTransliteration:
	def __init__(self, pattern, replacement, probability=1.0):
		self.pattern = pattern
		self.replacement = replacement
		self.probability = probability
		
	def transliterate(self, string):
		if random() > self.probability:
			return string
		
		return self.regex.sub(self.replacement, string)
		
	@property
	def pattern(self):
		return self._pattern
		
	@pattern.setter
	def pattern(self, pattern):
		self._pattern = pattern
		self.regex = re_compile(pattern)
		
class WritingSystem:
	def __init__(self, transliterations):
		self.transliterations = transliterations
		
	def transliterate(self, string):
		for transliteration in self.transliterations:
			string = transliteration.transliterate(string)
		return string
