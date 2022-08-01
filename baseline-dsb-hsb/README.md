# Baseline model for dsb-hsb

## Alignments and transliteration mining

1. If model folder is not present, run the training script to build alignment

  ```
  ~/mosesdecoder/scripts/training/train-model.perl \
    -root-dir ~/sorbian-transliteration/baseline-dsb-hsb/ \
    --corpus ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/train \
    --f dsb \
    --e hsb \
    -external-bin-dir ~/sorbian-transliteration/external_bin \
    -mgiza --last-step=3
  ```

2. Run the transliteration training script 

  ```
  ~/mosesdecoder/scripts/Transliteration/train-transliteration-module.pl \
    --corpus-f ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/train.dsb \
    --corpus-e ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/train.hsb \
    --alignment ~/sorbian-transliteration/baseline-dsb-hsb/model/aligned.grow-diag-final \
    --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/sorbian-transliteration/external_bin \
    --input-extension dsb \
    --output-extension hsb \
    --out-dir ~/sorbian-transliteration/baseline-dsb-hsb/transliteration-model \
    --srilm-dir ~/srilm/bin/aarch64
  ```

3. Train moses with transliteration option on, GDFA symmetrization of GIZA++ alignments
    - a 5-gram OSM missing
  ```
  nohup nice ~/mosesdecoder/scripts/training/train-model.perl \
    -root-dir ~/sorbian-transliteration/baseline-dsb-hsb \
    -corpus ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/train \
    -f dsb -e hsb -alignment grow-diag-final-and \
    -reordering msd-bidirectional-fe -lm 0:3:$HOME/sorbian-transliteration/baseline-dsb-hsb/transliteration-model/lm/targetLM:8 \
    -external-bin-dir ~/sorbian-transliteration/external_bin \
    -post-decoding-translit yes \
    -transliteration-phrase-table ~/sorbian-transliteration/baseline-dsb-hsb/transliteration-model/model/phrase-table.gz >& training.out &
  ```

4. Generate a file with OOVs and translation output without transliteration

  ```
  nohup nice ~/mosesdecoder/bin/moses -f ~/sorbian-transliteration/baseline-dsb-hsb/model/moses.ini \
    -output-unknowns ~/sorbian-transliteration/baseline-dsb-hsb/oov.dsb \
    < ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.dsb > ~/sorbian-transliteration/baseline-dsb-hsb/results/test.translated.hsb 2> trace.out
  ```

5. Transliterate the output

  ```
  ~/mosesdecoder/scripts/Transliteration/post-decoding-transliteration.pl \
    --moses-src-dir ~/mosesdecoder \
    --external-bin-dir ~/sorbian-transliteration/external_bin \
    --transliteration-model-dir ~/sorbian-transliteration/baseline-dsb-hsb/transliteration-model \
    --oov-file ~/sorbian-transliteration/baseline-dsb-hsb/oov.dsb \
    --input-file ~/sorbian-transliteration/baseline-dsb-hsb/results/test.translated.hsb \
    --output-file ~/sorbian-transliteration/baseline-dsb-hsb/results/test.translated.transliterated.hsb \
    --input-extension dsb --output-extension hsb \
    --language-model ~/sorbian-transliteration/baseline-dsb-hsb/transliteration-model/lm/targetLM \
    --decoder ~/mosesdecoder/bin/moses
  ```

6. Score with BLEU

  ```
  ~/mosesdecoder/scripts/generic/multi-bleu-detok.perl \
    -lc ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.hsb \
    < ~/sorbian-transliteration/baseline-dsb-hsb/results/test.translated.hsb;
  ~/mosesdecoder/scripts/generic/multi-bleu-detok.perl \
    -lc ~/sorbian-transliteration/data/hsb-dsb/corpus/clean/test.hsb \
    < ~/sorbian-transliteration/baseline-dsb-hsb/results/test.translated.transliterated.hsb
  ```
