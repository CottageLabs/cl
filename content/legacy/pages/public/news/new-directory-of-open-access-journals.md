# The New Directory of Open Access Journals


<img src="http://cottagelabs.com/media/doaj_logo.jpg" class="thumbnail span4" style="float: right; margin: 30px; margin-top: 0px; background: #ffffff">

We're pleased to be able to announce some great news for the beginning of 2014: Cottage Labs is now working with the <a href="http://doaj.org">DOAJ</a> to provide their brand new application and interface!

The DOAJ is a long-standing and key piece of the Open Access infrastructure, hosting records for around 10,000 journals and over 1.5 million bibliographic entries, making them available for discovery by researchers through the user interface, or for harvesting by aggregators and other scholarly systems via OAI-PMH.

Late in 2013 we started working with DOAJ (which is run by <a href="http://is4oa.org">IS4OA</a>) with the objective of migrating their existing data from their old service provider into a new system powered by an open source codebase.  We built the software on our favourite open source frameworks<a href="#technical_details">[]</a> and provided a javascript-driven faceted search and browse interface; we also re-created critical bits of the existing system: an OAI-PMH feed and an Atom Feed of the content.

This allowed the DOAJ to make its migration in only a very short space of time.  

We quietly went live with the new system on 19th December 2013.

There's lots in the pipeline still to come, too.  We're currently scoping out the next most critical parts of the new system, so keep your eye out for changes and enhancements over the coming months!  

Why not tell us what you think of the new DOAJ in the comments below, or let us know how you use it and what you'd like to see it do in the future?

<div class="row-fluid">
	<div class="span3">&nbsp;</div>
	<div class="span6"><a href="http://doaj.org"><img src="http://cottagelabs.com/media/doaj.png" class="thumbnail span12"></a></div>
</div>

<div class="row-fluid">
<div class="span12 well">
<a name="technical_details" href="#technical_details">[*]</a> - want to know more about the technology?  The new DOAJ is built on an <a href="http://elasticsearch.org">Elasticsearch</a> index, and the server is running a python application which utilises the <a href="http://flask.pocoo.org/">Flask</a> framework, with a load of custom written code for the DOAJ functionality (all <a href="https://github.com/DOAJ">available on github</a>).  On the front-end, we are using <a href="https://github.com/okfn/facetview/">Facetview</a> - a javascript engine for providing faceted search/browse over Elasticsearch indices.
</div>
</div>



Original Title: The New Directory of Open Access Journals
Original Author: richard
Tags: news, richard, doaj, featured
Created: 2014-01-03 1424
Last Modified: 2014-01-06 1922
