__author__ = 'tanmoy'

from pyparsing import *
from sets import Set
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
        self.parsed = []
        self.genString = "" #generating string back from Data Structure

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
        #x.intersection(y)

    def generateOr(self, argument):

        x = self.generate(argument[0])
        self.genString += " |"
        y = self.generate(argument[1])
        #x.union(y)

    def generateNot(self, argument):
        self.genString += "Not "
        self.generate(argument[0])

    def generateParenthesis(self, argument):
        self.genString += "("
        x = self.generate(argument[0])
        self.genString += ")"
        #x

    def generateQuotes(self, argument):
        """generate quoted strings

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

        self.genString += "\""
        #' '.join(search_terms)

    def generateWord(self, argument):
        self.genString += " "+argument[0]

    def generateWordWildcard(self, argument):
        self.genString += " "+ argument[0]+'* '

    def generate(self, argument):
        return self._methods[argument.getName()](argument)

    def Parse(self, query):
        self.genString=""
        self.parsed = self._parser(query)[0]
        print self.parsed
        self.generate(self._parser(query)[0])
        return self.parsed,self.genString

class ParserTest(SearchQueryParser):
    """Tests the parser with some search queries
    """
    def Test(self):

        query = SearchQueryParser()
        item = "(lawsuit* | court* | violation | illegal | regulation* | defandant)"
        print "Input Query:"+item
        ParsedList,reGengString = query.Parse(item)
        print "Parsed List:",
        print ParsedList #Parsed List from query
        print "ReGenerated String:"+reGengString #regenerated string from the parsed list
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
    ParserTest().Test()
    print 'Completed'


