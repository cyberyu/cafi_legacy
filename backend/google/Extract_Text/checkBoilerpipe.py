__author__ = 'tanmoy'

# Lot left to experiment. Few initial lines of code. Will have to write test cases to check which is better

from boilerpipe.extract import Extractor

url = "https://www.endicottalliance.org/jobcutsreports.php"
extractor = Extractor(extractor='ArticleExtractor', url=url)
extracted_text = extractor.getText()
print extracted_text
