<div class="row-fluid">
<div class="span9">
<a name="intro"></a>
<h1>Investigating the suitability of Apache Solr and Elasticsearch for Mimas Jorum / Dashboard</h1>

<p><br><br>Report commissioned by Mimas<br><br>

Written by Mark MacGillivray, Founder, Cottage Labs<br><br>

With support from Martyn Whitwell and Richard Jones of Cottage Labs, 
Ben Ryan and Sarah Currier of Mimas.<br><br></p>
</div>

<div class="span3 alert alert-info">
<p>CONTENTS<br><br>
<a href="#intro">Introduction</a><br>
<a href="#problem">Problem</a><br>
<a href="#investigation">Investigation</a><br>
<a href="#solution">Solution</a><br>
<a href="#esexample">Elasticsearch example</a><br>
<a href="#solrexample">Solr example</a><br>
<a href="#readmore">Further reading</a>
</div>

</div>

## Introduction

Whilst working with Mimas on improving their in-house repository interface and custom stats dashboard, it became clear after speccing things out and identifying requirements that a faceted browse frontend over a decent bit of indexing kit would help us achieve many of our goals.

Mimas were already well versed with this sort of tech, having used Apache Solr for a number of years - as we, too, have done. However we have also been using the newer Elasticsearch of late, and along with our anticipation of some particularly tricky queries, we decided spend the first sprint or two investigating these two indexing options.

It is worth noting that at the time of this investigation Mimas use the Solr 3.x versions, as the latest 4.x versions are still in beta.

Also, we do not believe that issues of scale are likely to be so great as to cause problems either for Solr or Elasticsearch in this case, so they are not covered.

<hr class="embossed"></hr>

<a name="problem"></a>
## Problem

The data over which we wish to query consists of metadata records about Open Educational Resources stored in the Jorum repository. In addition, a large amount of statistical data is collected about the events that occur on these OERs - such as their creation, views, and downloads - and that data is used by the stats dashboard, hence also relevant to the indexing problem. Finally, at the time of performing this investigation, it was not possible to be certain of the "shape" of the data, as changes were afoot in how the underlying information was processed and stored; we created an idealised version of the dataset, but interestingly, we also noted that it would be nice to be as flexible as possible about the shape of the data anyway, to maximise potential uses in future.

The queries we hoped to perform included looking for values across both types of record, and also retrieving faceting information across both records; this is where the complexity started to creep in. Consider the following pseudo-query:

<pre><code>
    Return all OERs where
        Language is one of [ en-GB, en-US, en ]
        the OER record was created after 2004
        the source type is HE
    And
        the OER stats indicate it has been DOWNLOADED from within the UK
    And in addition
        return a plot of all the downloads of all identified records in a given time period
        return a count of all the downloads of identified records in a given time period
        return a count of all the views of identified records in a given time period
</code></pre>

Could we do this sort of query in Solr, or in Elasticsearch? Would it be easier or better in one, compared to the other? And given that Mimas already use Solr, is any Elasticsearch advantage sufficiently great to justify introducing a new technology? Let's find out...

<hr class="embossed"></hr>

<a name="investigation"></a>
## Investigation

This sort of query calls for the concept of JOINing data of different types and querying across it. Doing JOINs is not the sort of thing that indexes are good for - relational databases are the tool for that. So we considered combining the different records into one or more indices.

Whilst it is possible to store all the stats with the OER they are about, the queries that can be performed are limited; for example, if an OER had been DOWNLOADED from the UK and also VIEWED from FRANCE, then a query requesting OERs that were DOWNLOADED from FRANCE would return such an OER, even though it was only VIEWED from FRANCE. This is because the relationships between the stats values are lost when stored within the OERs.

Consider this record:

<pre><code>
    {
        "title": "a great OER",
        "stats": [
            {
                "event": "download",
                "from": "UK"
            },
            {
                "event": "view",
                "from": "France"
            }
        ]
    }
</code></pre>

It would be simplified by a sort-of flattening for indexing something like this:

<pre><code>
    {
        "title": "a great OER",
        "stats.event": ["download", "view"],
        "stats.from": ["UK", "France"]
    }
</code></pre>

Hence it would not be possible to find records with a download from the UK - the data is no longer related. A timely example of this can be seen on the Edinburgh Festival Fringe website - try finding show X playing on the evening of day Y; if that show plays on any other evening during the Fringe, but NOT on the evening of day Y, it would stil show up as being available in the evening of day Y, because the query would separately match "Evening" and "day Y".

So we looked for a way round this problem with either indexing option.

<div class="row-fluid">
<div class="span6"><div class="hero-unit">

<h3>Solr</h3>

<p style="font-size:100%;">Due to the inherently flat nature of data stored in a Lucene index, we could not straightforwardly solve this problem with Solr. The only option would be to prepare the data prior to indexing in such a way as to answer a few of the specific queries we hoped to answer, and to create new indices when necessary for supporting other queries in future. New functionality in 4.x may improve this situation, but it is still in development.</p>

<p style="font-size:100%;">We did try creating an index of stats where every stat knew the details of the OER it was about, but from that we could not retrieve counted results about specific OERs; although we successfully applied grouping to the result sets, it is not possible to limit the facet counts by the grouping pre-4.x.</p>

<p style="font-size:100%;">Using an index of OERs containing stats, we have similar problems; using a combination of both indices, we can answer some but only very specifcally defined queries, and future expansion requires new index definitions, which lacks flexibility.</p>

</div></div>
<div class="span6"><div class="hero-unit">

<h3>Elasticsearch</h3>

<p style="font-size:100%;">There are two ways to tackle this problem with Elasticsearch, as it supports both nested documents and parent/child relationships.</p>

<p style="font-size:100%;"><strong>Parent / child</strong> allows for relating two separate datatypes in this manner; create some parent records (OERs), then create some child records (stats) and tell them who their parents are. With this approach, we could query OERs by values relevant to their CHILD stats records, but we could not retrieve complex facet information on the stats without re-issuing a slightly augmented second query to a separate index of stats - a bit clunky. Additionally, this could also be achieved in Solr with two indices anyway, so not a big enough reason to switch.</p>

<p style="font-size:100%;"><strong>Nested documents</strong> allows us to store the stats records effectively <i>inside</i> the OERs they are about whilst maintaining their integrity (so flattening would not appear to occur as in the example above). With this method we can query across the OER and stat values, retrieving relevant OER records along with complex facet information about the stat records themselves.</p>

</div></div>

</div>


### Further considerations

Due to an unsolved problem when performing certain sorts of queries combined with certain sorts of nested facets, I initially recommended that we stick with Solr as I did not think Elasticsearch nested documents could be relied upon. But, after further discussion we realised that the problem is very isolated and that we can meet current requirements with queries that give correct answers, and a very large subset of potential future requirements should be covered without risking incorrect results. After a bit more testing, we found that we could perform sufficiently complex queries on a single elasticsearch index with very little pre-definition, and retrieve all the facet information we desired.

Whilst scaling is not a problem now, would a change of technology present problems in future? Well, if we do decide to keep the index up to date in real time, we can perform partial updates on elasticsearch records to save data transmission. We can also do some other tricks in either indexing solution, so we are not concerned. Overall, Elasticsearch is designed specifically for scaling and is likely to be equal to or more performant than Solr at large scale anyway, so we would not lose out by a switch to Elasticsearch.

What about moving away from known tech? We do not want to make life more complicated for Mimas. Luckily, both Solr and Elasticsearch have the same foundation - they are based on Lucene - and they are both Java apps, and both are very easy to run. Also, Elasticsearch is easier to configure and to scale, so would save effort in the long term. Plus, there is currently no  suitable Solr index in existence at Mimas anyway, so a new one does have to be created somewhere. Finally, considering the limitations of the 3.x version of Solr compared to the current functionality of Elasticsearch and the new functionality in Solr 4.x, a move to a newer version may be required regardless of the outcomes of this project.

What if the shape of the data changes in future? How would current queries work against newer records? Although Solr can be set up with a dynamic schema, it is not designed with that in mind, whereas Elasticsearch is. We can introduce new records in future that have a completely different structure to the current ones, and still easily issue queries against the entire collection. The only restriction on this is that we could not use a key already representing one particular type of data to represent another completely different type of data; as long as we do not violate that rule, then any query will continue to work - although of course, if new records do not contain keys relevant to current queries, they would not be found as results to those queries. The end result here is that Elasticsearch wins out on flexibility.

<hr class="embossed"></hr>

<a name="solution"></a>
## Solution

Sticking with Solr in this instance would limit the queries we could perform, and critically would also add complexity to the current development what with the need to work out suitable pre-processing 
and indexing structures in advance, and before we have a definitive version of the dataset available; it would also add complexity to future upgrades by restricting us to a particular data "shape".

Whilst an Elasticsearch advocate myself, I came into this project hoping to get some work done updating our software to work with Solr again. But given the high risk of the very short timescale on this project, it is a safer option to swap any present Solr development risk for small future Elasticsearch support risk (in terms of Mimas having to maintain a technology new to their stack).

Therefore Elasticsearch is the recommended choice for this project; by using nested documents functionality we can perform complex queries across both the record types and we can retrieve facet information back from those same queries, with very little pre-processing and with hardly any commitment to pre-defined data structure.


<hr class="embossed"></hr>

<a name="esexample"></a>
## Appendix A: Elasticsearch example

We have put together a script that creates a suitable index from our idealised metadata, and provided an example query too. These can be found at <https://gist.github.com/3414096>.

The code that generates our sample metadata is available at <https://github.com/richard-jones/random-paradata>.

The versions of the sample metadata we used can be downloaded from <http://test.cottagelabs.com/jorum>.

And for interest, the example query is shown below (followed by some more useful resources):

<script src="https://gist.github.com/3414096.js?file=query"></script>

<hr class="embossed"></hr>

<a name="solrexample"></a>
## Appendix B: Solr example

We de-normalised the Stats and OER sample files into one large CSV file using Excel and VLOOKUP() function calls. Essentially the format is the same as the Stats file, plus the OER metadata for each statistic. Column headings were adjusted to suit Solr. The file was re-processed to use Unix-like line endings (LF). The de-normalised file can be downloaded from here: <http://test.cottagelabs.com/jorum/denormalised.csv.zip>.

Then we defined a new Solr index with a schema to match the de-normalised CSV file. The schema.xml file can be found here: <http://test.cottagelabs.com/jorum/schema.xml>

<pre><code>
# With the new index initialised, data was loaded using Curl
$ curl http://localhost:8983/solr/update/csv --data-binary @denormalised.csv -H 'Content-type:text/plain; charset=utf-8'

# Once loaded, the changes need to be committed to the index via a blank post
$ java -jar post.jar
</code></pre>

Now the Solr index contained all the information we needed and was ready for querying.

For example, a simple query to find all the statistical events relating to OER documents associated with Birmingham:-

<pre><code>
# returns 215 results (events)
http://localhost:8983/solr/select/?q=birmingham 
</code></pre>

But what we are really interested in are the OER documents, not statistical events, so we can re-normalise the data using grouping:

<pre><code>
# returns 2 results (OER documents)
http://localhost:8983/solr/select/?q=birmingham&group=true&group.field=text_oer_id&group.ngroups=true
</code></pre>

As the stats data is not needed in this output, it can be removed using Solr's FL parameter

<pre><code>
http://localhost:8983/solr/select/?q=birmingham&group=true&group.field=text_oer_id&group.ngroups=true&fl=oer_id,title,description,creator,creator_id,file_format,he_fe,jacs_classification,jacs_code,language,learn_direct_classification,learn_direct_code,publisher,record_origin,web_resource,uploaded_resource
</code></pre>

Now applying this pattern to the earlier problem, namely searching for OERs where the language is en-GB/en-US/en, the source is HE, the OER was created after 2004 and it has been downloaded from the UK, we can write the following query:

<pre><code>
# returns 13 results (OER documents)
http://localhost:8983/solr/select?indent=on&version=2.2&q=%28language%3Aen+OR+language%3Aen-GB+or+language%3Aen-US%29+%2B%28he_fe%3AHE%29+%2Brecord_created_date%3A%5B2004-01-01T00%3A00%3A00.000Z+TO+*%5D+%2B%28statistical_event_lat%3A%5B50+TO+60%5D%29+%2B%28statistical_event_long%3A%5B-10+TO+5%5D%29&fq=&start=0&fl=oer_id,title,description,creator,creator_id,file_format,he_fe,jacs_classification,jacs_code,language,learn_direct_classification,learn_direct_code,publisher,record_origin,web_resource,uploaded_resource&group=true&group.field=text_oer_id&group.main=false&group.ngroups=true
</code></pre>

This results in 13 OER documents which satisfy the constraints of the problem: good! however, with Solr version 3 and below, it is not possible to Facet over grouped results; hence grouped outputs could not drive a faceted view of the data. Version 4 of Solr promises to address this; but the timescales for release are unclear.

The other approach to solving this particular problem is a custom index per query, rather than a "general purpose" index.


<hr class="embossed"></hr>

<a name="readmore"></a>
## Appendix C: Read more about...

### Mimas

<http://mimas.ac.uk/>

### our software

our faceted browse repo: <http://github.com/okfn/facetview>

our Jorum development prototype: <http://test.cottagelabs.com/jorum> (not much there yet...)

### the Jorum software

Jorum beta: <https://jorumbeta.mimas.ac.uk/>

Jorum dashboard prototype: <http://dashboard.jorum.ac.uk/>

### Solr 4.0

<http://wiki.apache.org/solr/Solr4.0>

field collapsing: <http://wiki.apache.org/solr/FieldCollapsing>

group and limit: <http://stackoverflow.com/questions/4302729/solr-how-to-group-by-and-limit>

### elasticsearch

<http://www.elasticsearch.org/>

### elasticsearch nested vs parent / child

support in elasticsearch: <https://github.com/elasticsearch/elasticsearch/issues/1098>

comparison of the approaches: <http://elasticsearch-users.115913.n3.nabble.com/Choosing-Parent-Child-vs-Nested-Document-td3755924.html>

further info re. the flattening phenomenon: <http://www.spacevatican.org/2012/6/3/fun-with-elasticsearch-s-children-and-nested-documents/>

### elasticsearch partial updates:

<http://elasticsearch-users.115913.n3.nabble.com/partial-update-and-nested-type-td3959065.html>

### date histograms problem

in elasticsearch, on facets scoped by nested boolean queries: <https://github.com/elasticsearch/elasticsearch/issues/1645>




Original Title: Investigating the suitability of Apache Solr and Elasticsearch for the Mimas Jorum / Dashboard upgrade.
Original Author: mark
Tags: jorum, news, elasticsearch, solr, mark, martyn
Created: 2012-08-22 1107
Last Modified: 2013-09-22 1650
