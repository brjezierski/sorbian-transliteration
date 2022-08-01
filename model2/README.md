# dsb-hsb model with a retrained LM

## Train LM on monolingual hsb data and retrain transliteration and tranlation models

1. Get data

  ```
  cp ~/sorbian-transliteration/data/hsb/lexicon.hsb ~/sorbian-transliteration/model2/transliteration-model/lm/target
  ```

2. Build the language model

  ```
  ~/srilm/bin/aarch64/ngram-count \
    -order 5 -interpolate -kndiscount -addsmooth1 0.0 -unk \
    -text ~/sorbian-transliteration/model2/transliteration-model/lm/target \
    -lm ~/sorbian-transliteration/model2/transliteration-model/lm/targetLM
  ~/mosesdecoder/bin/build_binary \
    ~/sorbian-transliteration/model2/transliteration-model/lm/targetLM \
    ~/sorbian-transliteration/model2/transliteration-model/lm/targetLM.bin
  ```

3. Create new config file

  ```
  ~/mosesdecoder/scripts/training/train-model.perl \
    -mgiza -mgiza-cpus 10 -dont-zip -first-step 9 \
    -external-bin-dir ~/sorbian-transliteration/external_bin \
    -f dsb \
    -e hsb \
    -alignment grow-diag-final-and -parts 5 \
    -score-options '--KneserNey' \
    -phrase-translation-table ~/sorbian-transliteration/model2/transliteration-model/model/phrase-table \
    -config ~/sorbian-transliteration/model2/transliteration-model/model/moses.ini \
    -lm 0:5:$HOME/sorbian-transliteration/model2/transliteration-model/lm/targetLM.bin:8
  ```


4. Train moses with transliteration option on, GDFA symmetrization of GIZA++ alignments
    - a 5-gram OSM missing
  ```
  nohup nice ~/mosesdecoder/scripts/training/train-model.perl \
    -root-dir ~/sorbian-transliteration/model2 \
    -corpus ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/train \
    -f dsb -e hsb -alignment grow-diag-final-and \
    -reordering msd-bidirectional-fe -lm 0:3:$HOME/sorbian-transliteration/model2/transliteration-model/lm/targetLM:8 \
    -external-bin-dir ~/sorbian-transliteration/external_bin \
    -post-decoding-translit yes \
    -transliteration-phrase-table ~/sorbian-transliteration/model2/transliteration-model/model/phrase-table.gz >& training.out &
  ```

5. Generate a file with OOVs and translation output without transliteration

  ```
  nohup nice ~/mosesdecoder/bin/moses -f ~/sorbian-transliteration/model2/model/moses.ini \
    -output-unknowns ~/sorbian-transliteration/model2/oov.dsb \
    < ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.dsb > ~/sorbian-transliteration/model2/results/test.translated.hsb 2> trace.out
  ```

6. Transliterate the output

  ```
  ~/mosesdecoder/scripts/Transliteration/post-decoding-transliteration.pl \
    --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/sorbian-transliteration/external_bin \
    --transliteration-model-dir ~/sorbian-transliteration/model2/transliteration-model \
    --oov-file ~/sorbian-transliteration/model2/oov.dsb \
    --input-file ~/sorbian-transliteration/model2/results/test.translated.hsb \
    --output-file ~/sorbian-transliteration/model2/results/test.translated.transliterated.hsb \
    --input-extension dsb --output-extension hsb \
    --language-model ~/sorbian-transliteration/model2/transliteration-model/lm/targetLM \
    --decoder ~/mosesdecoder/bin/moses
  ```

## Evaluation

1. Score with BLEU

  ```
  ~/mosesdecoder/scripts/generic/multi-bleu-detok.perl \
    -lc ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.hsb \
    < ~/sorbian-transliteration/model2/results/test.translated.hsb;
  ~/mosesdecoder/scripts/generic/multi-bleu-detok.perl \
    -lc ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.hsb \
    < ~/sorbian-transliteration/model2/results/test.translated.transliterated.hsb;
  ~/mosesdecoder/scripts/generic/multi-bleu-detok.perl \
    -lc ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.hsb \
    < ~/sorbian-transliteration/model2/results2/test.translated.transliterated.hsb
  ```
  
## Results

- results dir contains transliteration done using a LM2 and translation with LM1
- results2 dir contains transliteration done using a LM2 and translation with LM2 as well

