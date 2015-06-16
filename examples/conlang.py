#!/usr/bin/env python3
from genling import *

syllables = []

# First syllable of stem
segments = []

# Initial
phonemes = [
	Phoneme("j", 1),
	Phoneme("h", 1),
	Phoneme("c", 1), # C
]
segments.append(Segment(phonemes, probability=0.1))

# Medial
phonemes = [
	Phoneme("", 20),

	Phoneme("t", 5),  # t
	Phoneme("tc", 2), # t_hC
	Phoneme("th", 5), # t_h
	Phoneme("tj", 2), # t_h_j

	Phoneme("d", 6),  # d
	Phoneme("dj", 2), # d_j

	Phoneme("k", 5),
	Phoneme("kc", 2),
	Phoneme("kh", 4),
	Phoneme("kj", 2),
	Phoneme("kT", 4), # k_hT

	Phoneme("g", 6),
	Phoneme("gc", 2),
	Phoneme("gj", 3),

	Phoneme("f", 5),
	Phoneme("fc", 2),
	Phoneme("fh", 3),
	Phoneme("fj", 3),

	Phoneme("v", 3),
	Phoneme("vj", 1),

	Phoneme("p", 4),
	Phoneme("pc", 2), # p_hC
	Phoneme("ph", 2), # p_h
	Phoneme("pj", 1), # p\j
	Phoneme("pf", 1), # p\f

	Phoneme("b", 6),
	Phoneme("bj", 2),

	Phoneme("h", 5),

	Phoneme("s", 5),  # S
	Phoneme("sh", 4), # S_h
	Phoneme("sj", 1), # S_h_j
	Phoneme("st", 2),
	Phoneme("sk", 2),
	Phoneme("sf", 2),
	Phoneme("sp", 1),
	Phoneme("sn", 3),
	Phoneme("sm", 4),

	Phoneme("T", 4),  # T
	Phoneme("Tj", 2), # T_j

	Phoneme("D", 5),  # D
	Phoneme("Dj", 2), # D_j

	Phoneme("l", 7),
	Phoneme("lc", 6), # K
	Phoneme("lh", 4),
	Phoneme("lj", 4),

	Phoneme("n", 6),
	Phoneme("nh", 5),
	Phoneme("nj", 3),

	Phoneme("m", 4),
	Phoneme("my", 2),

	Phoneme("j", 5),  # j

	Phoneme("r", 2),  # 4
	Phoneme("rh", 3),
	Phoneme("rj", 3)
]
segments.append(Segment(phonemes))

# Nucleus
phonemes = [
	Phoneme("a", 5),  # a
	Phoneme("A", 3),  # @
	Phoneme("i", 4),  # I
	Phoneme("ie", 2), # i
	Phoneme("u", 4),  # U
	Phoneme("e", 3),  # E
	Phoneme("o", 3),  # O
	Phoneme("ea", 2), # Ea
	Phoneme("oe", 2), # 9
	Phoneme("y", 2)  # Y
]
segments.append(Segment(phonemes))

# Coda
phonemes = [
	Phoneme("n", 6),
	Phoneme("l", 4),
	Phoneme("x", 6), # repeater
	Phoneme("c", 1),
	Phoneme("h", 2),
	Phoneme("r", 3)
]
segments.append(Segment(phonemes, probability=0.5))

syllables.append(Syllable(segments, position=1))


# Second syllable of stem
segments = []

# Initial
phonemes = [
	Phoneme("t", 4),
	Phoneme("tj", 2),

	Phoneme("d", 5),
	Phoneme("dj", 1),

	Phoneme("k", 4),
	Phoneme("kj", 3),

	Phoneme("g", 6),
	Phoneme("gj", 1),

	Phoneme("f", 4),
	Phoneme("fj", 2),

	Phoneme("p", 4),
	Phoneme("pj", 1),

	Phoneme("b", 4),
	Phoneme("bj", 1),

	Phoneme("s", 5),
	Phoneme("sj", 2),

	Phoneme("T", 4),
	Phoneme("Tj", 1),

	Phoneme("D", 3),
	Phoneme("Dj", 1),

	Phoneme("l", 7),
	Phoneme("lc", 2),
	Phoneme("lj", 3),

	Phoneme("n", 8),
	Phoneme("nj", 3),

	Phoneme("m", 6),
	Phoneme("mj", 3),

	Phoneme("j", 3),

	Phoneme("r", 2),
	Phoneme("rj", 1)
]
segments.append(Segment(phonemes))

# Nucleus
phonemes = [
	Phoneme("a", 5),
	Phoneme("A", 5),
	Phoneme("e", 3),
	Phoneme("o", 3)
]
segments.append(Segment(phonemes))

syllables.append(Syllable(segments, position=2))

syllable_balance = [5, 2]
stem = Stem(syllables, infix=">", balance=syllable_balance)

filters = [
	RegexFilter("x$"),
	RegexFilter("h$"),
	RegexFilter("c$"),

	SimpleFilter("n>m"),

	SimpleFilter("cs"),

	SimpleFilter("l>l"),
	SimpleFilter("r>r"),
	SimpleFilter("l>r"),
	SimpleFilter("x>r")
]

conversions = [
	SimpleReplace("A", "ı"),
	SimpleReplace("oe", "ø"),

	SimpleReplace("T", "þ"),
	SimpleReplace("D", "ð"),

	RegexReplace("x>(.)", "\\1\\1"),

	SimpleReplace(">", "")
]

from sys import argv

amount = int(argv[1])

if(len(argv) > 2 and argv[2] == "raw"):
	conversions = []

while amount:
	string = stem.generate()
	for f in filters:
		if f.is_rejected(string):
			break
	else:
		for c in conversions:
			string = c.replace(string)
		print(string)
		amount -= 1;
