#Seeking XCRI

<br>

As part of our [XCRI demonstrator project](http://cottagelabs.com/projects/xcri) we wanted to do some preliminary work to understand how widely used XCRI data is and how easy it is to find.  We'd then use the results of that background research to seed our demonstrator index to show the value of aggregating these feeds.  This post details part of that background research: our attempts to locate usable XCRI data just using basic internet searching and intuition.

##Approach

We wanted to approach this from the perspective of someone who wants to aggregate or automatically acquire course information, but who might not strictly know about XCRI.  So: a technical user, who's comfortable exploring a relatively technical side of the web to find the information they are looking for.  We're not imagining that (potential) students looking for courses would know or care about XCRI.

From this perspective, then, we performed internet searches on the following types of terms:

<div class="row-fluid">

<div class="span4">
<div class="alert alert-success">
<h3><i class="icon-search"></i>&nbsp;xcri</h3>
<p>assuming knowledge of the XCRI standard, and hoping to go directly to XCRI formatted resources or pages about such resources</p>
</div>
</div>

<div class="span4">
<div class="alert alert-success">
<h3><i class="icon-search"></i>&nbsp;course information</h3>
<p>assuming no knowledge of course information APIs or exchange formats</p>
</div>
</div>

<div class="span4">
<div class="alert alert-success">
<h3><i class="icon-search"></i>&nbsp;university course information</h3>
<p>being specific because "course information" turns out to be far too wide a term; this, unfortunately, limits us to finding information only from universities, and thus misses many potential suppliers of xcri data</p>
</div>
</div>

</div>
<div class="row-fluid">
<div class="span2"></div>

<div class="span4">
<div class="alert alert-success">
<h3><i class="icon-search"></i>&nbsp;course information xcri</h3>
<p>assuming again knoweldge of the XCRI standard, but being specific that we're looking for pages detailing course information, in the hope of eliminating pages about the XCRI specifciation</p>
</div>
</div>

<div class="span4">
<div class="alert alert-success">
<h3><i class="icon-search"></i>&nbsp;course information api</h3>
<p>not assuming any knowledge of the XCRI standard, looking for generic course information APIs</p>
</div>
</div>

</div>

Following on from any search results we used a "follow your nose" approach with the objective of locating XCRI formatted resources/APIs for inclusion into our demonstrator.  The rest of this post details the resources we found during this process, and some commentary on the state of XCRI available on the open web today.

##Resources

###Resources about XCRI

<div class="row-fluid">
<div class="span9">
<p>It was relatively easy to find resources about XCRI as a standard, in particular <a href="http://www.xcri.co.uk">the XCRI Knowledge Base</a>, which links out to <a href="http://www.xcri.org/forum/">the XCRI forum</a> and <a href="http://www.xcri.org/wiki/index.php/XCRI_Wiki">the XCRI wiki</a>.  Their principle focus is to support the community of XCRI implementers, and therefore seemed like a good place to discovery links to endpoints.</p></div>
<div class="span2"><a href="http://cottagelabs.com/media/xcri-knowledge-base.png"><img src="http://cottagelabs.com/media/xcri-knowledge-base.png" class="img thumbnail"></a></div>
</div>

###Lists of XCRI endpiints

<div class="row-fluid">
<div class="span9">
<p>Starting from <a href="http://www.xcri.co.uk">the XCRI Knowledge Base</a>, we can rapidly find two lists of XCRI endpoints:</p>

<ol>
<li><a href="http://xxp.igsl.co.uk/app/xcridirectory">The XCRI directory</a> - this contains 66 documented endpoints, both REST and SOAP.  Some of them were clearly marked as not working, and we could verify that that was the case.  It wasn't possible to verify any of the SOAP services directly through a web browser, though many of them appeared to be responding to basic HTTP requests.</li>

<li><a href="http://www.xcri.org/wiki/index.php/XCRI_Feeds">The XCRI wiki page</a>- this contained a sub-set of the resources listed in <a href="http://xxp.igsl.co.uk/app/xcridirectory">the XCRI directory</a>, again with some of them clearly not responding.</li>
</ol>
</div>
<div class="span2"><a href="http://cottagelabs.com/media/xcri-directory.png"><img src="http://cottagelabs.com/media/xcri-directory.png" class="img thumbnail"></a></div>
</div>

###Discovery endpoint

<div class="row-fluid">

<div class="span9">
<p>The <a href="http://www.xcri.co.uk">the XCRI Knowledge Base</a> includes an <a href="http://coursedata.k-int.com/discover/">aggregator of its own</a>, which provides access to around 1500 course data resources, built on an <a href="http://www.elasticsearch.org/">ElasticSearch</a> index and providing a very basic faceted browse and search interface.</p>
</div>
<div class="span2"><a href="http://cottagelabs.com/media/xcri-discovery.png"><img src="http://cottagelabs.com/media/xcri-discovery.png" class="img thumbnail"></a></div>
</div>

###University pages

The [the XCRI Knowledge Base](http://www.xcri.co.uk) provides [5 case studies](http://www.xcri.co.uk/h2-what-case-studies.html) of institutions implementing XCRI feeds for their course data.  We investigated each of their websites to see if we could locate their endpoints:

* [University of Bradford](http://www.bradford.ac.uk/external/) - we found some blog posts, but were unable to locate a feed
* [University of Bolton](http://www.bolton.ac.uk/) - we found a project page, but were unable to locate a feed
* [Leeds Trinity](http://www.leedstrinity.ac.uk/) - we found a project page, but were unable to locate a feed
* [New College Nottingham](http://www.ncn.ac.uk) - no information found about XCRI
* [Open University](www.open.ac.uk/) - we found a paper about XCRI, but were unable to locate a feed

We investigated these first, because we felt that they would have the highest chance of yielding a feed that we could discover, so were relatively disappointed with the results.  In particular, using the [The XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory) we knew that the Open University has a SOAP endpoint, as documented here: [http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1056](http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1056).

Beyond these 5 case studies, then, we looked at the course information pages for a number of universities, largely at random, as they came up in our internet searches.  They all provide pretty good interfaces for discovering courses, but precisely none provided any links to APIs (XCRI or otherwise) for that data.  We also looked at [UCAS](http://www.ucas.ac.uk/) and found the same situation.

##Conclusions

What we've probably shown here is that XCRI is too new for there to be mature and/or widespread implementations across the educational sector.

Of the resources that we located, [the XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory) is probably the most useful, although it is still relatively few implementations (66 in total), some of which appear to have been prototypes which are no longer running.  We would need to do a more detailed exploration of each of the entries in that directory (which, itself, does not appear to provide an API) to determine what the amount of usable data actually is, but we could probably estimate 30 - 40 usable endpoints, provided that the large number of SOAP interfaces lead to valid data.

That, in fact, is the most disappointing thing about the implementations that we discovered - the prevelance of SOAP.  In a world where web APIs are dominated by REST, it was surprising for us to encounter so many SOAP APIs.  An unfortunate side effect of this is that unlike a REST API we can't simply point a web browser at the endpoint and determine the quality of the data - we will need to implement a thin SOAP client, undestand the WSDL, and make the correct procedure call in order to validate the XCRI data therein.

##Next Steps

In order to build our demonstrator for JISC we will need to aggregate some XCRI data sources.  The tasks we'll need to do before that, then are:

1. Compare what we discovered in our internet research with the information provided directly by JISC to seed this project, and see where the overlap is
2. Implement a thin SOAP client and attempt to consume the data from the endpoints in [the XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory)
3. Examine all of the resources listed in [the XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory) (both REST and SOAP) and determine which can be used for our demonstrator

We'll then be in a position to move on to the next phase of the project, which is to implement an aggregator and faceted browser of our own, and attempt to build value on the aggregated dataset.



Original Title: Seeking XCRI
Original Author: richard
Tags: xcri, richard, news
Created: 2012-11-11 1615
Last Modified: 2013-03-02 1859
