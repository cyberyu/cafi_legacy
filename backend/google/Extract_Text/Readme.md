
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
