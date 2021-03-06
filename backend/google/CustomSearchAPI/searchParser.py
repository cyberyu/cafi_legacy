__author__ = 'tanmoy'

from pyparsing import *
from sets import Set
import re

#import pickle

class SearchQueryParser:

    def __init__(self):
        self._methods = {
            '&': self.generateAnd,
            '|': self.generateOr,
            'not':self.generateNot,
            'parenthesis': self.generateParenthesis,
            'quotes': self.generateQuotes,
            'word': self.generateWord,
            'wordwildcard': self.generateWordWildcard,
            #add more if you want to later
        }
        self._parser = self.parser()
        self.query = ""
        self.parsed = []
        self.genString = "" #generating string back from Data Structure
        self.keywords = set()
        self.keywordsRemove = set() #remove keywords which appear alone in a quotation
        self.keywordsFinal = set() #Add the variable to display keywords maintaining the inherent structure of phrase

    def parser(self):
        """
        This function returns a parser.
        Grammar:
        - a query consists of alphanumeric words, with an optional '*' wildcard
          at the end of a word
        - a sequence of words between quotes is a literal string
        - words can be used together by using operators ('&' or '|')
        - words with operators can be grouped with parenthesis
        - a word or group of words can be preceded by a 'not' operator
        - the '&' operator precedes an '|' operator
        - if an operator is missing, use an '&' operator
        & (And) |(Or)
        """
        opOr = Forward()

        opWord = Group(Combine(Word(alphanums) + Suppress('*'))).setResultsName('wordwildcard') | \
                            Group(Word(alphanums)).setResultsName('word')

        opQuotesContent = Forward()

        opQuotesContent << (
            (opWord + opQuotesContent) | opWord
        )

        opQuotes = Group(
            Suppress('"') + opQuotesContent + Suppress('"')
        ).setResultsName("quotes") | opWord


        opParenthesis = Group(
            (Suppress("(") + opOr + Suppress(")"))
        ).setResultsName("parenthesis") | opQuotes

        opNot = Forward()
        opNot << (Group(
            Suppress(Keyword("not", caseless=True)) + opNot
        ).setResultsName("not") | opParenthesis)

        opAnd = Forward()
        opAnd << (Group(
            opNot + Suppress(Keyword("&", caseless=True)) + opAnd
        ).setResultsName("&") | Group(
            opNot + OneOrMore(~oneOf("& |") + opAnd)
        ).setResultsName("&") | opNot)

        opOr << (Group(
            opAnd + Suppress(Keyword("|", caseless=True)) + opOr
        ).setResultsName("|") | opAnd)

        return opOr.parseString

    def generateAnd(self, argument):
        x = self.generate(argument[0])
        self.genString += " & "
        y = self.generate(argument[1])
        return x.intersection(y)

    def generateOr(self, argument):

        x = self.generate(argument[0])
        self.genString += " |"
        y = self.generate(argument[1])
        return x.union(y)

    def generateNot(self, argument):
        self.genString += "not "
        self.keywordsRemove.update(argument[0])
        return self.GetNot(self.generate(argument[0]))

    def generateParenthesis(self, argument):
        self.genString += "("
        x = self.generate(argument[0])
        self.genString += ")"
        return x

    def generateQuotes(self, argument):
        """ generate quoted strings
            It does an 'and' on the indidual search terms
        """
        r = Set()
        search_terms = []
        self.genString += "\""

        for item in argument:
            search_terms.append(item[0])
            if len(r) == 0:
                r = self.generate(item)
            else:
                r = r.intersection(self.generate(item))
            if len(argument)>1:
                self.keywordsRemove.update(item)

        self.genString += "\""
        return self.GetQuotes(" ".join(search_terms), r)


    def generateWord(self, argument):
        self.genString += " "+argument[0]
        return self.GetWord(argument[0])

    def generateWordWildcard(self, argument):
        self.genString += " "+ argument[0]+'* '
        return self.GetWordWildcard(argument[0])

    def generate(self, argument):
        return self._methods[argument.getName()](argument)

    def GetWord(self, word):
        self.keywords.update([word])
        return Set()

    def GetWordWildcard(self, word):
        self.keywords.update([word])
        return Set()

    def GetQuotes(self, search_string, tmp_result):
        self.keywords.update([search_string])
        return Set()


    def GetNot(self, not_set):
        return Set().difference(not_set)

    def Parse(self, query): # Return Final list of keywords
        self.genString=""
        query = re.sub('[^A-Za-z0-9|& \"*()]+', '', query)
        self.query = query
        try:
            self.parsed = self._parser(query)[0]
            self.generate(self._parser(query)[0])
            self.keywordsFinal= self.keywords
            self.keywordsFinal.difference_update(self.keywordsRemove)
            self.keywordsFinal = list(self.keywordsFinal) #Converting it to a list
            return self.keywordsFinal
        except Exception:
            query = ' | '.join(re.compile(r"\w{4,}").findall(query))
            #print query
            self.parsed = self._parser(query)[0]
            self.generate(self._parser(query)[0])
            self.keywordsFinal= self.keywords
            self.keywordsFinal.difference_update(self.keywordsRemove)
            self.keywordsFinal = list(self.keywordsFinal) #Converting it to a list
            return self.keywordsFinal


class ParserTest():
    """Tests the parser with some search queries
    """
    def __init__(self):
        self.Test()

    def Test(self):

        query = SearchQueryParser()
        #item = "(lawsuit* | court* | violation & greed failure |\"joint venture\"|\"teaming agreement\"|\"memorandom of understanding\"| illegal | regulation* | defandant)"
        #item = "(\"joint venture\" | ( \"jv of honey's\" ) | \"mou\" | \"memorandum of understanding\" | \"strategic alliance\" | \"teaming agreement\" | \"strategic partner*\" | \"partner\" | \"supplier\" | \"provider\" | \"agreement\" | \"contract\" | \"component\" | \"subcontract*\" | \"receive\" | \"win*\" )&\"Microsoft\""
        item = "((not rain<5 | \"snow\'s\") & cold)"
        #item = " mcDonald's | kfc"
        import sys
        item = sys.argv[1]
        print "Input Query:"+item
        keywordsFinal = query.Parse(item)

        print "Parsed List:",
        print query.parsed  #Parsed List from query
        print "ReGenerated String:"+ query.genString    #regenerated string from the parsed list
        print "Keywords Final:",
        print keywordsFinal

        '''
        ##Use of pickle to serialize a complex list
        pickle.dump(query, file('parsedList.pickle','w'))
        del query
        query2 = pickle.load(file('parsedList.pickle'))
        print query2
        print query2.genString
        return "all_ok"
        '''

if __name__=='__main__':
    ParserTest()
    print 'Completed'