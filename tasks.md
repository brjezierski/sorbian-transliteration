# Tasks

1. Mine for transliterations between Upper and Lower Sorbian with the baseline model

2. Build an hsb-dsb MT model following [this paper](https://aclanthology.org/E14-4029.pdf). Three methods for incorporating transliteration into the MT pipeline, namely:  
    - replacing OOVs with the 1-best transliteration in a postdecoding step,  
    - selecting the best transliteration from the list of n-best transliterations using
transliteration and language model features in a
post-decoding step,  
    - providing a transliteration
phrase-table to the decoder on the fly where it
can consider all features to select the best transliteration of OOV words.

3. Evaluate the translations with and without substituting OOVs with mined transliterations