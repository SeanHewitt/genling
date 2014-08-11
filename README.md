#Generatrum Linguarum

This is a project to develop an application with which it is possible to generate a spoken contructed language, a conlang. In its current state, it is simply a word stem generator.

In the generating process, user input weights and probabilities affect the usage of individual phonemes, usage of syllable segments, usage of syllables in the same position, the amount of syllables within a stem and whether a stem caught by a filter is to be allowed. User input regex is used for deciding whether a generated word stem is allowed or not (e.g. combinations of phonemes that are not permitted) and in transliterating a generated word/stem from a raw form (e.g. "&lt;ge&gt;&lt;hYo&gt;&lt;uN&gt;&lt;e&gt;&lt;nu&gt;") into a final form (e.g. "gehyōn'enu", "げひょうんえぬ", "gexyoungënu" or "гэхёунъэну").

For a quicker development of the design, the application is written in Python. Any optimisation or porting to a faster language can be done later if at all necessary.

Requirements:
* Python3
* PyYAML - A language is defined with a YAML config file

##Current usage
````
python3 genling.py <language config> <writing system index> <word count>
````
The writing system index starts with 1 and is the definition order within the config file. 0 keeps the stem in its raw form.

###Example
````
python3 genling.py config/example2.yaml 1 100
```
