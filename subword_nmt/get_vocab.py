#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import inspect
import warnings
import argparse
import codecs
import configparser

from collections import Counter

# hack for python2/3 compatibility
from io import open
argparse.open = open

class filterwarnings(object):
    def __init__(self, stat, cat):
        super(filterwarnings, self).__init__()
        self.ignore = warnings.filterwarnings
        self.stat = stat
        self.cat = cat

    def __enter__(self):
        self.ignore('ignore' if self.stat else 'default', category=self.cat)
    def __exit__(self, a,b,c):
        pass



def save_configFromArgs(args):

    absfile = (os.path.abspath(__file__))

    
    config = configparser.ConfigParser()
   
    path  = os.path.join('/'.join(absfile.split('/')[:-1]), 'config.ini')
    
    with open(path, 'w') as w:
        config['test'] = {}
        cfg = dict()
        for var in vars(args):
            cfg[var] = getattr(create_parser(), var)
            
            config['test'][var]  = str(cfg[var])


        config.write(w)
        print('saved to %s' % path)

def create_parser(subparsers=None):

    if subparsers:
        parser = subparsers.add_parser('get-vocab',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Generates vocabulary")
    else:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Generates vocabulary")

    parser.add_argument(
        '--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
        metavar='PATH',
        help="Input file (default: standard input).")

    parser.add_argument(
        '--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
        metavar='PATH',
        help="Output file (default: standard output)")

    return parser

def get_vocab(train_file, vocab_file):

    c = Counter()

    for line in train_file:
        for word in line.strip('\r\n ').split(' '):
            if word:
                c[word] += 1

    for key,f in sorted(c.items(), key=lambda x: x[1], reverse=True):
        vocab_file.write(key+" "+ str(f) + "\n")

if __name__ == "__main__":
    save_configFromArgs(create_parser())


