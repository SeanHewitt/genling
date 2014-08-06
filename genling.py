#! /usr/bin/env python3
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

from stem import *
from writing_system import *
from yaml import load as yaml_decode
from sys import argv

language_config = argv[1]
writing_system_index = int(argv[2])
stem_count = int(argv[3])

with open(language_config) as f:
	language = yaml_decode(f)

syllables = list()
for syllable in language["stem"]["syllables"]:
	if "segments" not in syllable:
		continue
	
	segments = list()
	for segment in syllable["segments"]:
		if "phonemes" not in segment:
			continue
		
		phonemes = list()
		for phoneme in segment["phonemes"]:
			if "grapheme" not in phoneme:
				continue
			
			phonemes.append(Phoneme(
				phoneme["grapheme"], segment.get("weight", 1)))
			
		segments.append(Segment(phonemes, segment.get("probability", 1.0),
			segment.get("prefix", ""), segment.get("suffix", "")))
	
	syllables.append(Syllable(segments, syllable.get("position", 0),
		syllable.get("prefix", ""), syllable.get("suffix", ""), syllable.get("infix", "")))

syllable_balance = language["stem"].get("syllable-balance", [1,1,1,1])

filters = list()
for filt in language["stem"]["filters"]:
	probability = filt.get("probability", 1.0)
	allow = filt.get("allow", False)
	if("regex" in filt):
		filters.append(RegexFilter(filt["regex"],
			probability, allow))

prefix = language["stem"].get("prefix", "")
suffix = language["stem"].get("suffix", "")
infix = language["stem"].get("infix", "")

stem = Stem(syllables, syllable_balance, filters, prefix, suffix, infix)

writing_systems = list()
for writing_system in language["writing-systems"]:
	if "transliterations" not in writing_system:
		continue
		
	transliterations = list()
	for transliteration in writing_system["transliterations"]:
		try:
			replacement = transliteration["replacement"]
		except:
			continue
		probability = transliteration.get("probability", 1.0)
			
		if "regex" in transliteration:
			transliterations.append(RegexTransliteration(
				transliteration["regex"], replacement, probability))
			
	writing_systems.append(WritingSystem(transliterations))

for i in range(stem_count):
	string = stem.generate()
	if writing_system_index > 0:
		string = writing_systems[writing_system_index-1].transliterate(string)
	print(string)
