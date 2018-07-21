#!/usr/bin/env python

import string
from random import choice
import hashlib

def wrap(h):
    """Wrap a hashlib hash function to be one that outputs integers."""
    def wrapped(s):
        m = h()
        m.update(s)
        return hash(m.digest())
    return wrapped

HASH_FUNCS = [hash] + [wrap(h) for h in [hashlib.md5,
                                         hashlib.sha1,
                                         hashlib.sha224,
                                         hashlib.sha256,
                                         hashlib.sha384,
                                         hashlib.sha512]]


class BloomFilter:
    def __init__(self, size, hash_funcs):
        self.array = [0] * size
        self.hash_funcs = hash_funcs

    def add(self, x):
        for h in self.hash_funcs:
            self.array[h(x) % len(self.array)] = 1

    def __contains__(self, x):
        return all(self.array[h(x) % len(self.array)] for h in self.hash_funcs)

    def load(self):
        return sum(self.array)


def random_word(size):
    return ''.join(choice(string.ascii_lowercase) for _ in range(size))


WORDS = set(line.strip() for line in open('wordlist.txt').readlines())


for size in [100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000]:
    print
    for n_hash in range(1, 8):
        b = BloomFilter(size, HASH_FUNCS[:n_hash])
        for word in WORDS:
            b.add(word)

        false_positives = 0
        for _ in range(10000):
            w = random_word(5)
            if w in b and not w in WORDS:
                false_positives += 1

        print 'size: {:>8}     hash func: {:>1}     load: {:>8}      false positive (out of 10000): {:>5}'.format(
                size, n_hash, b.load(), false_positives)
