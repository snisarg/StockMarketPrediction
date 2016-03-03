"""Tags a sentence with a way-overkill four-level tagger trained from the Brown
Corpus, and then looks at its verbs. If somewhere in the sentence, there's a
to-be verb and then later on a non-gerund, we'll flag the sentence as probably
passive voice."""
from textblob import TextBlob
import nltk
import sys
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
            if pos=='NN' and flag== True:
                prevnoun= word
            if pos=='VBG' or pos=='RB' or pos=='VBN':
                verb=word
                flag= False
            if pos=='NN' and flag== False:
                nextnoun=word
                break
        ans= prevnoun+" "+verb+" "+nextnoun+" "

        fileans.write(ans+'\n')
        print "passive:", oneline(sent)
    else:
        file1.write(oneline(sent))
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