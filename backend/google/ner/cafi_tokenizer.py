__author__ = 'shiyu'

import nltk

class CAFI_Tokenizer:

    def __init__(self):

        self.tokenizer_rule = r'''(?x)      # set flag to allow verbose regexps
              ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?():-_`]      # these are separate tokens
        '''

    def textcleanse(self,intext):
        return unicode(intext, 'ascii', 'ignore')


    def tokenize(self,intext):
        return nltk.regexp_tokenize(self.textcleanse(intext), self.tokenizer_rule)


if __name__=='__main__':
    text = "International Business Machines Corp. dismissed a report stating that massive new layoffs were coming this week for the computing giant. " \
           "A report in Forbes on Thursday said the company was preparing to cut its workforce by 26%, " \
           "which would amount to the largest workforce reductions in IBM's history and affect more than 100,000 employees. " \
           "In an emailed statement, an IBM spokesman reiterated management's comments following its..."
    tk = CAFI_Tokenizer()
    print tk.tokenize(text)
