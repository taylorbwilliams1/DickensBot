"""

DickensBot.py

Authors: Taylor Williams and Bryn Peters

CSCI 404 Final Project
Western Washington University
Winter 2017

"""

import nltk
import random
import tweepy
from time import sleep
from credentials import *

biModel = {} 
        
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
    
#Using URL downloading in nltk
"""
url = "https://www.gutenberg.org/files/1400/1400.txt"
response = request.urlopen(url)
print(type(response.read()))
raw = response.read().decode('utf8')
tokens = nltk.word_tokenize(raw)
print(tokens[:11])


#from downloaded txt files
tester = open("expect.txt").read()
tokens = nltk.sent_tokenize(tester)
print(tokens[1])

"""
def senBuilder(word):
    #word = random.choice(list(biModel.keys()))
    if word in biModel:
        sentence = word.capitalize()
        prevWord = word
        i = 0
        while i < 20:
            #weighted choice for possible values
            b = [[k,v] for k,v in biModel[word].items()]
            word = weighted_choice(b)
            #accounting for special punctuation cases
            if word == ".":
                i = 20
            elif word in [",", ";", "!", ":"] or "'" in list(word):
                sentence += word
            else:
                sentence += " " + word
            i += 1
        sentence += "."
    else:
        sentence = "Keyword: " + word + " is not contained within Dickens Corpus."
    return(sentence)
    
def mBuilder(wordList):
    word1 = wordList[0]
    word2 = wordList[1]
    if word1 not in biModel:
        #new bigram
        biModel.update({word1: {word2: 1}})
    else:
        if word2 not in biModel[word1]:
            #new 2nd word for existing 1st word
            biModel[word1].update({word2: 1})
        else:
            #existing bigram, increment count
            biModel[word1][word2] += 1

def training(file):
    biWords = []
    raw = open(file).read()
    tokens = nltk.word_tokenize(raw)
    for word in tokens:
        if len(biWords) == 2:
            mBuilder(biWords)
            biWords.pop(0)
            biWords.append(word)
        else:
            biWords.append(word)

def tweet():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    #retweet and reply to latest mention
    mentions = api.mentions_timeline(count=1)
    for tweet in mentions:
        try:
            keyword = tweet.text.split(' ', 1)[1]
            if '#' in keyword:
                keyword = keyword.replace('#', "")
            #print("'" + tweet.text + "' by: @" + tweet.user.screen_name)
            sentence = senBuilder(keyword)
            api.update_status('@' + tweet.user.screen_name + ' #' + keyword + ': ' + sentence)    
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def main():
    for file in ["expectations.txt", "oliver.txt", "copperfield.txt"]:
        training(file)
    tweet()
    

if __name__ == "__main__":
    main()
