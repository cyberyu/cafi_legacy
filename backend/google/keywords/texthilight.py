__author__ = 'shiyu'

import re
import regex
from google.CustomSearchAPI.searchParser import SearchQueryParser


class Highlighter:
    COLOR = ['red', 'blue', 'orange', 'violet', 'green']

    def highlight (self, text, searchstr, namevariations=None):
        kwlist = self.parseSearchString(searchstr)

        if namevariations!=None:
            kwfinal = self.union(kwlist, namevariations)
            return self.addcolor(text,kwfinal)
        else:
            kwlist = self.parseSearchString(searchstr)
            return self.addcolor(text,kwlist)


    def addcolor (self, text, kwlist):
        regmatch = '(\\b' + '\\b)|(\\b'.join(kwlist) + '\\b)'
        regex = re.compile(regmatch, re.I)

        i=0; output="<html>"

        if len(regex.findall(text))>1:  # when there is matched keywords, add color
            for m in regex.finditer(text):
                output += "".join([text[i:m.start()],
                        "<strong><span style='color:%s'>" % self.COLOR[m.lastindex % 5],
                                  text[m.start():m.end()],
                                  "</span></strong>"])

            i=m.end()
            highlighted_text = "".join([output, text[m.end():],  "</html>"])
        else:  # if there is no matched keyword, output the same text
            highlighted_text = text

        return highlighted_text



    def parseSearchString(self, searchstr):
        query = SearchQueryParser()
        query.Parse(searchstr)
        return query.keywords


    def union(self,a,b):
        return list(set(a) | set(b))


if __name__ == "__main__":

    text = unicode("""Every day, in more than 100 countries around the world, thousands of Microsoft Student Partners (MSPs) share their deep knowledge and passion for technology with their fellow students""", "utf-8")
    text2 = "Contracts - Microsoft Research"
    searchstr = "(joint venture | jv | mou | memorandum of understanding | strategic alliance | teaming agreement | strategic partner* | partner | supplier | provider | agreement | contract | component | subcontract* | receive | win*)"
    searchstr2 ='("joint venture" | "jv" | "mou" | "memorandum of understanding" | "strategic alliance" | "teaming agreement" | "strategic partner*" | "partner" | "supplier" | "provider" | "agreement" | "contract" | "component" | "subcontract*" | "receive" | "win*")'
    searchstr3 = searchstr2.replace('"','')
    searchstr4 = '("joint venture" | "jv" | "mou" | "memorandum of understanding" | "strategic alliance" | "teaming agreement" | "strategic partner*" | "partner" | "supplier" | "provider" | "agreement" | "contract" | "component" | "subcontract*" | "receive" | "win*")&"IBM Global Business Service"'
    searchstr4 = searchstr4[:searchstr4.rfind("&")]
    searchstr4 = searchstr4.replace('\"','')
    searchstr5 = "(joint venture | jv | mou | memorandum of understanding | strategic alliance | teaming agreement |  strategic partner* | partner | supplier | provider | agreement | contract | component | subcontract* | receive | win*)"
    nv = ['microsoft','micrsoft asia']
    h = Highlighter()

    print h.highlight(text, searchstr5, nv)
