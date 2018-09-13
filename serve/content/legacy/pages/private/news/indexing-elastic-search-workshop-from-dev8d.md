This is an overview of what we covered at the [Dev8d](http://dev8d.org) [Indexing and elasticsearch](http://data.dev8d.org/2012/programme/?event=CS42) workshop.

## Install

To see our notes from the day: <http://pad.cottagelabs.com/es>

For Windows instructions on how to install and run the example dataset conversion script: <http://pad.cottagelabs.com/eswin>

Installing is just a matter of having java and getting and unzipping the file from <http://www.elasticsearch.org/download>

Try this:

<code>
<pre>
wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.18.7.tar.gz

tar -xzvf elasticsearch-0.18.7.tar.gz

elasticsearch-0.18.7/bin/elasticsearch start
</pre>
</code>

If you wait a minute for it to start up, try requesting the main URL to see if it is running (can do this in a web browser, or using command line)

<pre>
'''the main URL'''
curl localhost:9200

'''the status URL - shows some details including list of indices available (none at start)'''
curl localhost:9200/_status

'''the cluster health URL - yellow or green is good'''
curl http://localhost:9200/_cluster/health
</pre>


## Indexing stuff

Now that you have it up and running:

<code>
<pre>
'''to create an index'''
curl -X POST localhost:9200/test

'''should return'''
{"ok":true,"acknowledged":true}

'''put something in your index'''
$ curl -X POST localhost:9200/test/record -d '{"hello" : "world"}'

'''should return'''
{"ok":true,"_index":"john","_type":"record","_id":"NQ7woVigTcCJjpRW3HU9zQ","_version":1}
</pre>
</code>

## Retrieving stuff

<code>
<pre>
'''retrieve the record previously indexed (see the ID above, change for your own example)'''
curl -X GET localhost:9200/test/record/NQ7woVigTcCJjpRW3HU9zQ

'''returns a result object with the record in the _source key'''
{"_index":"john","_type":"record","_id":"NQ7woVigTcCJjpRW3HU9zQ","_version":1,"exists":true, "_source" : {"hello" : "world"}}

'''create a record with a specified identifier'''
curl -X PUT localhost:9200/john/record/myfirstrecord -d '{"hello" : "world"}'

'''and can then be retrieved with that identifier'''
curl -X GET localhost:9200/test/record/myfirstrecord
</pre>
</code>


## Indexing datasets

Here is an example python script to get JSON records from a file into your index:

<code>
<pre>
import json
import httplib

infile = open('kv.json')
jsonin = json.load(infile)

for record in jsonin:
    conn = httplib.HTTPConnection('localhost:9200')
    conn.request("POST", "/test/record", json.dumps(record))
    result = conn.getresponse()
</pre>
</code>

For an example of porting some XML into a suitable JSON file, see this gist: <http://gist.github.com/1852712>.


## Example queries

<code>
<pre>
'''Query everything:'''
curl http://localhost:9200/john/record/_search?q=*

'''Query a specific string'''
curl http://localhost:9200/john/record/_search?q=lindefors

'''Query a specific field for a specific string'''
curl http://localhost:9200/john/record/_search?q=author:lindefors

'''With wildcard'''
curl http://localhost:9200/john/record/_search?q=author:lindef*

'''With boolean'''
curl http://localhost:9200/john/record/_search?q=author:lindef* AND month:may

'''Search all object types'''
curl http://localhost:9200/john/_search?q=*

'''Search across all indices'''
curl http://localhost:9200/_search?q=*

'''append this to pretty-print your json'''
&pretty=true
</pre>
</code>


## Mappings

When you index stuff, it is dynamically mapped by elasticsearch - there is no need to write a schema in advance! You can find out what keys have been mapped, and how, at the mapping URL:

<code>
<pre>
curl http://localhost:9200/test/record/_mapping
</pre>
</code>

You can also specify a mapping (just send a JSON object to the URL) and you can even specify a mapping that remains dynamic apart from the bits you specify. Very flexible. Just check out the elasticsearch website for more details.


## Useful links

* <http://okfnlabs.org/facetview>
* <http://bibsoup.net>
* <http://www.elasticsearch.org>
* <https://github.com/mbostock/d3>
* <http://django-haystack.readthedocs.org/en/latest/index.html> (ElasticSearch integration for Django)



Original Title: Indexing elasticsearch workshop from dev8d
Original Author: richard
Tags: conference, dev8d, elasticsearch, indexing, mark, richard, tutorial
Created: 2012-02-17 1210
Last Modified: 2013-12-09 2338
