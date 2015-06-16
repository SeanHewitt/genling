#!/usr/bin/env python3
from genling import *

segments = []

# Initial
phonemes = [
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
segments.append(Segment(phonemes, probability=0.8))

# Medial
phonemes = [
	Phoneme("Y", 1)
]
segments.append(Segment(phonemes, probability=0.005))

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
	Phoneme("N", 9),
	Phoneme("x", 1)
]
segments.append(Segment(phonemes, probability=0.1))

syllables = [Syllable(segments, prefix="<", suffix=">")]

syllable_balance = [2, 12, 8, 2, 1]
stem = Stem(syllables, balance=syllable_balance)

filters = [
	RegexFilter("[yY][Yie]"),
	RegexFilter("<w[Yiueo]"),
	RegexFilter("x>$"),
	RegexFilter("N><.Y", 0.9, False),
	RegexFilter("x><.Y"),
	SimpleFilter("<Y"),
	RegexFilter("x><[^kstpc]"),

	SimpleFilter("mYu", 0.95),
	SimpleFilter("di", 0.9),
	SimpleFilter("du", 0.9),
	RegexFilter("^<d[ui]")
]

writing_systems = {}

# Hepburn
conversions = [
	SimpleReplace("si", "shi"),
	SimpleReplace("sY", "sh"),
	SimpleReplace("ti", "chi"),
	SimpleReplace("tu", "tsu"),
	SimpleReplace("hu", "fu"),
	SimpleReplace("tY", "ch"),
	SimpleReplace("zi", "ji"),
	SimpleReplace("zY", "j"),
	RegexReplace("d([iu])", "j\\1"),
	RegexReplace("N><([aiueo])", "n'><\\1"),
	SimpleReplace("x><ch", "t><ch"),
	RegexReplace("x><(.)(.?)", "\\1><\\1\\2"),
	SimpleReplace("Y", "y"),
	SimpleReplace("N", "n"),

	SimpleReplace("a><a", "ā"),
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
	SimpleReplace("<ya", "や"),
	SimpleReplace("<yu", "ゆ"),
	SimpleReplace("<yo", "よ"),
	SimpleReplace("Ya", "iゃ"),
	SimpleReplace("Yu", "iゅ"),
	SimpleReplace("Yo", "iょ"),

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
	SimpleReplace("N>", "ん"),
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
	RegexReplace("N><([aiueo])", "n'><\\1"),
	RegexReplace("x><(.)(.?)", "\\1><\\1\\2"),
	SimpleReplace("Y", "y"),
	SimpleReplace("N", "n"),

	SimpleReplace("<", ""),
	SimpleReplace(">", "")
]
writing_systems["strict"] = conversions


from sys import argv

amount = int(argv[1])

conversions = writing_systems["hiragana"]
if len(argv) > 2:
	if argv[2] in writing_systems:
		conversions = writing_systems[argv[2]]
	elif argv[2] == "raw":
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
