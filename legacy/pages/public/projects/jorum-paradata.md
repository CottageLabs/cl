# The Jorum Paradata Enhancement Project
<br>

<div class="row-fluid">
<div class="span8">
<strong>Project Partner(s)</strong>: <a href="http://www.mimas.ac.uk/">Mimas</a><br>
<strong>Cottage Labs Lead</strong>: <a href="/author/richard">Richard</a><br>
<strong>Cottage Labs Involved</strong>: <a href="/author/mark">Mark</a>, Martyn<br>
<strong>Timeline</strong>: July - September 2012
</div>
<div class="span4">
<img src="http://cottagelabs.com/media/jorumlogo.jpeg" class="img thumbnail span6 pull-right">
</div>
</div>

<br>

**Project Summary**

Cottage Labs and [Mimas](http://www.mimas.ac.uk/) have joined forces to enhance the exposure of usage statistics from the [Jorum](http://www.jorum.ac.uk) OER repository, giving users, developers and managers access to them in new and useful ways.

Jorum is a national service to UK HE and FE, for sharing open learning and teaching resources, built on [DSpace](http://www.dspace.org).  The current version is 1.5.2, but work is going on right now to upgrade to DSpace 1.8.3.  This is going to bring some significant advantages, particularly around usage statistics (a.k.a [paradata](http://en.wikipedia.org/wiki/Paradata_(learning_resource_analytics))), since this version of DSpace keeps its statistics in an [Apache Solr](http://lucene.apache.org/solr/) instance which we can therefore extract by querying its web API.

We are working on two interfaces to Jorum:

<ol>
<li>The Jorum Front-End - a Ruby-on-Rails application which provides a user interface to DSpace</li>
<li><a href="http://dashboard.jorum.ac.uk/">The Jorum Dashboard</a> - a PHP application which provides paradata statistics for DSpace</li>
</ol>

<br>
We'll be integrating both of these with the Solr statistics in DSpace 1.8.3, to enhance the user experience all round!

**Project Resources**

<ul>
<li><a href="/news/the-jorum-paradata-enhancement-project">Our introductory blog post</a></li>
<li><a href="http://dashboard.jorum.ac.uk/">The Jorum Dashboard</a></li>
</ul>

<div class="facetview facetview-stories facetview-descending" data-size="20" data-search='tags:jorum AND  url:"/news/*"'></div> 



Original Title: Jorum Paradata
Original Author: richard
Tags: complete, project, jorumparadata, jorum, mimas, universityofmanchester, elasticsearch, dspace, solr, facetview, ruby, richard, mark, martyn, emanuil
Created: 2012-07-18 2124
Last Modified: 2014-05-15 1053
