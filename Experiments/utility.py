from textblob import TextBlob
import passive
import posttagger
import nltk
"""
Extracting sentences from document
"""
blob= TextBlob("Mansee is a good Girl. Perhaps she is the best girl ever 300 third.")
blob1= TextBlob("  A program called Maximus is included by UNR.")
blob2= TextBlob("Samsung Electronics has been sued by Apple Electronics for copying the 1415 of its iPad tablet and iPhone smartphone")
for sentence in blob2.sentences:
    print sentence
"""
Printing one sentence
"""
#ans= blob2.sentences[0]
#ans = TextBlob(blob.sentences[1])
#print ans
"""
Extracting noun phrases
"""
#for np in blob2.noun_phrases:
   # print np
"""
Tagging parts of speech
"""
for word, pos in blob1.tags:
    print word,pos

punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
with open('passiveoutput.txt') as f:
        text = f.read()
        blob3 = TextBlob(text)
        sentences = punkt.tokenize(text)
        for sent in sentences:
            print sent

with open('passiveoutput.txt', 'r') as in_file:
    text = in_file.read()
    sents = nltk.sent_tokenize(text)


