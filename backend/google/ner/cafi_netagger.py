__author__ = 'shiyu'

from nltk.tag.stanford import StanfordNERTagger
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from cafi_tokenizer import CAFI_Tokenizer as tkner

#Shyu 's para
# PARA_CLASSPATH="/home/shiyu/cafi_main/backend/google/ner/models/"
# PARA_STANFORD_MODELS="/home/shiyu/cafi_main/backend/google/ner/models/"
# PARA_JAVAHOME="/home/shiyu/Downloads/jre1.8.0_60/bin/java"

#AWS's para
# PARA_CLASSPATH="/home/ubuntu/nermodel"
# PARA_STANFORD_MODELS="/home/ubuntu/nermodel"
# PARA_JAVAHOME="/usr/bin/java"

class CAFI_NETagger:

    def __init__(self):
        #define enviornment variables!
        import os
        # os.environ['CLASSPATH'] = PARA_CLASSPATH  #
        # os.environ['STANFORD_MODELS'] = PARA_STANFORD_MODELS
        # os.environ['JAVAHOME'] = PARA_JAVAHOME

        # self.st = StanfordNERTagger('english.muc.7class.nodistsim.crf.ser.gz')
        # self.st = StanfordNERTagger('english.all.3class.nodistsim.crf.ser.gz')
        self.st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
        self.NELIST_PERSON = []
        self.NELIST_ORGANIZATION = []
        self.NELIST_LOCATION = []
        self.NELIST_MONEY = []

    def stanfordNE2BIO(self,tagged_sent):  # this function is a place holder for boundary detection
        bio_tagged_sent = []
        prev_tag = "O"
        for token, tag in tagged_sent:
            if tag == "O": #O
                bio_tagged_sent.append((token, tag))
                prev_tag = tag
                continue
            if tag != "O" and prev_tag == "O": # Begin NE
                bio_tagged_sent.append((token, "B-"+tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag == tag: # Inside NE
                bio_tagged_sent.append((token, "I-"+tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
                bio_tagged_sent.append((token, "B-"+tag))
                prev_tag = tag

        return bio_tagged_sent

    def stanfordNE2tree(self,ne_tagged_sent):   # this function is a place holder for parsed tree output
        bio_tagged_sent = self.stanfordNE2BIO(ne_tagged_sent)
        sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
        sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

        sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
        ne_tree = conlltags2tree(sent_conlltags)
        return ne_tree

    def get_continuous_chunks(self,tagged_sent): # get continuous chunks from tagged text
        continuous_chunk = []
        current_chunk = []

        for token, tag in tagged_sent:
            if tag != "O":
                current_chunk.append((token, tag))
            else:
                if current_chunk: # if the current chunk is not empty
                    continuous_chunk.append(current_chunk)
                    current_chunk = []

        # Flush the final current_chunk into the continuous_chunk, if any.
        if current_chunk:
            continuous_chunk.append(current_chunk)
        return continuous_chunk

    def get_entities_str_tag(self,cont_chunk):
        #named_entities_str = [" ".join([token for token, tag in ne]) for ne in nes]
        return [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in cont_chunk]

    def get_ne_tags_all(self, intext):  # split the tagged entities into four major class (actually all 7 classes are tagged but current cafi uses 4)

        # auto flush
        self.flush()

        # initialize the tokenizer
        tk = tkner()

        tagged = self.st.tag(tk.tokenize(intext))
        nes = self.get_continuous_chunks(tagged)
        ett = self.get_entities_str_tag(nes)
        for x,y in ett:
            #print x,y
            if y=='PERSON':
                self.NELIST_PERSON.append(x)
            elif y=='ORGANIZATION':
                self.NELIST_ORGANIZATION.append(x)
            elif y=='LOCATION':
                self.NELIST_LOCATION.append(x)
            elif y=='MONEY':
                self.NELIST_MONEY.append(x)


    def get_ne_tags_PERSON(self):   # get the person NE list
        return self.NELIST_PERSON


    def get_ne_tags_ORGANIZATION(self):  # get the organization NE list
        return self.NELIST_ORGANIZATION

    def get_ne_tags_LOCATION(self): # get the locatoin NE list
        return self.NELIST_LOCATION

    def get_ne_tags_MONEY(self):  # get the money NE list
        return self.NELIST_MONEY

    def flush(self):  # flush the NE list holder
        self.NELIST_PERSON = []
        self.NELIST_ORGANIZATION = []
        self.NELIST_LOCATION = []
        self.NELIST_MONEY = []


if __name__=='__main__':

    #initialize the tagger, which costs IO and memory, each instance only needs to initialize this once
    nt = CAFI_NETagger()

    # tag some text
    te = 'Rami Eid is studying at Stony Brook University in New York and he paid tution fee for $100,000'
    nt.get_ne_tags_all(te)

    # output the tags separately
    print nt.get_ne_tags_PERSON()
    print nt.get_ne_tags_ORGANIZATION()
    print nt.get_ne_tags_LOCATION()
    print nt.get_ne_tags_MONEY()

    # flush
    nt.flush()

    te = 'Jingping Xi is visiting UK'
    nt.get_ne_tags_all(te)
    print nt.get_ne_tags_PERSON()
    print nt.get_ne_tags_ORGANIZATION()
    print nt.get_ne_tags_LOCATION()
    print nt.get_ne_tags_MONEY()
    nt.flush()


    long_text = "International Business Machines Corp. dismissed a report stating that massive new layoffs were coming this week for the computing giant. " \
           "A report in Forbes on Thursday said the company was preparing to cut its workforce by 26%, " \
           "which would amount to the largest workforce reductions in IBM's history and affect more than 100,000 employees. " \
           "In an emailed statement, an IBM spokesman reiterated management's comments following its..."
    long_text = "The new system will enable the gold producer to centralize and quickly analyze data about its mining operations. It includes a dashboard of important information enabling the companys management team to make informed decisions about which ore to mine and which extraction processes to use to achieve the best return on investment. Once the project is complete, JSC Altyntau Resources will be able to speed up its annual financial planning cycle from two months to two weeks and ensure that investors are kept informed on the company's operations and forecasts.".decode('ascii', 'ignore')
    nt.get_ne_tags_all(long_text)
    print nt.get_ne_tags_PERSON()
    print nt.get_ne_tags_ORGANIZATION()
    print nt.get_ne_tags_LOCATION()
    print nt.get_ne_tags_MONEY()
    nt.flush()

    f = open('/home/shiyu/test1.csv','r')
    hugetext =  f.readline()
    nt.get_ne_tags_all(hugetext)
    print nt.get_ne_tags_PERSON()
    print nt.get_ne_tags_ORGANIZATION()
    print nt.get_ne_tags_LOCATION()
    print nt.get_ne_tags_MONEY()
    nt.flush()
