#Generatrum Linguarum

This is a personal project of mine to develop an application with which it is possible to generate a spoken contructed language, a conlang. So far I have made plenty of attempts at it using the different programming languages and programming methods I've learned over time.

In this attempt I'm using Python due to the ease at which code can be restructured and rewritten. The generator makes use of user input regex for deciding whether a generated word stem is allowed or not (e.g. combinations of phonemes that are not permitted) and in transliterating a generated word/stem from a raw form (e.g. "&lt;ge&gt;&lt;hYo&gt;&lt;uN&gt;&lt;e&gt;&lt;nu&gt;") into a final form (e.g. "gehyōn'enu", "げひょうんえぬ", "gexyoungënu" or "гэхёунъэну"). In the generating process, user input weights and probabilities affect the usage of individual phonemes, usage of syllable segments, the amount of syllables within a stem and whether a stem caught by a filter is to be allowed.

To further develop this design, I ported it from Java into Python 3. The reason for this being that I realised that its not so easy to write in Java if you don't know the final structure of the application. Any optimisation or porting to a faster language can be done later if necessary. It may actually already be fast enough as it is now. With my test config I have achieved 10,000 generated raw word stems per second (Around 0.2 seconds in Java).

A language is defined with a YAML config file and therefore PyYAML is required.

##Current usage
````
genling.py <language config> <writing system index> <word count>
````
The writing system index starts with 1 and is the definition order within the config file. 0 keeps the stem in its raw form.

###Example
````
genling.py config/test.yaml 2 100
```