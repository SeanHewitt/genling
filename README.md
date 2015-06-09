#Generatrum Linguarum

This is a project to develop a Python library with which it is possible to generate a spoken constructed language, a conlang. In the library's current state, it is possible to program a word stem generator.

In the generating process, weights and probabilities affect the usage of individual phonemes, usage of syllable segments, usage of syllables in the same position, the amount of syllables within a stem and whether a stem caught by a filter is to be allowed. Regex is used for deciding whether a generated word stem is allowed or not (e.g. combinations of phonemes that are not permitted) and in transliterating a generated word/stem from a raw form (e.g. "&lt;ge&gt;&lt;hYo&gt;&lt;uN&gt;&lt;e&gt;&lt;nu&gt;") into a final form (e.g. "gehyōn'enu", "げひょうんえぬ", "gexyoungënu" or "гэхёунъэну").

Requirements:
* Python3

###Examples
````
python3 conlang.py 100 raw
python3 conlang.py 100
python3 japanese.py 100 hiragana
```
