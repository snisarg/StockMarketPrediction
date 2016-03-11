import pandas
from nltk.corpus import verbnet
from textblob import TextBlob
import nltk
import sys
from nltk.stem.lancaster import LancasterStemmer
import os
from itertools import dropwhile
import posttagger

punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
headlines = pandas.read_csv('data/headlines.txt', parse_dates=[0])
headlines = headlines[headlines['message'].notnull()]


def get_prices(stock_name):
    stock = pandas.read_csv('data/'+stock_name+'.csv', parse_dates=[0])
    stock = stock[['Date', 'Close', 'Volume', 'Threshold Change', 'Next day', 'Price change']]
    # Columns we are extracting. Add more here.
    return stock


def get_prices_threshold(dataframe):
    return dataframe[dataframe['Threshold Change'] == '1']


def headlines_for(topic):
    return headlines[headlines['message'].str.contains(topic, case=False)]

def passivep(tags):
    """Takes a list of tags, returns true if we think this is a passive
    sentence."""
    # Particularly, if we see a "BE" verb followed by some other, non-BE
    # verb, except for a gerund, we deem the sentence to be passive.

    postToBe = list(dropwhile(lambda(tag): not tag.startswith("BE"), tags))
    nongerund = lambda(tag): tag.startswith("V") and not tag.startswith("VBG")

    filtered = filter(nongerund, postToBe)
    out = any(filtered)

    return out

TAGGER = None
def get_feature_vector(sent):
    global TAGGER
    TAGGER = posttagger.get_tagger()
    findpassives(sent)


def repl():
    """Read eval (for passivity) print loop."""
    try:
        while True:
            line = raw_input()
            findpassives(line)
    except EOFError,e:
        pass

def tag_sentence(sent):
    """Take a sentence as a string and return a list of (word, tag) tuples."""
    assert isinstance(sent, basestring)

    tokens = nltk.word_tokenize(sent)
    return TAGGER.tag(tokens)

def oneline(sent):
    """Replace CRs and LFs with spaces."""
    return sent.replace("\n", " ").replace("\r", " ")

def findpassives(sent):
    # Feature extraction code here.
    """Given a sentence, tag it and print if we think it's a passive-voice
    formation."""
    lancaster_stemmer = LancasterStemmer()
    tagged = tag_sentence(sent)
    tags = map( lambda(tup): tup[1], tagged)
    print sent
    if passivep(tags):
        #file.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag =True
        prevnoun=""
        verb=""
        nextnoun=""
        for word, pos in blob.tags:
            #print word,pos
            if (pos=='NN' or pos =='NNP') and flag== True:
                prevnoun= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN'or pos=='VB') and flag==True:
                verb=word
                flag= False
            if (pos=='NN' or pos=='NNP') and flag== False:
                nextnoun=word
                break
        lancaster_stemmer.stem(verb)
        #print verb
        if len(verbnet.classids(verb))==0:
            ans= prevnoun+" "+verb+" "+nextnoun+" "
        else:
            ans1=verbnet.classids(verb)
            ansstring=''.join(ans1)
            ans= prevnoun+" "+ansstring+" "+nextnoun+" "
        #fileans.write(ans+'\n')

        #print verbnet.classids('acclaim')
        #print "passive:", oneline(sent)
    else:
        #file1.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag1 =True
        prevnoun1=""
        verb1=""
        nextnoun1=""
        for word, pos in blob.tags:
            #print word,pos
            if (pos=='NN' or pos =='NNP') and flag1== True:
                prevnoun1= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN'or pos=='VB') and flag1==True:
                verb1=word
                flag1= False
            if (pos=='NN' or pos=='NNP') and flag1== False:
                nextnoun1=word
                break
        lancaster_stemmer.stem(verb1)
        #print verb1
        if len(verbnet.classids(verb1))==0:
            ans= prevnoun1+" "+verb1+" "+nextnoun1+" "
        else:
            ans1=verbnet.classids(verb1)
            ansstring=''.join(ans1)
            ans= prevnoun1+" "+ansstring+" "+nextnoun1+" "
        #fileans.write(ans+'\n')
        print ans
        return ans





