#!/usr/bin/env bash
cd /home/bartek/sorbian-transliteration/baseline/transliteration-model/tuning/tmp
/home/bartek/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run5.scores.dat --ffile run5.features.dat -r /home/bartek/sorbian-transliteration/baseline/transliteration-model/tuning/reference -n run5.best100.out.gz
