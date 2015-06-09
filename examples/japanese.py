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
	RegexFilter("<Y"),
	RegexFilter("x><[^kstpc]"),
  
	RegexFilter("mYu", 0.95),
	RegexFilter("di", 0.9),
	RegexFilter("du", 0.9),
	RegexFilter("^<d[ui]")
]

writing_systems = {}

# Hepburn
transliterations = [
	RegexTransliteration("si", "shi"),
	RegexTransliteration("sY", "sh"),
	RegexTransliteration("ti", "chi"),
	RegexTransliteration("hu", "fu"),
	RegexTransliteration("tY", "ch"),
	RegexTransliteration("zi", "ji"),
	RegexTransliteration("zY", "j"),
	RegexTransliteration("d([iu])", "j\\1"),
	RegexTransliteration("N><([aiueo])", "n'><\\1"),
	RegexTransliteration("x><ch", "t><ch"),
	RegexTransliteration("x><(.)(.?)", "\\1><\\1\\2"),
	RegexTransliteration("Y", "y"),
	RegexTransliteration("N", "n"),

	RegexTransliteration("a><a", "ā"),
	RegexTransliteration("u><u", "ū"),
	RegexTransliteration("e><e", "ē"),
	RegexTransliteration("o><[ou]", "ō"),

	RegexTransliteration("[<>]", "")
]
writing_systems["hepburn"] = WritingSystem(transliterations)

# Hiragana
transliterations = [
	RegexTransliteration("<ya", "や"),
	RegexTransliteration("<yu", "ゆ"),
	RegexTransliteration("<yo", "よ"),
	RegexTransliteration("Ya", "iゃ"),
	RegexTransliteration("Yu", "iゅ"),
	RegexTransliteration("Yo", "iょ"),

	RegexTransliteration("<ka", "か"),
	RegexTransliteration("<ki", "き"),
	RegexTransliteration("<ku", "く"),
	RegexTransliteration("<ke", "け"),
	RegexTransliteration("<ko", "こ"),

	RegexTransliteration("<sa", "さ"),
	RegexTransliteration("<si", "し"),
	RegexTransliteration("<su", "す"),
	RegexTransliteration("<se", "せ"),
	RegexTransliteration("<so", "そ"),

	RegexTransliteration("<ta", "た"),
	RegexTransliteration("<ti", "ち"),
	RegexTransliteration("<tu", "つ"),
	RegexTransliteration("<te", "て"),
	RegexTransliteration("<to", "と"),

	RegexTransliteration("<na", "な"),
	RegexTransliteration("<ni", "に"),
	RegexTransliteration("<nu", "ぬ"),
	RegexTransliteration("<ne", "ね"),
	RegexTransliteration("<no", "の"),

	RegexTransliteration("<ha", "は"),
	RegexTransliteration("<hi", "ひ"),
	RegexTransliteration("<hu", "ふ"),
	RegexTransliteration("<he", "へ"),
	RegexTransliteration("<ho", "ほ"),

	RegexTransliteration("<ma", "ま"),
	RegexTransliteration("<mi", "み"),
	RegexTransliteration("<mu", "む"),
	RegexTransliteration("<me", "め"),
	RegexTransliteration("<mo", "も"),

	RegexTransliteration("<ra", "ら"),
	RegexTransliteration("<ri", "り"),
	RegexTransliteration("<ru", "る"),
	RegexTransliteration("<re", "れ"),
	RegexTransliteration("<ro", "ろ"),

	RegexTransliteration("<wa", "わ"),
	RegexTransliteration("<wo", "を"),
	RegexTransliteration("N>", "ん"),
	RegexTransliteration("x>", "っ"),

	RegexTransliteration("<ga", "が"),
	RegexTransliteration("<gi", "ぎ"),
	RegexTransliteration("<gu", "ぐ"),
	RegexTransliteration("<ge", "げ"),
	RegexTransliteration("<go", "ご"),

	RegexTransliteration("<za", "ざ"),
	RegexTransliteration("<zi", "じ"),
	RegexTransliteration("<zu", "ず"),
	RegexTransliteration("<ze", "ぜ"),
	RegexTransliteration("<zo", "ぞ"),

	RegexTransliteration("<da", "だ"),
	RegexTransliteration("<di", "ぢ"),
	RegexTransliteration("<du", "づ"),
	RegexTransliteration("<de", "で"),
	RegexTransliteration("<do", "ど"),

	RegexTransliteration("<ba", "ば"),
	RegexTransliteration("<bi", "び"),
	RegexTransliteration("<bu", "ぶ"),
	RegexTransliteration("<be", "べ"),
	RegexTransliteration("<bo", "ぼ"),

	RegexTransliteration("<pa", "ぱ"),
	RegexTransliteration("<pi", "ぴ"),
	RegexTransliteration("<pu", "ぷ"),
	RegexTransliteration("<pe", "ぺ"),
	RegexTransliteration("<po", "ぽ"),

	RegexTransliteration("<a", "あ"),
	RegexTransliteration("<i", "い"),
	RegexTransliteration("<u", "う"),
	RegexTransliteration("<e", "え"),
	RegexTransliteration("<o", "お"),

	RegexTransliteration("[<>]", "")
]
writing_systems["hiragana"] = WritingSystem(transliterations)

# Strict(Nihon/Kunrei-shiki)
transliterations = [
	RegexTransliteration("N><([aiueo])", "n'><\\1"),
	RegexTransliteration("x><(.)(.?)", "\\1><\\1\\2"),
	RegexTransliteration("Y", "y"),
	RegexTransliteration("N", "n"),

	RegexTransliteration("[<>]", "")
]
writing_systems["strict"] = WritingSystem(transliterations)


from sys import argv

amount = int(argv[1])

if(len(argv) > 2 and argv[2] in writing_systems):
	writing_system = writing_systems[argv[2]]
else:
	writing_system = None

while amount:
	string = stem.generate()
	for f in filters:
		if not f.is_allowed(string):
			break
	else:
		if writing_system:
			string = writing_system.transliterate(string)
		print(string)
		amount -= 1;
