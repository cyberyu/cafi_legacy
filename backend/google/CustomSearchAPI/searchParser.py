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
        operatorOr = Forward()

        operatorWord = Group(Combine(Word(alphanums) + Suppress('*'))).setResultsName('wordwildcard') | \
                            Group(Word(alphanums)).setResultsName('word')

        operatorQuotesContent = Forward()
        operatorQuotesContent << (
            (operatorWord + operatorQuotesContent) | operatorWord
        )

        operatorQuotes = Group(
            Suppress('"') + operatorQuotesContent + Suppress('"')
        ).setResultsName("quotes") | operatorWord

        operatorParenthesis = Group(
            (Suppress("(") + operatorOr + Suppress(")"))
        ).setResultsName("parenthesis") | operatorQuotes

        operatorNot = Forward()
        operatorNot << (Group(
            Suppress(Keyword("not", caseless=True)) + operatorNot
        ).setResultsName("not") | operatorParenthesis)

        operatorAnd = Forward()
        operatorAnd << (Group(
            operatorNot + Suppress(Keyword("&", caseless=True)) + operatorAnd
        ).setResultsName("&") | Group(
            operatorNot + OneOrMore(~oneOf("& |") + operatorAnd)
        ).setResultsName("&") | operatorNot)

        operatorOr << (Group(
            operatorAnd + Suppress(Keyword("|", caseless=True)) + operatorOr
        ).setResultsName("|") | operatorAnd)

        return operatorOr.parseString

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

    def Parse(self, query):
        self.genString=""
        self.parsed = self._parser(query)[0]
        self.generate(self._parser(query)[0])
        self.keywordsFinal= self.keywords
        self.keywordsFinal.difference_update(self.keywordsRemove)
        self.keywordsFinal = list(self.keywordsFinal) #Converting it to a list
        return self.parsed,self.genString

class ParserTest():
    """Tests the parser with some search queries
    """
    def __init__(self):
        self.Test()

    def Test(self):

        query = SearchQueryParser()
        #item = "(lawsuit* | court* | violation & greed failure |\"joint venture\"|\"teaming agreement\"|\"memorandom of understanding\"| illegal | regulation* | defandant)"
        item = "(\"joint venture\" | \"jv\" | \"mou\" | \"memorandum of understanding\" | \"strategic alliance\" | \"teaming agreement\" | \"strategic partner*\" | \"partner\" | \"supplier\" | \"provider\" | \"agreement\" | \"contract\" | \"component\" | \"subcontract*\" | \"receive\" | \"win*\")&\"Microsoft\""
        #item = "(\"joint venture\" | hello |\"mou\")&\"Microsoft\""

        print "Input Query:"+item
        ParsedList,reGengString = query.Parse(item)
        print "Parsed List:",
        print ParsedList #Parsed List from query
        print "ReGenerated String:"+reGengString #regenerated string from the parsed list
        print "Keywords Final:",
        print query.keywordsFinal
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


