# Baseline model

Need:
-  
```
./mosesdecoder/scripts/Transliteration/train-transliteration-module.pl \
--corpus-f ~/sorbian-transliteration/data/corpus/tokenized/lowercase/train.hsb --corpus-e ~/sorbian-transliteration/data/corpus/tokenized/lowercase/train.dsb \
--alignment ~/sorbian-transliteration/data/alignment/train.hsb-dsb \
--moses-src-dir /mosesdecoder --external-bin-dir /moses-transliteration-pair-mining/external_bin \
--input-extension hsb --output-extension dsb \
--srilm-dir /usr/share/srilm --out-dir ~/sorbian-transliteration/baseline
```

## Installation

1. Get srilm [from](https://hovinh.github.io/blog/2016-04-22-install-srilm-ubuntu/)
- issue ```gcc unrecognized command line option -m64 "srilm"```