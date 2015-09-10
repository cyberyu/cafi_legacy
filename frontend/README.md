# Consumer Complaint Search Front-End

A flexible front-end for ElasticSearch

![Screenshot](screenshot.png)


## Dependencies

In order to run this code, you will need to have the following installed
  1. [elasticsearch](http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_installing_elasticsearch.html)
  2. Node.JS / NPM
  3. [bower](http://bower.io/#install-bower)

You will also need to configure elasticsearch to accept requests from the browser using [CORS](http://en.wikipedia.org/wiki/Cross-origin_resource_sharing). To enable CORS, add the following to elasticsearch's config file. Usually, this file is located near the elasticsearch executable at `config/elasticsearch.yml`.

```yml
http.cors:
  enabled: true
  allow-origin: /https?:\/\/localhost(:[0-9]+)?/
```

Please check the `package.json` and `bower.json` for library dependencies.

## Installation
1.  Clone this repository from your desired location: `git clone git@github.cfpb.gov:[account]/complaint-analytics-search-tool.
2.  `npm install` - this will also run the Bower Install commands.
3.  `grunt build`
4.  `cd dist`
5.  `python -m SimpleHTTPServer` to serve files via `localhost:8000`, or use your server of choice to view files in the browser.

## Configuration

If the software is configurable, describe it in detail, either here or in other documentation to which you link.

## Usage

To be determined

## How to test the software

If the software includes automated tests, detail how to run those tests.

## Known issues

Document any known significant shortcomings with the software.

## Getting help

Instruct users how to get help with this software; this might include links to an issue tracker, wiki, mailing list, etc.

**Example**

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

This section should detail why people should get involved and describe key areas you are
currently focusing on; e.g., trying to get feedback on features, fixing certain bugs, building
important pieces, etc.

General instructions on _how_ to contribute should be stated with a link to [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info
Please see the parent repository for further details.


----

## Credits and references

1. ElasticSearch JavaScript SDK
2. Elastic.JS
3. Eric Spalger's Angular + ElasticSearch Example
4. ElastiUI for inspiration on writing directives

...
1. Projects that inspired you
2. Related projects
3. Books, papers, talks, or other sources that have meaniginful impact or influence on this project
