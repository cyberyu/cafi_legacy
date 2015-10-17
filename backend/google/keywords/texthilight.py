__author__ = 'shiyu'

import re
import regex
from google.CustomSearchAPI.searchParser import SearchQueryParser


class Highlighter:
    COLOR = ['red', 'blue', 'orange', 'violet', 'green']

    def highlight (self, text, searchstr, namevariations=None):
        kwlist = self.parseSearchString(searchstr)
        #print kwlist
        if namevariations!=None:
            kwfinal = self.union(kwlist, namevariations)
            return self.addcolor(text,kwfinal)
        else:
            return self.addcolor(text,kwlist)

    def addcolor (self, text, kwlist):
        regmatch = '(\\b' + '\\b)|(\\b'.join(kwlist) + '\\b)'
        regex = re.compile(regmatch, re.I)
        #print regmatch
        i=0; output=""

        if len(regex.findall(text))>=1:  # when there is matched keywords, add color
            i = 0; output = ""
            for m in regex.finditer(text):
                output += "".join([text[i:m.start()],
                                   "<strong><span style='color:%s'>" % self.COLOR[m.lastindex % 5],
                                   text[m.start():m.end()],
                                   "</span></strong>"])
                i = m.end()
            highlighted_text = "".join([output, text[m.end():]])
        else:  # if there is no matched keyword, output the same text
            highlighted_text = text

        return highlighted_text

    def parseSearchString(self, searchstr):
        query = SearchQueryParser()
        return query.Parse(searchstr)

    def union(self,a,b):
        return list(set(a) | set(b))


if __name__ == "__main__":

    h = Highlighter()
    #istring = "(\"joint venture\")&\"IBM\""
    #istring = "(\"joint venture\")"
    istring = "(\"IBM end\")"
    # istring = 'Deloitte'
    #istring = "(\"Lisp Perl Python\")&\"Deloitte\""
    #newqstr = istring[:istring.rfind("&")]
    #newqstr = newqstr.replace('\"','')
    # newqstr = istring


    hiqueryStr= istring

    #hiqueryStr2 =
    text = "Mastek and Deloitte and ibm End Joint Venture"

    #text = """Graham says that Perl is cooler than Java and Python than Perl. In some circles, maybe. Graham uses the example of Slashdot, written in Perl. But what about Advogato, written in C? What about all of the cool P2P stuff being written in all three of the languages? Considering that Perl is older than Java, and was at one time the Next Big Language, I think you would have a hard time getting statistical evidence that programmers consider Perl "cooler" than Java, except perhaps by virtue of the fact that Java has spent a few years as the "industry standard" (and is thus uncool for the same reason that the Spice Girls are uncool) and Perl is still "underground" (and thus cool, for the same reason that ambient is cool). Python is even more "underground" than Perl (and thus cooler?). Maybe all Graham has demonstrated is that proximity to Lisp drives a language underground. Except that he's got the proximity to Lisp argument backwards too."""
    print h.highlight(text, hiqueryStr, None)
