# Baseline model

## Steps

1. ```cd``` into sorbian-transliteration/baseline

2. If model folder is not present, run the training script to build alignment

```
~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/sorbian-transliteration/baseline/ --corpus corpus/test_clean --f hsb --e dsb -external-bin-dir external_bin/ -mgiza --last-step=3
```

3. Run the transliteration training script 
```
~/mosesdecoder/scripts/Transliteration/train-transliteration-module.pl --corpus-f ~/sorbian-transliteration/baseline/sample/corpus/clean.hsb --corpus-e ~/sorbian-transliteration/baseline/sample/corpus/clean.dsb --alignment ~/sorbian-transliteration/baseline/sample/model/aligned.grow-diag-final --moses-src-dir ~/mosesdecoder --external-bin-dir ~/sorbian-transliteration/baseline/external_bin --input-extension hsb --output-extension dsb --srilm-dir /usr/share/srilm --out-dir ~/sorbian-transliteration/baseline/sample/transliteration-model
```

## Issues

1. Getting srilm [from](https://hovinh.github.io/blog/2016-04-22-install-srilm-ubuntu/)
- didn't work because of the issue ```gcc unrecognized command line option -m64 "srilm"``` (probably an M1 chip problem)

2. Running the transliteration training script gives the following error

```
Error: 'sVok[z]<sVok[z+1]' ::: in Source /home/bartek/mgiza/mgizapp/src/mkcls/KategProblemTest.cpp:159
ERROR: Execution of: /home/bartek/sorbian-transliteration/baseline/external_bin/mkcls -c50 -n2 -p/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/corpus.hsb -V/home/bartek/sorbian-transliteration/baseline/sample/transliteration-model/training/prepared/hsb.vcb.classes opt
  died with signal 11, with coredump
```

