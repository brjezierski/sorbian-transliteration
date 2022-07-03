# Sorbian transliteration



## Steps for transliteration baseline model

Paper breaks it down into  
(1) pre-processing,   
(2) modification of the input sequences based on alignment representation   
(3) creation of an RNN-based machine transliteration

Initially, we extract a list of word pairs from a word-aligned parallel corpus using GIZA++, what word aligner to use?
Initially, the parallel corpus is word-aligned using GIZA++ (Och and Ney, 2003), and the alignments are refined using the grow-diag-final-and heuristic (Koehn et al., 2003)

We extracted the training data for the transliteration system using a preliminary transliteration mining
model, filtered the data using a preliminary transliteration model, and trained the final transliteration
model on the filtered data.

### Summary
- filter out non-transliterations iteratively
- Grapheme-to-phoneme model g2p - in test mode, we look for the best sequence of multigrams given a fixed source and target string and return the probability of this sequence
- SMT with Moses toolkit - optimizes accuracy rather than the likelihood of training data like g2p. We build the LM on the
target word types in the data to be filtered.
For training Moses as a transliteration system, we
treat each word pair as if it were a parallel sentence,
by putting spaces between the characters of each
word. (epsilon insertion) LM is built with SRILM
- **extraction of pairs** - run g2p on word-aligned data and everytime iteratively remove the bottom 5% with lowest likelihood of being a transliteration. Determine a stopping criterion. The stopping criterion uses unlabelled held-out data to predict the optimal stopping point (?)
- how to build a transliteration module on the extracted transliteration pairs and how to integrate it into MGIZA++
  - For every source word, we generate the list of 10-best transliterations nbestT I(e)


### Terms
- distortion limit - for reordering in Moses
- transliteration discovery - picking a plausible transliteratio from a given list

### Stack
- GIZA++ - to extract list of word-pairs
- g2p
- Moses
- SRILM-Toolkit - for 5-gram LM

### My steps
1. Align words using GIZA++
2. Get a joint unigram likelihood of the given pair with g2p?
3. Preprocess words with epsilon insertion
4. Apply the transliteration model (Moses) to optimize transliteration accuracy (?) (or neural transliteration (Design Challenges in Named Entity Transliteration))
5. Filter out non-transliteration pairs with low g2p score. Train a transliteration model (Moses?) on half the remaining data and test on the source side of the other half to determine the stopping criterion.
6. We would apply the transliteration model to OOV words?

## Papers

### Neural transliteration
- [Sequence-to-sequence neural network models for transliteration](https://arxiv.org/pdf/1610.09565.pdf)
  - CRF model - performs local string rewriting?
  - epsilon insertion - relevant
- [Aksharantar: Towards Building Open Transliteration Tools for
the Next Billion Users](https://arxiv.org/pdf/2205.03018.pdf)

### Transliteration mining
- [An Algorithm for Unsupervised Transliteration Mining with an Application
to Word Alignment](https://aclanthology.org/P11-1044.pdf)
- [Aksharantar: Towards Building Open Transliteration Tools for
the Next Billion Users](https://arxiv.org/pdf/2205.03018.pdf)
- [Integrating an Unsupervised Transliteration Model into
Statistical Machine Translation](https://aclanthology.org/E14-4029.pdf)
- [Manual for Moses implementation of the Durrani paper (p.178)](http://www2.statmt.org/moses/manual/manual.pdf)
## Sorbian
- [The LMU Munich System for
the WMT20 Very Low Resource Supervised MT Task](https://www.cis.lmu.de/~fraser/pubs/libovicky_wmt2020.pdf) - usage of transliteration mining

## g2p 
- [Sequitur](http://www.cs.columbia.edu/~ecooper/tts/g2p.html) - used for the paper, old (abandonware)
- [Pynini: A Python library for weighted finite-state grammar compilation](https://aclanthology.org/W16-2409.pdf) - the MFA g2p training model is based on panini
- [Stemmer and phonotactic rules to improve n-gram tagger-based indonesian phonemicization](https://www.sciencedirect.com/science/article/pii/S1319157821000069) - for low-resource languages
- [NEURAL GRAPHEME-TO-PHONEME CONVERSION WITH PRE-TRAINED GRAPHEME
MODELS](https://arxiv.org/pdf/2201.10716.pdf) - another good one for low-resource languages with [source code](https://github.com/ldong1111/GraphemeBERT)
- DeepPhonemizer - based on papers: [Transformer based Grapheme-to-Phoneme Conversion](https://arxiv.org/pdf/2004.06338.pdf) and [GRAPHEME-TO-PHONEME CONVERSION USING LONG SHORT-TERM MEMORY RECURRENT NEURAL NETWORKS](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43264.pdf)

## Questions
- What words exactly count as transliterations? We should expect a lot of cognates, are they transliterations?
- How about mining wikipedia for more data? (up to 3.3 k articles in dsb) - paper Mining Transliterations from Wikipedia using Pair HMMs
- Are GIZA++ and Moses right tools to use?

## Documenting instalation
1. Preprocessing the corpus - use [europarl tutorial](https://fabioticconi.wordpress.com/2011/01/17/how-to-do-a-word-alignment-with-giza-or-mgiza-from-parallel-corpus/)
  - tokenize with a list of German nonbreaking prefixes
  ```
  ./tokenizer.perl -l de < ../../sorbian-transliteration/hsb-dsb-mt-split/train_dsb_hsb.hsb > ../../sorbian-transliteration/hsb-dsb-mt-split/train_dsb_hsb.tok.hsb
```
- convert to lowercase
```
tr '[:upper:]' '[:lower:]' < train_dsb_hsb.tok.hsb > train_dsb_hsb.tok.low.hsb
```

2. [GIZA++ for python](https://github.com/sillsdev/giza-py)
```
git clone https://github.com/sillsdev/giza-py.git
cd giza-py
pip install -r requirements.txt
```
-  requires Python 3.7+ (3.9.10 installed)
-  requires [Boost (1.79.0)](https://www.boost.org/)  
```
cd boost_1_79_0
./bootstrap.sh --prefix=./build --with-libraries=thread,system
./b2 install
```
-  which requires [clang (13.0.0)](https://www.ics.uci.edu/~pattis/common/handouts/macclion/clang.html) 
```
command xcode-select --install
```
- requires CMake
- issues:
```
Undefined symbols for architecture x86_64:
  "boost::thread::hardware_concurrency()", referenced from:
      _main in main.cpp.o
ld: symbol(s) not found for architecture x86_64
```  
solution: replace it with ```std::thread::hardware_concurrency()``` in files *hardware_concurrency_pass.cpp, main.cpp, wait_fuzz.cpp, test_hardware_concurrency.cpp* and add ```#include \<thread\>``` in each file ([same functionality](https://stackoverflow.com/questions/8540387/why-is-there-a-difference-using-stdthreadhardware-concurrency-and-boostt))

issue 2:
```
Traceback (most recent call last):
  File "/Volumes/GoogleDrive-118172319871802801944/My Drive/Colab Notebooks/GR/giza-py/giza.py", line 5, in <module>
    from giza_aligner import HmmGizaAligner, Ibm1GizaAligner, Ibm2GizaAligner, Ibm3GizaAligner, Ibm4GizaAligner
  File "/Volumes/GoogleDrive-118172319871802801944/My Drive/Colab Notebooks/GR/giza-py/giza_aligner.py", line 9, in <module>
    from machine.translation import SymmetrizationHeuristic, WordAlignmentMatrix
ModuleNotFoundError: No module named 'machine'
```
run
```
pip3 install sil-machine
```

3. g2p, three candidates:  

    a) [montreal forced aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/g2p_train.html)
    - **issue**: looks like need to pre-process input  

    b) deep-phonemizer 
    - simple to use
    - **issues**: need to make a change in code to display scores not only for OOV words, possible issue with rating quality of generated transliteration and not the likelihood of a given pair being a transliteration

    ```
    pip3 install deep-phonemizer
    ```
    
    c) [sequitur g2p](https://github.com/sequitur-g2p/sequitur-g2p) 
    - originally used by the paper
    - **issue**: abandonware
    - **dependencies**: numpy, python, C++ compiler, swig (4.0.2)
    ```
    brew install swig
    ```

4. [Moses](http://www2.statmt.org/moses/?n=Development.GetStarted)

    ```
    brew install subversion
    brew install tcl-tk
    brew install zlib # already installed
    brew install bzip2
    brew install icu4c # already installed
    brew install libunistring # already installed

    cpan XML::Twig
    cpan Sort::Naturally

    brew install libcmph

    ```

    ```
    --with-cmph=/usr/local/Cellar/libcmph/2.0.2
    --with-xmlrpc-c=/usr/local/Cellar/xmlrpc-c/1.54.05
    --with-mm --with-probing-pt -j5 toolset=clang -q -d2
    ```
    - is libboost-dev boost on mac?

    The following dependencies will be installed: 
 boost171
 bzip2
 expat
 gettext-runtime
 icu
 libedit
 libffi
 libiconv
 lz4
 lzma
 ncurses
 openssl
 openssl3
 python310
 python3_select
 python_select
 sqlite3
 xz
 zlib
 zstd

    - [Alex tutorial](https://www.cis.uni-muenchen.de/~fraser/nepal/moses.html)
    ```
    brew install graphviz
    brew install imagemagick
    ```
