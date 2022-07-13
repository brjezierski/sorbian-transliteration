# Baseline model

## Data pre-processing

1. ```cd``` into sorbian-transliteration/baseline

2. Tokenization (whitespace insertion and punctuation deletion)
    - * is train, val or test 
  ```
  ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l hsb < ~/sorbian-transliteration/data/corpus/*.hsb > ~/sorbian-transliteration/data/corpus/tokenized/*.hsb
  ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l dsb < ~/sorbian-transliteration/data/corpus/*.dsb > ~/sorbian-transliteration/data/corpus/tokenized/*.dsb
  ```

3. Lowercase conversion

  ```
  ~/mosesdecoder/scripts/tokenizer/lowercase.perl < ~/sorbian-transliteration/data/corpus/tokenized/*.hsb > ~/sorbian-transliteration/data/corpus/tokenized/lowercase/*.hsb
  ~/mosesdecoder/scripts/tokenizer/lowercase.perl < ~/sorbian-transliteration/data/corpus/tokenized/*.dsb > ~/sorbian-transliteration/data/corpus/tokenized/lowercase/*.dsb
  ```

4. Cleaning lines longer than 80 characters (check how many percentage wise are longer)

  ```
  ~/mosesdecoder/scripts/training/clean-corpus-n.perl ~/sorbian-transliteration/data/corpus/tokenized/lowercase/* hsb dsb ~/sorbian-transliteration/data/corpus/clean/* 1 80
  ```


## Transliteration mining

1. ```cd``` into sorbian-transliteration/baseline

2. If model folder is not present, run the training script to build alignment

  ```
  ~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/sorbian-transliteration/baseline/ --corpus ~/sorbian-transliteration/data/corpus/clean/train --f hsb --e dsb -external-bin-dir ~/mosesdecoder/tools -mgiza --last-step=3
  ```

3. Run the transliteration training script 

  ```
  ~/mosesdecoder/scripts/Transliteration/train-transliteration-module.pl --corpus-f ~/sorbian-transliteration/data/corpus/clean/train.hsb --corpus-e ~/sorbian-transliteration/data/corpus/clean/train.dsb --alignment ~/sorbian-transliteration/baseline/model/aligned.grow-diag-final --moses-src-dir ~/mosesdecoder --external-bin-dir ~/mosesdecoder/tools --input-extension hsb --output-extension dsb --srilm-dir /usr/share/srilm --out-dir ~/sorbian-transliteration/baseline/transliteration-model
  ```


## Integration of transliteration in translation for evaluation

1. Choose a transliteration integration method. Here we will follow method 2
    - method 2 - obtains the list of OOV words automatically by running the decoder
    ```
    post-decoding-transliteration = "yes"
    ```
    - method 3 - requires user to provide the list of words to be transliterated
    ```
    in-decoding-transliteration = "yes"
    transliteration-file = /file containing list of words to be transliterated/
    ```

2. Generate an interpolated Kneser-Ney smoothed 5-gram language model with KenLM for target language (dsb)
  ```
  mkdir ~/lm
  cd ~/lm
  ~/mosesdecoder/bin/lmplz -o 5 <~/sorbian-transliteration/data/corpus/clean/train.dsb > ~/sorbian-transliteration/baseline/lm/arpa.dsb
  ```
    - Binarize for faster loading
  ```
  ~/mosesdecoder/bin/build_binary ~/sorbian-transliteration/baseline/lm/arpa.dsb ~/sorbian-transliteration/baseline/lm/blm.dsb
  ```

4. Train moses with transliteration option on, GDFA symmetrization of GIZA++ alignments
    - a 5-gram OSM missing
  ```
  nohup nice ~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/sorbian-transliteration/baseline -corpus ~/sorbian-transliteration/data/corpus/clean/train \
    -f hsb -e dsb -alignment grow-diag-final-and \
    -reordering msd-bidirectional-fe -lm 0:3:$HOME/sorbian-transliteration/baseline/lm/blm.dsb:8 \
    -external-bin-dir ~/mosesdecoder/tools -post-decoding-translit yes \
    -transliteration-phrase-table ~/sorbian-transliteration/baseline/transliteration-model/model/phrase-table.gz >& training.out &
  ```

5. Generate a file with OOVs and translation output without transliteration

  ```
  nohup nice ~/mosesdecoder/bin/moses -f  ~/mosesdecoder/sample-models/phrase-model/moses.ini \
    -output-unknowns ~/sorbian-transliteration/baseline/oov.hsb \
    < ~/sorbian-transliteration/data/corpus/clean/val.hsb > ~/sorbian-transliteration/data/corpus/clean/val.dsb 2> ~/sorbian-transliteration/baseline/val.translation.dsb
  ```

6. Transliterate the output

  ```
  ./post-decoding-transliteration.pl --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/mosesdecoder/tools --transliteration-model-dir <transliteration model> \
    --oov-file ~/sorbian-transliteration/baseline/oov.hsb \
    --input-file ~/sorbian-transliteration/baseline/val.translation.dsb \
    --output-file ~/sorbian-transliteration/baseline/val.translation-transliteration.dsb \
    --input-extension hsb --output-extension dsb \
    --language-model $HOME/sorbian-transliteration/baseline/lm/blm.dsb \
    --decoder ~/mosesdecoder/bin/moses
  ```


## Questions
We use 4 basic phrase-translation features (direct, inverse phrasetranslation, and lexical weighting features), language model feature (built from the target-side of mined transliteration corpus), and word and phrase penalties. The feature weights are tuned on a devset of 1000 transliteration pairs

# References
- [Moses instruction for transliteration module](http://www2.statmt.org/moses/manual/manual.pdf)
- [Belarusian transliteration and NMT integration paper](https://link.springer.com/article/10.1007/s10590-017-9203-5)
- [Integrating an Unsupervised Transliteration Model into Statistical Machine Translation](https://aclanthology.org/E14-4029.pdf)

## Issue documentation

1. Getting srilm [from](https://hovinh.github.io/blog/2016-04-22-install-srilm-ubuntu/)
- didn't work because of the issue ```gcc unrecognized command line option -m64 "srilm"``` (probably an M1 chip problem)

2. Running the transliteration training script gives the following error

```
Error: 'sVok[z]<sVok[z+1]' ::: in Source /home/bartek/mgiza/mgizapp/src/mkcls/KategProblemTest.cpp:159
ERROR: Execution of: /home/bartek/sorbian-transliteration/baseline/external_bin/mkcls -c50 -n2 -p/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/corpus.hsb -V/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/prepared/hsb.vcb.classes opt
  died with signal 11, with coredump
```

