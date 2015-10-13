
**Install Apache Tika**
--------------------
```
$ wget http://www.apache.org/dyn/closer.cgi/tika/tika-server-1.10.jar
```

To be able to set up and run such a server like this:
```
$ java -jar tika-server-1.10.jar --port 1234
```
Usage
-----
HTTP PUT a document to parse with Tika
  			
  PUT document to get text
	curl -T pom.pdf http://localhost:1234/tika
		returns textual content, if any, as json
  

HTTP Codes returned
-------------------
200 - Ok
404 - Document not found
415 - Unknown file type
422 - Unparsable document of known type (password protected documents and unsupported versions like Biff5 Excel)
500 - Internal error

Install python-boilerpipe
-------------------------

A python wrapper for Boilerpipe_, an excellent Java library for boilerplate removal and fulltext extraction from HTML pages. 

Configuration
-------------

Dependencies:
jpype, charade

The boilerpipe jar files will get fetched and included automatically when building the package.
```
pip install JPype1    # to install https://pypi.python.org/pypi/JPype1
pip install charade
pip install boilerpipe

Be sure to have set JAVA_HOME properly since jpype depends on this setting.
```

Usage
-----

The constructor takes a keyword argment ``extractor``, being one of the available boilerpipe extractor types:

- DefaultExtractor
- ArticleExtractor
- ArticleSentencesExtractor
- KeepEverythingExtractor
- KeepEverythingWithMinKWordsExtractor
- LargestContentExtractor
- NumWordsRulesExtractor
- CanolaExtractor

If no extractor is passed the DefaultExtractor will be used by default. Additional keyword arguments are either ``html`` for HTML text or ``url``.