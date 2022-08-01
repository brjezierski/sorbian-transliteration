#!/usr/bin/env bash
cd /home/bartek/sorbian-transliteration/baseline-dsb-hsb/transliteration-model/tuning/tmp
/home/bartek/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run7.scores.dat --ffile run7.features.dat -r /home/bartek/sorbian-transliteration/baseline-dsb-hsb/transliteration-model/tuning/reference -n run7.best100.out.gz
