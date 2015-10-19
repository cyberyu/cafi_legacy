__author__ = 'shiyu'

import re
import regex
from google.CustomSearchAPI.searchParser import SearchQueryParser
from google.ner.cafi_netagger import CAFI_NETagger

KEYWORDS_PATTERN = "<span style='color:%s'>"
EN_PERSON_PATTERN = "<span style='background-color: #F5D0A9'>"
EN_ORGANIZATION_PATTERN = "<span style='background-color: #FFFF00'>"
EN_LOCATION_PATTERN = "<span style='background-color: #819FF7'>"
EN_MONEY_PATTERN = "<span style='background-color: #D0F5A9'>"
KWCOLOR = ['blue', 'red', 'orange', 'violet', 'green']


class Highlighter:

    def __init__(self):
        self.patterns_keywords = KEYWORDS_PATTERN
        self.patterns_en_person = EN_PERSON_PATTERN
        self.patterns_en_organization = EN_ORGANIZATION_PATTERN
        self.patterns_en_location = EN_LOCATION_PATTERN
        self.patterns_en_money = EN_MONEY_PATTERN
        self.keyword_color = KWCOLOR

    def highlight (self, text, searchstr, namevariations=None):
        kwlist = self.parseSearchString(searchstr)
        if namevariations!=None:
            kwfinal = self.union(kwlist, namevariations)
            return self.addcolor(text,kwfinal)
        else:
            return self.addcolor(text,kwlist)


    def highlight_kw_ne (self,text,searchstr,ne_person,ne_org,ne_loc,ne_money):
        kwlist = self.parseSearchString(searchstr)
        ne_person = self.substraction(ne_person, kwlist)  # remove the NEs which occur in keywords
        ne_org = self.substraction(ne_org, kwlist)  # remove the NEs which occur in keywords
        ne_loc = self.substraction(ne_loc, kwlist)  # remove the NEs which occur in keywords
        ne_money = self.substraction(ne_money, kwlist)  # remove the NEs which occur in keywords

        hi_kw = self.addcolor(text,kwlist)
        hi_per = self.highlight_entities(hi_kw,ne_person,'person')
        hi_org = self.highlight_entities(hi_per,ne_org,'organization')
        hi_loc = self.highlight_entities(hi_org,ne_loc,'location')
        hi_mny = self.highlight_entities(hi_loc,ne_money,'money')

        return hi_mny


    def addcolor (self, text, kwlist):
        regmatch = '(\\b' + '\\b)|(\\b'.join(kwlist) + '\\b)'
        regex = re.compile(regmatch, re.I)
        i=0; output=""

        if len(regex.findall(text))>=1:  # when there is matched keywords, add color
            i = 0; output = ""
            for m in regex.finditer(text):
                output += "".join([text[i:m.start()],
                                   "<strong><span class='text-danger'>", text[m.start():m.end()],
                                   "</span></strong>"])
                i = m.end()
            highlighted_text = "".join([output, text[m.end():]])
        else:  # if there is no matched keyword, output the same text
            highlighted_text = text

        return highlighted_text


    def highlight_entities(self,text,enlist,type):

        if type=="person":
            pattern = self.patterns_en_person
        elif type=="organization":
            pattern = self.patterns_en_organization
        elif type=="location":
            pattern = self.patterns_en_location
        elif type=="money":
            pattern = self.patterns_en_money

        if len(enlist)>0:
            regmatch = '(\\b' + '\\b)|(\\b'.join(enlist) + '\\b)'

            print regmatch
            regex = re.compile(regmatch, re.I)
            i=0; output=""

            if len(regex.findall(text))>=1:  # when there is matched keywords, add color
                i = 0; output = ""
                for m in regex.finditer(text):
                    output += "".join([text[i:m.start()],
                                       "<strong>", pattern,
                                       text[m.start():m.end()],
                                       "</span></strong>"])
                    i = m.end()
                highlighted_text = "".join([output, text[m.end():]])
            else:  # if there is no matched keyword, output the same text
                highlighted_text = text

            return highlighted_text
        else:
            return text


    def parseSearchString(self, searchstr):
        query = SearchQueryParser()
        print query.Parse(searchstr), '-----'
        return query.Parse(searchstr)

    def union(self,a,b):
        return list(set(a) | set(b))

    def substraction(self,a,b):
        return list(set(a) - set(b))


if __name__ == "__main__":


    #istring = "(\"joint venture\")&\"IBM\""
    #istring = "(\"joint venture\")"
    istring = "(\"Forbes\" | \"layoffs\" | \"employees\" )"
    # istring = 'Deloitte'
    #istring = "(\"Lisp Perl Python\")&\"Deloitte\""
    #newqstr = istring[:istring.rfind("&")]
    #newqstr = newqstr.replace('\"','')
    # newqstr = istring


    hiqueryStr= istring

    #hiqueryStr2 =
    text = "Mastek and Deloitte and ibm end Joint Venture"

    long_text = "International Business Machines Corp. dismissed a report stating that massive new layoffs were coming this week for the computing giant. " \
           "A report in Forbes on Thursday said the company was preparing to cut its workforce by 26%, " \
           "which would amount to the largest workforce reductions in IBM's history and affect more than 100,000 employees. " \
           "In an emailed statement, an IBM spokesman reiterated management's comments following its... It could save the operation expense for 10 million dollars ... Reported by Tom Hanks, New York"

    # USE CASE ----------------------------------------

    h = Highlighter()   # intialize the highlighter

    nt = CAFI_NETagger()  # intialize the tagger

    nt.get_ne_tags_all(long_text)  # tag the text

    # highlight the text using tagged entities
    hi_kw_ne = h.highlight_kw_ne(long_text,   # tring of text to be highlighted
                                 hiqueryStr,  # string of search keywords
                                 nt.get_ne_tags_PERSON(),  # list of tagged person names
                                 nt.get_ne_tags_ORGANIZATION(), # list of tagged company names
                                 nt.get_ne_tags_LOCATION(),  # list of tagged locations
                                 nt.get_ne_tags_MONEY())  # list of tagged money

    nt.flush() # flush the tagger for reuse

    print hi_kw_ne



