"""

DickensBot.py

Authors: Taylor Williams and Bryn Peters

CSCI 404, Final Project
WWU, Winter 2017

"""

import nltk
import random

#test list
listy = [['a',5],['b',10],['c',40]]
        
def weighted_choice(choices):
    totalSum = sum(weights for choice, weights in choices)
    r = random.uniform(0, totalSum)
    upto = 0
    for choice, weight in choices:
        if upto + weight >= r:
            return choice
        upto += weight
    #function can't get here
    assert False

#sentences = nltk.sentence_tokenizer(
