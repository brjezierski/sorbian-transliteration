# Baseline model

## Setting up moses

1. Install moses

2. Comment out a line which removes English which removes words in the latin script in the clean script of transliteration module

3. install SLIRM 1.7.1


## Data pre-processing

1. ```cd``` into sorbian-transliteration/baseline

2. Tokenization (whitespace insertion and punctuation deletion)
    - * is train or test 
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
    We get 52744 sentences for train and 1453 for test set

## Alignments and ransliteration mining

1. ```cd``` into sorbian-transliteration/baseline

  ```
  mkdir external_bin
  cp ~/mgiza/mgizapp/bin/* external_bin/
  cp ~/mgiza/mgizapp/scripts/merge_alignment.py external_bin/
  ```

2. If model folder is not present, run the training script to build alignment

  ```
  ~/mosesdecoder/scripts/training/train-model.perl \
    -root-dir ~/sorbian-transliteration/baseline/ \
    --corpus ~/sorbian-transliteration/data/corpus/clean/train \
    --f hsb \
    --e dsb \
    -external-bin-dir ~/sorbian-transliteration/baseline/external_bin \
    -mgiza --last-step=3
  ```

3. Run the transliteration training script 

  ```
  ~/mosesdecoder/scripts/Transliteration/train-transliteration-module.pl \
    --corpus-f ~/sorbian-transliteration/data/corpus/clean/train.hsb \
    --corpus-e ~/sorbian-transliteration/data/corpus/clean/train.dsb \
    --alignment ~/sorbian-transliteration/baseline/model/aligned.grow-diag-final \
    --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/sorbian-transliteration/baseline/external_bin \
    --input-extension hsb \
    --output-extension dsb \
    --out-dir ~/sorbian-transliteration/baseline/transliteration-model \
    --srilm-dir ~/srilm/bin/aarch64
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

2. [IGNORE] Generate an interpolated Kneser-Ney smoothed 5-gram language model with KenLM for target language (dsb)
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
  nohup nice ~/mosesdecoder/scripts/training/train-model.perl \
    -root-dir ~/sorbian-transliteration/baseline \
    -corpus ~/sorbian-transliteration/data/corpus/clean/train \
    -f hsb -e dsb -alignment grow-diag-final-and \
    -reordering msd-bidirectional-fe -lm 0:3:$HOME/sorbian-transliteration/baseline/transliteration-model/lm/targetLM:8 \
    -external-bin-dir ~/sorbian-transliteration/baseline/external_bin \
    -post-decoding-translit yes \
    -transliteration-phrase-table ~/sorbian-transliteration/baseline/transliteration-model/model/phrase-table.gz >& training.out &
  ```

5. Generate a file with OOVs and translation output without transliteration

  ```
  nohup nice ~/mosesdecoder/bin/moses -f ~/sorbian-transliteration/baseline/model/moses.ini \
    -output-unknowns ~/sorbian-transliteration/baseline/oov.hsb \
    < ~/sorbian-transliteration/data/corpus/clean/test.hsb > ~/sorbian-transliteration/data/corpus/clean/test.dsb 2> ~/sorbian-transliteration/baseline/test.translated.dsb
  ```

6. Transliterate the output

  ```
  ~/mosesdecoder/scripts/Transliteration/post-decoding-transliteration.pl \
    --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/sorbian-transliteration/baseline/external_bin \
    --transliteration-model-dir ~/sorbian-transliteration/baseline/transliteration-model \
    --oov-file ~/sorbian-transliteration/baseline/oov.hsb \
    --input-file ~/sorbian-transliteration/baseline/results/test.translated.dsb \
    --output-file ~/sorbian-transliteration/baseline/results/test.translated.transliterated.dsb \
    --input-extension hsb --output-extension dsb \
    --language-model ~/sorbian-transliteration/baseline/transliteration-model/lm/targetLM \
    --decoder ~/mosesdecoder/bin/moses
  ```

## Evaluation

1. Score with BLEU

  ```
  ~/mosesdecoder/scripts/generic/multi-bleu.perl \
    -lc ~/sorbian-transliteration/data/corpus/clean/test.dsb \
    < ~/sorbian-transliteration/baseline/results/test.translated.dsb
  ~/mosesdecoder/scripts/generic/multi-bleu.perl \
    -lc ~/sorbian-transliteration/data/corpus/clean/test.dsb \
    < ~/sorbian-transliteration/baseline/results/test.translated.transliterated.dsb
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

