<div class="row-fluid">
<div class="hero-unit">
<h1>XCRI-CAP: Final report</h1>
</div>
</div>


<div class="row-fluid">
<div class="span6">

<h2>Introduction</h2>

<p>In September 2012 we started working with Rob Englebright at Jisc to do a bit of investigating into recent work to produce feeds of data about course information from UK Further and Higher education establishments. The previous phase of Jisc-funded work had developed some exemplar rich course metadata feeds from numerous institutes, making them available via application programming interfaces and a registry of such interfaces.</p>

<p>The aims of our investigations - along with other people running similar small projects, was to find out how well the new data feeds could be used and to come back with some example uses. So we proposed to build an easily searchable, navigable, up to date aggregation of all the metadata available via the registered feeds, presented on an HTML5 website viewable on modern devices from desktops to smartphones; and to provide feedback on the process of doing so.</p>
</div>

<div class="span6">
<img src="https://docs.google.com/drawings/pub?id=1acTEjMW9d55lr_cLKHb8DvJMWeOQZJ0u1nR4ioe1ko0&amp;w=1013&amp;h=423">
</div>

</div>



<hr></hr>


## What we did

### Find the data

We began with some preliminary work to understand how widely used XCRI data is and how easy it is to find, using just basic internet searching and intuition. We wanted to approach this from the perspective of someone who wants to aggregate or automatically acquire course information, but who might not strictly know about XCRI.  So: a technical user, who's comfortable exploring a relatively technical side of the web to find the information they are looking for. Following on from any search results we used a "follow your nose" approach with the objective of locating XCRI formatted resources/APIs for inclusion into our demonstrator.

It was relatively easy to find resources about XCRI as a standard, in particular <a href="http://www.xcri.co.uk">the XCRI Knowledge Base</a>, which links out to <a href="http://www.xcri.org/forum/">the XCRI forum</a> and <a href="http://www.xcri.org/wiki/index.php/XCRI_Wiki">the XCRI wiki</a>.  Their principle focus is to support the community of XCRI implementers, and the <a href="http://xxp.igsl.co.uk/app/xcridirectory">XCRI directory</a> and <a href="http://www.xcri.org/wiki/index.php/XCRI_Feeds">XCRI wiki page</a> turned out to be the best place to discover links to endpoints. The <a href="http://www.xcri.co.uk">the XCRI Knowledge Base</a> includes an <a href="http://coursedata.k-int.com/discover/">aggregator of its own</a>, which provides access to around 1500 course data resources via a basic faceted browse and search interface.

One thing we noted at this point, however, was that there is very little information available on institutional websites about their XCRI feeds - without knowing about XCRI in the first place, there is very little if any advertising of the fact that these feeds are available on the websites of institutions that provide them; this was not too surprising as many of the XCRI feeds were quite new at the start of our project, but it is something that should be improved in future - indeed, the fact that such data is made available for all sorts of useful purposes should be a relatively good demonstration of commitment to sharing useful information with the wider community.


### Aggregate the data

From the various SOAP and REST web services that we discovered, we pulled as much data as we could; during this process we found - unsurprisingly - that the REST endpoints were quite easy to access, whereas the SOAP ones were somewhat more laborious. 

In particular, the lack of a machine-readable API to the XCRI feed registry required us to do a bit of manual work before even getting to the feeds; a number of the SOAP endpoints were implemented in different ways and with different documentation, which meant it was not possible to generalise an access method across all institutes even if a machine-readable list of their endpoints were available. However, unfazed, we continued - but, it should be noted that as the number of feeds increases this process would become more laborious and something of a barrier to use.

These issues make a standardised approach to harvesting data from the services basically impossible, and therefore each service will need to be incorporated in its own custom way.  There would be a significant advantage in standardising to some degree the SOAP methods to be used. Or better still to abandon SOAP altogether and insist on a REST API. Further information about the technicalities of this is available in our project blog posts (listed at the end of this report).

After collating a list of endpoints and the required information to access them, we were able to proceed with the aggregation. We found a number of fairly standard and not unexpected errors, such as some missing URLs, some endpoints not returning data properly, but overall we were able to extract the expected data.


### Convert the data

As our proposed approach to this project included HTML5 / javascript web services / widgets calling back to a python / elasticsearch backend, we then processed the raw aggregated data into a format more suitable to our goals - an XCRI-CAP 1.2 JSON serialisation. This was achieved without difficulty although it did involve a number of steps to validate and tidy some of the raw XML and also to convert older 1.1-spec feeds to the 1.2 spec. Further technical details are available in our project blog posts, and a full expression of an XCRI JSON document is available [here](https://github.com/CottageLabs/xcri/blob/master/xcri.json), and the software which produces and utilises it [here](https://github.com/CottageLabs/xcri).

We are now using this serialisation within our demonstrator.


### Present the data

Once aggregated and converted, we made the data available via the API of our preferred backend storage layer - <a href="http://www.elasticsearch.org">elastic search</a>, and then we layered over that a web page with a javascript interface allowing for quick and easy faceted searching of the results. We were able to successfully get to the point of offering powerful searches across the aggregated data and to offer some example faceted browsing options such as limiting courses by institution. However we did find that more complex uses such as offering geographical searches or price-value comparisons was not possible with the data currently available via most XCRI feeds; it is technically well within reach, there just needs to be a bit more work done on the data being made available in the feeds, and a wee bit more standardisation on how some of that data is represented.

Further combinations of the XCRI data with information for example from the unistats KIS datasets would have been very nice, and we believe another project did succeed in doing this by getting a dump of all that data. Unfortunately for us, we had intended to rely on the unistats API which, it turns out, is broken in a number of comedic ways - and we received no response to our support requests. Regardless of our failing on this point though, it is clear that there is plenty of scope for further added value by aggregation and combination of the XCRI data feeds with datasets such as KIS.

Our demonstrator is available at <a href="http://test.cottagelabs.com/xcri">http://test.cottagelabs.com/xcri</a> and will remain there for the rest of this year. Our aggregate index will also remain available for the year, so if anyone is interested in seeing or using that, just let us know. We may even be interested in adding more records to it as more XCRI feeds become available!


<hr></hr>



## Observations

The commitment and collaboration of the community is very good, and the feeds that have been provided so far demonstrate great potential. There are a few key issues remaining, resolution of which would make the XCRI feeds good candidates for becoming invaluable infrastructure in the further and higher education environment.

* Data quality - there is occasional technically incorrect or invalid XML, although this is less of a concern. However field content appears on occasion to be copied straight from web / course descriptions, or is sometimes boilerplate / placeholder text. There are sometimes links that do not work, and regularly we found useful data defined in fields intended for human-readable content, such as an institute description or title highlighting the relevant age range but the appropriate age field being left empty.

* Some fields are on occasion misappropriated - semantics shoe-horned into more generic fields, data placed in the wrong fields, and there appears to be lack of consensus on what are the core fields - some institutes will always populate certain ones whilst other institutes focus on others. Semantics are sometimes wrapped into field content - different description fields, for example, having different purposes evidenced in the content - such as listing course aims. Some of this appears to be due to changes in how this data should be represented between XCRI 1.1 and 1.2, so there is an applicable solution in some cases.

* The spec is very flexible as to how fields can be used - for example most fields can be repeated, but for certain fields this makes it difficult to build a clear user interface, particularly in combination with the above-noted tendency for descriptions to contain semantic value - it is not obvious which field would have the most appropriate content to present to the user in different circumstances. Additionally, this flexibility results in similar information being keyed in different ways across the community - so although all valid, it cannot be guaranteed that the same sort of information will be found in the same place across multiple feeds.

* Oftentimes data that is easily discoverable on an institutional website is not available in the feed - and this is critical to the value of the feeds; if there is data an aggregator wants that is not in the feeds, it will be retrieved via other means over which the institute has no control - such as page scraping followed by potentially incorrect inference.

* The spec allows embedded XHTML, and whilst this may be useful to provide semantic meaning to the content, it more often than not appears to be solely used to simplify the task of populating fields - e.g. the course descriptions may be pulled directly from an institutional CMS. It should be noted that attempts to use embedded XHTML to control format will fail - as the layout is context dependent, the formatting will likely be stripped awat by an aggregator anyway - resulting in unnecessary complexity for everyone, for no benefit.


<hr></hr>


<h2>What we produced</h2>

<div class="row-fluid">
<div class="span6">

<p>During this project our total production output was as follows:</p>

<ul>
<li>a collection of blog posts documenting our progress (all listed on the right)</li>
<li>software capable of aggregating across multiple XCRI data feeds</li>
<li>XCRI 1.1 to 1.2 converter / validator</li>
<li>XCRI JSON serialiser</li>
<li>some code to build indexed data suitable for lucene-style queries</li>
<li>demonstrator app code showing simple frontends that query the indexing backend</li>
<li>a code repository at <a href="https://github.com/cottagelabs/xcri">https://github.com/cottagelabs/xcri</a> containing the above code under an open source license</li>
<li>the running demo at <a href="http://test.cottagelabs.com/xcri">http://test.cottagelabs.com/xcri</a></li>
<li>We also presented at the XCRI meetup in Birmingham at the start of the year</li>
</ul>

</div>

<div class="span6">
<p>Our project blog posts:</p>
<ul>
<li><a href="http://cottagelabs.com/projects/xcri/plan">XCRI project plan</a></li>
<li><a href="http://cottagelabs.com/news/seeking-xcri">Seeking XCRI</a></li>
<li><a href="http://cottagelabs.com/news/experiences-extracting-xcri">Experiences extracting XCRI</a></li>
<li><a href="http://cottagelabs.com/news/from-directory-to-course-data">From directory to course data</a></li>
<li><a href="http://cottagelabs.com/news/xcri-cap-json">XCRI-CAP JSON</a></li>
<li><a href="http://cottagelabs.com/news/xcri-xml-to-json">XCRI XML to JSON</a></li>
<li><a href="http://cottagelabs.com/news/xcri-in-the-wild">XCRI in the wild</a></li>
<li><a href="http://cottagelabs.com/news/xcri-final-report">XCRI-CAP final report</a></li></ul>
</div>
</div>


<hr></hr>


## Conclusions and recommendations

The XCRI feeds that are now in existence overall work well and mostly as intended. Insofar as our project, by building demonstrators that make use of the feeds, goes towards proving the viability and usefulness of the feeds, we can answer that yes they meet their intended purpose and provide a great way to access really useful information.

From what we have seen of the community of people involved in the programme of projects working on getting XCRI to this point, we have been impressed and have greatly enjoyed taking a small part in it. The strength of this community, and ongoing commitment to driving the further development, support and maintenance of the XCRI feeds ecosystem, is the key factor to getting XCRI embedded as a key part of the further and higher education infrastructure in years to come.

In order to achieve this, however, a number of challenges do remain; further work is required to raise the technical specification of XCRi and to bring the community and consensus to standardised usage of the specification to a peak. It is time to shift the perspective of XCRI from being one of a useful tool for exposing information available on local CMS / course databases to being the de facto standard by which course information is manipulated and shared.

Given the success of community-building and engagement so far with XCRI, we think a short period of focussing more strongly on the technical requirements of a particular use case such as consumption / aggregation of standardised course data rather than production would help to mitigate the remaining hurdles to wider uptake of XCRI feeds. To build the wider audience, all attempts should be made to provide as much high quality data as possible within the feeds themselves - this will ensure that the feeds become the go-to resource for such data, thus providing a clear point at which usage analysis can be performed, and opening a clear channel with aggregators or other consumers via which to discuss issues around presentation or application of particularly tricky elements of the underlying data, where local knowledge as to meaning can be better exposed to a general audience.

We hope to see an increasing number of feeds becoming available in the near future, along with additional development of supporting documentation such as further use case and implementation examples, and growing advertisement of the availability of these resources in the further and higher education communities.






Original Title: XCRI-CAP Project Final Report
Original Author: mark
Tags: xcri, news, mark
Created: 2013-03-30 0955
Last Modified: 2013-09-22 1644
