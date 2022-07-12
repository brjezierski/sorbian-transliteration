# Baseline model

## Transliteration mining

1. ```cd``` into sorbian-transliteration/baseline

2. If model folder is not present, run the training script to build alignment

```
~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/sorbian-transliteration/baseline/ --corpus corpus/clean --f hsb --e dsb -external-bin-dir external_bin/ -mgiza --last-step=3
```

3. Run the transliteration training script 
```
~/mosesdecoder/scripts/Transliteration/train-transliteration-module.pl --corpus-f ~/sorbian-transliteration/baseline/corpus/clean.hsb --corpus-e ~/sorbian-transliteration/baseline/corpus/clean.dsb --alignment ~/sorbian-transliteration/baseline/model/aligned.grow-diag-final --moses-src-dir ~/mosesdecoder --external-bin-dir ~/sorbian-transliteration/baseline/external_bin --input-extension hsb --output-extension dsb --srilm-dir /usr/share/srilm --out-dir ~/sorbian-transliteration/baseline/transliteration-model
```


## Integration of transliteration in translation for evaluation

1. Choose a transliteration integration method
    - method 2 - obtains the list of OOV words automatically by running the decoder
    ```post-decoding-transliteration = "yes"```
    - method 3 - requires user to provide the list of words to be transliterated
    ```post-decoding-transliteration = "yes"```

2. Preprocess to a maximum sentence length of 80

3. Generate an interpolated Kneser-Ney smoothed 5-gram language model with KenLM for target language (dsb)
  ```
  mkdir ~/lm
  cd ~/lm
  ~/mosesdecoder/bin/lmplz -o 5 <corpus/clean.dsb > arpa.dsb
  ```
    - Binarize for faster loading
  ```
  ~/mosesdecoder/bin/build_binary clean.dsb blm.dsb
  ```

4. Train moses with transliteration option on, GDFA symmetrization of GIZA++ alignments
    - a 5-gram OSM missing
  ```
  nohup nice ~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/sorbian-transliteration/ -corpus corpus/clean \
    -f hsb -e dsb -alignment grow-diag-final-and \
    -reordering msd-bidirectional-fe -lm 0:3:$HOME/sorbian-transliteration/baseline/lm/blm.dsb:8 \
    -external-bin-dir ~/sorbian-transliteration/baseline/external_bin -post-decoding-translit yes \
    -transliteration-phrase-table ~/sorbian-transliteration/baseline/transliteration-model/model/phrase-table.gz >& training.out &
  ```

## Questions
We use 4 basic phrase-translation features (direct, inverse phrasetranslation, and lexical weighting features), language model feature (built from the target-side of mined transliteration corpus), and word and phrase penalties. The feature weights are tuned on a devset of 1000 transliteration pairs

# Papers
[Belarusian transliteration and NMT integration paper](https://link.springer.com/article/10.1007/s10590-017-9203-5)

## Issue documentation

1. Getting srilm [from](https://hovinh.github.io/blog/2016-04-22-install-srilm-ubuntu/)
- didn't work because of the issue ```gcc unrecognized command line option -m64 "srilm"``` (probably an M1 chip problem)

2. Running the transliteration training script gives the following error

```
Error: 'sVok[z]<sVok[z+1]' ::: in Source /home/bartek/mgiza/mgizapp/src/mkcls/KategProblemTest.cpp:159
ERROR: Execution of: /home/bartek/sorbian-transliteration/baseline/external_bin/mkcls -c50 -n2 -p/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/corpus.hsb -V/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/prepared/hsb.vcb.classes opt
  died with signal 11, with coredump
```

