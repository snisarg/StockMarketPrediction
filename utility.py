import pandas
from nltk.corpus import verbnet
from textblob import TextBlob
import nltk
import sys
from nltk.stem.lancaster import LancasterStemmer
import os
from itertools import dropwhile
import posttagger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
import re
from sklearn import feature_extraction
import string
import numpy
import os.path

punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
__stemmer = nltk.stem.LancasterStemmer()
__words_only = re.compile("^[A-Za-z]*$")


def get_headlines():
    headlines = pandas.read_csv('data/headlines.txt', parse_dates=[0], encoding='latin_1')
    headlines = headlines[headlines['message'].notnull()]
    headlines['Date'] = headlines.msg_dt.map(pandas.datetools.normalize_date)
    return headlines


def get_prices(stock_name):
    stock = pandas.read_csv('data/'+stock_name+'.csv', parse_dates=[0])
    stock['Threshold Change'] = stock['Threshold Change'].fillna(0.0).astype(float)
    stock = stock[['Date', 'Close', 'Volume', 'Threshold Change', 'Next day', 'Price change', 'Direction']]
    # Columns we are extracting. Add more here.
    return stock


def get_prices_threshold(dataframe):
    return dataframe[dataframe['Threshold Change'] == '1']


def headlines_for(topic):
    headlines = get_headlines()
    return headlines[headlines['message'].str.contains(topic, case=False)]


def get_news_prices(company):
    if os.path.isfile('data/'+company+'_news.csv'):
        return pandas.read_csv('data/'+company+'_news.csv', parse_dates=[1, 3], encoding='latin_1')
    else:
        # The number of merged news points are less than news articles since some are published on non working days.
        # Best case would be to pick a future price, left for later. Doing only 'inner' join for now.
        data = pandas.merge(headlines_for(company), get_prices(company), left_on='Date', right_on='Date')
        data.to_csv('data/'+company+'_news.csv', encoding='latin_1')
        return data


def __punctuation_cleaner(s):
    if s not in string.punctuation:
        return True
    return False


def __stop_word_cleaner(s):
    if s not in feature_extraction.text.ENGLISH_STOP_WORDS:
        return True
    return False


def __stem_cleaner(s):
    return __stemmer.stem(s)


def __regex_filter(s):
    if __words_only.match(s) is not None:
        return True
    return False


def __clean_word(s):
    result = ""
    if s is not None:
        for w in nltk.tokenize.word_tokenize(s.lower()):
            #print w
            if w is not None and __stop_word_cleaner(w) and __punctuation_cleaner(w) and __regex_filter(w):
                result += " " + __stem_cleaner(w)
    #print result
    return result


def pipeline_setup(learning_algo):
    tf_idf = TfidfVectorizer(preprocessor=__clean_word, use_idf=True)
    lsa = TruncatedSVD(n_components=50, n_iter=5, random_state=25)
    pipeline_list = [('tf_idf', tf_idf), ('svd', lsa), ('learning_algo', learning_algo)]
    pipeline = Pipeline(pipeline_list)
    return pipeline


def one_hot(list):
    array = numpy.zeros((len(verbnet.classids())))
    for i in list:
        array[i] = 1
    return array


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

TAGGER = posttagger.get_tagger()
def get_feature_vector(sent):
    # global TAGGER
    # TAGGER = posttagger.get_tagger()
    return findpassives(sent)


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
result=[]
def findpassives(sent):
    # Feature extraction code here.
    """Given a sentence, tag it and print if we think it's a passive-voice
    formation."""
    lancaster_stemmer = LancasterStemmer()
    tagged = tag_sentence(sent)
    tags = map( lambda(tup): tup[1], tagged)
    ansi=[]
    # print sent
    if passivep(tags):
        #file.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag =True
        prevnoun=""
        negative=0
        number=0
        verb=""
        nextnoun=""
        for word, pos in blob.tags:
            #print word,pos
            if (pos=='NN' or pos =='NNP') and flag== True:
                prevnoun= word
            if (pos=='RB'):
                negative=1
            if (pos=='CD'):
                number= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN'or pos=='VB') and flag==True:
                verb=word
                flag= False
            if (pos=='NN' or pos=='NNP') and flag== False:
                nextnoun=word
                break
        lancaster_stemmer.stem(verb)
        #print verb
        if verb=="":
            ansi.append(0)
            ansi.append(negative)
            ansi.append(number)
        elif len(verbnet.classids(verb))==0:
            ans= prevnoun+" "+verb+" "+nextnoun+" "

            ansi.append(0)
            ansi.append(negative)
            ansi.append(number)
        else:
            ans1=verbnet.lemmas()[0:3620].index(verb)

            ansi.append(ans1)
            ansi.append(negative)
            ansi.append(number)
        #fileans.write(ans+'\n')
        result.append(ansi)
        ansi=[]

    else:
        #file1.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag1 =True
        prevnoun1=""
        verb1=""
        nextnoun1=""
        negative=0
        number=0
        for word, pos in blob.tags:
            #print word,pos
            if (pos=='NN' or pos =='NNP') and flag1== True:
                prevnoun1= word
            if (pos=='RB'):
                negative=1
            if (pos=='CD'):
                number= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN'or pos=='VB') and flag1==True:
                verb1=word
                flag1= False
            if (pos=='NN' or pos=='NNP') and flag1== False:
                nextnoun1=word
                break
        lancaster_stemmer.stem(verb1)
        #print verb1
        if verb1=="":
            ansi.append(0)
            ansi.append(negative)
            ansi.append(number)
        elif len(verbnet.classids(verb1))==0:
            ans= prevnoun1+" "+verb1+" "+nextnoun1+" "

            ansi.append(0)
            ansi.append(negative)
            ansi.append(number)

        else:
            ans1=ans1=verbnet.lemmas()[0:3620].index(verb1)

            ansi.append(ans1)
            ansi.append(negative)
            ansi.append(number)
    result.append(ansi)
    ansi=[]


    return result





