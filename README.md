# Generatrum Linguarum
This is a project to develop a Python library with which it is possible to generate a spoken constructed language, a conlang. In the library's current state, it is possible to program a word generator.

In the generating process, weights and probabilities affect the usage of individual phonemes, usage of syllable segments, usage of syllables in the same position, the amount of syllables within a stem and the usage of rules. Simple or more complex Regex rules are used for filtering generated word stems (e.g. combinations of phonemes that are not permitted) and in converting a generated word/stem from a raw form (e.g. "&lt;ge&gt;&lt;hYo&gt;&lt;uN&gt;&lt;e&gt;&lt;nu&gt;") into a final form (e.g. "gehyōn'enu", "げひょうんえぬ", "gexyoungënu" or "гэхёунъэну").

The title of this project is in Latin and translates to "Generator of Languages".

## Requirements
* Python 3

## Usage of examples
```
python3 conlang.py 100
python3 conlang.py 100 raw

python3 japanese.py 100 hiragana
python3 japanese.py 100 hepburn
python3 japanese.py 100 strict
python3 japanese.py 100 raw
```
