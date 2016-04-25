#!/usr/bin/env python3
from genling import *

segments = []

# Initial
phonemes = [
	Phoneme("_", 20),

	Phoneme("k", 5),
	Phoneme("s", 4),
	Phoneme("t", 4),
	Phoneme("n", 4),
	Phoneme("h", 3),
	Phoneme("m", 1),
	Phoneme("y", 1),
	Phoneme("r", 1),
	Phoneme("w", 1),
	Phoneme("g", 1),
	Phoneme("z", 1),
	Phoneme("d", 1),
	Phoneme("b", 1),
	Phoneme("p", 1)
]
segments.append(Segment(phonemes))

# Medial
phonemes = [
	Phoneme("_", 20),
	Phoneme("y", 1)
]
segments.append(Segment(phonemes))

# Nucleus
phonemes = [
	Phoneme("a", 5),
	Phoneme("i", 4),
	Phoneme("u", 4),
	Phoneme("e", 3),
	Phoneme("o", 3)
]
segments.append(Segment(phonemes))

# Coda
phonemes = [
	Phoneme("_", 10),

	Phoneme("n", 9),
	Phoneme("x", 3)
]
segments.append(Segment(phonemes))

syllables = [Syllable(segments, prefix="<", suffix=">")]

filters = [
	SimpleFilter("_y"),
	SimpleFilter("x>>"),

	SimpleFilter("n><_",0.9),

	SimpleFilter("<<d_[ui]"),
	SimpleFilter("d_i", 0.9),
	SimpleFilter("d_u", 0.9),

	SimpleFilter("mya", 0.95),
	SimpleFilter("myu", 0.95),

	RegexFilter("y_?[yie]"),
	RegexFilter("w_?[yiueo]"),

	RegexFilter("n><.y", 0.9, False),
	RegexFilter("x><.y"),
	RegexFilter("x><[^kstpc]")
]

syllable_balance = [2, 12, 8, 2, 1]

stem = Stem(syllables, balance=syllable_balance, filters=filters,
	prefix="<", suffix=">")

writing_systems = {}

# Hepburn
conversions = [
	SimpleReplace("n><_", "n'"),

	SimpleReplace("_", ""),

	SimpleReplace("si", "shi"),
	SimpleReplace("sy", "sh"),
	SimpleReplace("ti", "chi"),
	SimpleReplace("tu", "tsu"),
	SimpleReplace("hu", "fu"),
	SimpleReplace("ty", "ch"),
	SimpleReplace("zi", "ji"),
	SimpleReplace("zy", "j"),
	SimpleReplace("di", "ji"),
	SimpleReplace("du", "ju"),
	SimpleReplace("x><ch", "tch"),
	RegexReplace("x><(.)", "\\1\\1"),

	SimpleReplace("a><a", "ā"),
	SimpleReplace("o><u", "ī"),
	SimpleReplace("u><u", "ū"),
	SimpleReplace("e><e", "ē"),
	SimpleReplace("o><o", "ō"),
	SimpleReplace("o><u", "ō"),

	SimpleReplace("<", ""),
	SimpleReplace(">", "")
]
writing_systems["hepburn"] = conversions

# Hiragana
conversions = [
	SimpleReplace("_", ""),

	SimpleReplace("<ya", "や"),
	SimpleReplace("<yu", "ゆ"),
	SimpleReplace("<yo", "よ"),
	SimpleReplace("ya", "iゃ"),
	SimpleReplace("yu", "iゅ"),
	SimpleReplace("yo", "iょ"),

	SimpleReplace("<ka", "か"),
	SimpleReplace("<ki", "き"),
	SimpleReplace("<ku", "く"),
	SimpleReplace("<ke", "け"),
	SimpleReplace("<ko", "こ"),

	SimpleReplace("<sa", "さ"),
	SimpleReplace("<si", "し"),
	SimpleReplace("<su", "す"),
	SimpleReplace("<se", "せ"),
	SimpleReplace("<so", "そ"),

	SimpleReplace("<ta", "た"),
	SimpleReplace("<ti", "ち"),
	SimpleReplace("<tu", "つ"),
	SimpleReplace("<te", "て"),
	SimpleReplace("<to", "と"),

	SimpleReplace("<na", "な"),
	SimpleReplace("<ni", "に"),
	SimpleReplace("<nu", "ぬ"),
	SimpleReplace("<ne", "ね"),
	SimpleReplace("<no", "の"),

	SimpleReplace("<ha", "は"),
	SimpleReplace("<hi", "ひ"),
	SimpleReplace("<hu", "ふ"),
	SimpleReplace("<he", "へ"),
	SimpleReplace("<ho", "ほ"),

	SimpleReplace("<ma", "ま"),
	SimpleReplace("<mi", "み"),
	SimpleReplace("<mu", "む"),
	SimpleReplace("<me", "め"),
	SimpleReplace("<mo", "も"),

	SimpleReplace("<ra", "ら"),
	SimpleReplace("<ri", "り"),
	SimpleReplace("<ru", "る"),
	SimpleReplace("<re", "れ"),
	SimpleReplace("<ro", "ろ"),

	SimpleReplace("<wa", "わ"),
	SimpleReplace("<wo", "を"),
	SimpleReplace("n>", "ん"),
	SimpleReplace("x>", "っ"),

	SimpleReplace("<ga", "が"),
	SimpleReplace("<gi", "ぎ"),
	SimpleReplace("<gu", "ぐ"),
	SimpleReplace("<ge", "げ"),
	SimpleReplace("<go", "ご"),

	SimpleReplace("<za", "ざ"),
	SimpleReplace("<zi", "じ"),
	SimpleReplace("<zu", "ず"),
	SimpleReplace("<ze", "ぜ"),
	SimpleReplace("<zo", "ぞ"),

	SimpleReplace("<da", "だ"),
	SimpleReplace("<di", "ぢ"),
	SimpleReplace("<du", "づ"),
	SimpleReplace("<de", "で"),
	SimpleReplace("<do", "ど"),

	SimpleReplace("<ba", "ば"),
	SimpleReplace("<bi", "び"),
	SimpleReplace("<bu", "ぶ"),
	SimpleReplace("<be", "べ"),
	SimpleReplace("<bo", "ぼ"),

	SimpleReplace("<pa", "ぱ"),
	SimpleReplace("<pi", "ぴ"),
	SimpleReplace("<pu", "ぷ"),
	SimpleReplace("<pe", "ぺ"),
	SimpleReplace("<po", "ぽ"),

	SimpleReplace("<a", "あ"),
	SimpleReplace("<i", "い"),
	SimpleReplace("<u", "う"),
	SimpleReplace("<e", "え"),
	SimpleReplace("<o", "お"),

	SimpleReplace("<", ""),
	SimpleReplace(">", "")
]
writing_systems["hiragana"] = conversions

# Strict(Nihon/Kunrei-shiki)
conversions = [
	SimpleReplace("n><_", "n'"),

	SimpleReplace("_", ""),

	RegexReplace("x><(.)", "\\1\\1"),

	SimpleReplace("<", ""),
	SimpleReplace(">", "")
]
writing_systems["strict"] = conversions


from sys import argv

if len(argv) > 1:
	amount = int(argv[1])
else:
	amount = 10

conversions = writing_systems["hiragana"]
if len(argv) > 2:
	if argv[2] in writing_systems:
		conversions = writing_systems[argv[2]]
	elif argv[2] == "raw":
		conversions = []

for i in range(amount):
	word = stem.generate()
	for c in conversions:
		word = c.replace(word)
	print(word)
