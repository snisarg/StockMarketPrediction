"""Tags a sentence with a way-overkill four-level tagger trained from the Brown
Corpus, and then looks at its verbs. If somewhere in the sentence, there's a
to-be verb and then later on a non-gerund, we'll flag the sentence as probably
passive voice."""
from nltk.corpus import verbnet
from textblob import TextBlob
import nltk
import sys
from nltk.stem.lancaster import LancasterStemmer
import os
from itertools import dropwhile
import posttagger

TAGGER = None

def tag_sentence(sent):
    """Take a sentence as a string and return a list of (word, tag) tuples."""
    assert isinstance(sent, basestring)

    tokens = nltk.word_tokenize(sent)
    return TAGGER.tag(tokens)

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

def oneline(sent):
    """Replace CRs and LFs with spaces."""
    return sent.replace("\n", " ").replace("\r", " ")

def print_if_passive(sent):
    """Given a sentence, tag it and print if we think it's a passive-voice
    formation."""
    lancaster_stemmer = LancasterStemmer()
    tagged = tag_sentence(sent)
    tags = map( lambda(tup): tup[1], tagged)

    if passivep(tags):
        file.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag =True
        prevnoun=""
        verb=""
        nextnoun=""
        for word, pos in blob.tags:
            if (pos=='NN' or pos =='NNP') and flag== True:
                prevnoun= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN') and flag==True:
                verb=word
                flag= False
            if (pos=='NN' or pos=='NNP') and flag== False:
                nextnoun=word
                break
        lancaster_stemmer.stem(verb)
        print verb
        if len(verbnet.classids(verb))==0:
            ans= prevnoun+" "+verb+" "+nextnoun+" "
        else:
            ans1=verbnet.classids(verb)
            ansstring=''.join(ans1)
            ans= prevnoun+" "+ansstring+" "+nextnoun+" "
        fileans.write(ans+'\n')

        #print verbnet.classids('acclaim')
        #print "passive:", oneline(sent)
    else:
        file1.write(oneline(sent))
        blob=TextBlob(oneline(sent))
        flag1 =True
        prevnoun1=""
        verb1=""
        nextnoun1=""
        for word, pos in blob.tags:
            #print word,pos
            if (pos=='NN' or pos =='NNP') and flag1== True:
                prevnoun1= word
            if (pos=='VBG' or pos=='RB' or pos=='VBN') and flag1==True:
                verb1=word
                flag1= False
            if (pos=='NN' or pos=='NNP') and flag1== False:
                nextnoun1=word
                break
        lancaster_stemmer.stem(verb1)
        print verb1
        if len(verbnet.classids(verb1))==0:
            ans= prevnoun1+" "+verb1+" "+nextnoun1+" "
        else:
            ans1=verbnet.classids(verb1)
            ansstring=''.join(ans1)
            ans= prevnoun1+" "+ansstring+" "+nextnoun1+" "
        fileans.write(ans+'\n')
    #print verbnet.classids(verb1)

       # print verbnet.lemmas()[1950:1960]
        #print verbnet.classids('memorize')
        #print (verbnet.classids(lemma=var))
        #print "passive:", oneline(sent)
       # file1.write("|*|")
       # print "active:", oneline(sent)

punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()

def findpassives(fn):
    with open(fn) as f:
        text = f.read()
        sentences = punkt.tokenize(text)

        for sent in sentences:
            print_if_passive(sent)

def repl():
    """Read eval (for passivity) print loop."""
    try:
        while True:
            line = raw_input()
            print_if_passive(line)
    except EOFError,e:
        pass

def main():
    global TAGGER
    TAGGER = posttagger.get_tagger()

    if len(sys.argv) > 1:
        for fn in sys.argv[1:]:
            findpassives(fn)
    else:
        repl()

if __name__ == "__main__":
    file = open('passiveoutput.txt', 'w')
    file1 = open('activeoutput.txt', 'w')
    fileans = open('ans.txt', 'w')
    main()
    file.close()
    file1.close()
    fileans.close()