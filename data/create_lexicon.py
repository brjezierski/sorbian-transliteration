#!/usr/bin/python

import sys, getopt
import re
import string
alphabet ='ížúctdpéxhwazřqfvńňęäimsßjŕgćyár­łźśšukoóàýbżněölüeč' # [consonants with an accent are dsb only]

def special_match(strg, search=re.compile(r'[^{}]'.format(alphabet)).search):
    return not bool(search(strg))

def create_lexicon(inputfile, outputfile):
    lexicon = set()
    print("Loading corpus from", inputfile)
    with open(inputfile, 'r') as f:
        for line in f:
            for word in line.split():
                if special_match(word):
                    lexicon.add(word)
    sorted_lexicon = sorted(lexicon)
    with open('corpus.hsb', 'w+') as f:
        for word in sorted_lexicon:
            if (special_match(word)):
                f.write("%s\n" % " ".join(word))
    print("Lexicon created in", outputfile)
            
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("create_lexicon.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("create_lexicon.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    create_lexicon(inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])