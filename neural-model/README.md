# Resources
- [This paper](https://aclanthology.org/L18-1150.pdf) describes a neural approach using a concatenated list of transliteration pairs for neural training. It uses a Bible names translation matrix dataset (Wu and Yarowsky, 2018). Each
training example was split into spaces, with a special source
language symbol prepended, as shown in Table 1.
Transfer learning. The single neural MT system trained
on the concatenation of the training data for all languages
performed much better than the other systems in our experiments, achieving a 69% one-best accuracy on the concatenation of the test sets. This massive gain stems from
the combination of the 1000x increase in training data and
the neural architecture’s ability to effectively leverage the
commonality between languages. This result indicates that
this transfer learning technique works well when combining low-resource languages, even when each individual language pair may only have a miniscule amount of data.

- [Kundu et al](https://aclanthology.org/W18-2411.pdf) - Segment the words into characters or byte-pairs. RNN-based and Conv seq2seq ensembles

- [Grundkiewicz et al](https://aclanthology.org/W18-2413.pdf) - BiDeep architecture, [training scripts](https://github.com/snukky/news-translit-nmt), validation sets consists of randomly selected 500 examples that are subtracted
from the training data

# Data
Mined transliteration pairs from the SMT model. It contains 32 995 pairs. 

# Steps

# Questions
- How does a machine translation model deal with OOVs?
- How about subword machine translation model (only for OOVs?)?
- Do we need dev/test sets? OOVs from the test/dev sets?


# Comments
[This reinforces results from previous studies that subword-level translation is better than the transliteration of untranslated words in the output of an SMT system.](https://arxiv.org/pdf/2003.08925.pdf)