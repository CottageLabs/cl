# Jorum Paradata Enhancement Project: Phase 1 Complete
<br>

We're pleased to be able to say that the Jorum Paradata Enhancement Project's first phase has completed successfully, and we have moved on to Phase 2 in recent weeks.

The Jorum Paradata Enhancement Project aims to improve the exposure and reporting facilities available to end-users of all kinds of the statistics and other paradata collected by the [Jorum Open Educational Resources (OER) system](http://www.jorum.ac.uk/ ).

## User Stories and Requirements

In the first phase we spent some weeks exploring the user stories that [Mimas](http://www.mimas.ac.uk) and the Jorum Team had already started to put together, and from them we created a set of requirements which would cover all of those stories.  You can read the full list of stories and requirements [here](https://docs.google.com/document/d/1vE_yPUHKsWgFut4UYp1-0PxeeRbo4fDC1SVVqLTVlCk/edit ), but here's a flavour of the kinds of things that we were looking at:

<div class="row-fluid">
<div class="span4">
<div class="alert alert-success">As a Repository Manager, I want all stats for my repository's OERs in Jorum</div>
<div class="alert alert-success">As a Dashboard User, I want to compare stats across N OERs</div>
<div class="alert alert-success">As a Dashboard User, I want to create a set of OERs and get any stats on that set</div>
</div>
<div class="span4">
<div class="alert alert-success">As a Content Creator, I want to access statistics about an OER from its own page</div>
<div class="alert alert-success">As a Content Seeker, I want to order search results by popularity, views, shares and downloads</div>
<div class="alert alert-success">As a Third Party Software Developer, I want to connect to an API to extract statistics to present in my local environment(s)</div>
</div>
<div class="span4">
<div class="alert alert-success">As a Dashboard/Jorum user, I want to select a time period over which stats query applies</div>
<div class="alert alert-success">As a Content Creator / User, I want to see social media shares of OERs, e.g. Twitter, Delicious, Facebook, Google+</div>
</div>
</div>

As you can see, there's quite a range of features here: 

* **a variety of end-users** such as repository managers, content creators, the general public, software developers
* **a variety of ways to constrain data**: for example by time, ordered appropriately
* **a variety of ways to look at the data**: from the perspective of a single OER or a group of OERs, or in a comparative mode for single or sets of OERs

When we analysed these user stories we generated a list of around 50 requirements, and here are some examples of those which might help us meet some of the user stories above:

<div class="row-fluid">
<div class="span4">
<div class=" alert alert-info">Jorum must register all incoming records (including manually entered ones, PMH harvested ones, and any other mechanism of ingest) with its origin (e.g. repository) and its affiliation (e.g. University of Manchester)</div>
<div class=" alert alert-info">t should be possible to constrain the statistics considered in any part of the reporting interface to which it applies by both start and end time (e.g. only consider accesses between times X and Y)</div>
</div>

<div class="span4">
<div class=" alert alert-info">It should be possible to retrieve statistics filtered by their origin and their affiliation</div>
<div class=" alert alert-info">Be able to select any number of OERs and look at the statistics side-by-side (using appropriate user interface idioms)</div>
<div class=" alert alert-info">To be able to select and create a group from a set of OERs (based on the selection mechanisms defined in these requirements) upon which stats can be generated</div>
</div>

<div class="span4">
<div class=" alert alert-info">The user interface should be able to provide a complete set of statistics for a single item as a standard view (i.e. "these are the stats and paradata for item X")</div>
<div class=" alert alert-info">Must provide API access to data, similar to existing API</div>
</div>
</div>


What you might notice is that this set of requirements isn't everything that's needed to meet the user stories that we listed above, and there is a reason for this.  Obviously the project has a finite amount of resources, and some user stories (and thus requirements) are more critical at this stage than others.  Our next part of the process was to look at both the criticality of each user story and the way in which the requirements depend on eachother, in order to prioritise the development; meeting all 50 requirements in the short time-frame of the project was never going to be possible!

<div class="row-fluid">
<div class="span1"></div>
<div class="span2"><a href="/media/jorum_access_reqs.jpg"><img src="/media/jorum_access_reqs.jpg" class="img thumbnail"></a></div>
<div class="span2"><a href="/media/jorum_facets_reqs.jpg"><img src="/media/jorum_facets_reqs.jpg" class="img thumbnail"></a></div>
<div class="span2"><a href="/media/jorum_metadata_reqs.jpg"><img src="/media/jorum_metadata_reqs.jpg" class="img thumbnail"></a></div>
<div class="span2"><a href="/media/jorum_stats_reqs.jpg"><img src="/media/jorum_stats_reqs.jpg" class="img thumbnail"></a></div>
<div class="span2"><a href="/media/jorum_ui_reqs.jpg"><img src="/media/jorum_ui_reqs.jpg" class="img thumbnail"></a></div>
</div>

So with extensive discussion with Mimas in their offices in Manchester, on a table covered with flash cards with user stories and requirements hand-written on with white-board markers, we triaged the list and settled on what we felt was the "core" of the work that needed to be done, which is defined by the requirements:

<div class="row-fluid">
<div class="span4">
<div class=" alert alert-info">Jorum must register all incoming records (including manually entered ones, PMH harvested ones, and any other mechanism of ingest) with its origin (e.g. repository) and its affiliation (e.g. University of Manchester)</div>
</div>

<div class="span4">
<div class=" alert alert-info">The user interface should be able to provide a complete set of statistics for a single item as a standard view (i.e. "these are the stats and paradata for item X")</div>
</div>

<div class="span4">
<div class=" alert alert-info">Be able to show the aggregated set of statistics for a set of OERs</div>
<div class=" alert alert-info">It should be possible to select OERs for reporting on via a standard search mechanism</div>
</div>
</div>

## Technical Design

This might seem like a modest set of requirements to meet out of the 50 or so that we defined, but in reality all the other requirements are pretty much built on the framework that these 4 require in terms of technology.

Let us first look at the current set-up of the Jorum environment, and then go on to look at the proposed technical solution.

<div class="row-fluid">
<div class="span3"></div>
<img src="https://docs.google.com/drawings/pub?id=1Zn1g7ctr8DsJZ2nj4dX-scqZRDFj1Qreb6fecy77vA0&amp;w=960&amp;h=720" class="img span6">
</div>

Jorum is based on the [DSpace](http://www/dspace.org) repository platform, and all the usage statistics are stored in the application.  The [Front-End](https://jorumbeta.mimas.ac.uk/) (a Ruby on Rails application) accesses DSpace via a version of the REST API, and uses that to provide discovery end-users with a way in to the content (DSpace's UI is not the preferred way to reach the content).  The [Dashboard](http://dashboard.jorum.ac.uk/), meanwhile, is a PHP application which presents stats end-users with some information about the usage of items in Jorum, which it does by extracting the stats from DSpace via a customised connector.

The main issues with this are the heterogeneity of the environment and the separation between the Front-End and the Dashboard; it is clear from the requirements that many features lie not cleanly within one system or the other, but somewhere in-between.  Consider, for example, a user who wants to ask the following:

<div class="row-fluid">
<div class="span3"></div>
<div class="span6 hero-unit"><strong>Show me all the statistics pertaining to the set of OERs which are published by the University of Oxford with the JACS code "F000"</strong></div>
</div>

This involves querying the bibliographic properties of the OERs (their publisher and their JACS classification) in order to access an aggregate of their statistical information (views, downloads, etc).  If you look at the two existing systems, neither one of them can answer a question such as the above (despite its apparent simplicity); the Front-End can certainly tell you about the bibliographic data, but it has no access to the statistical information via the REST API, wheras the Dashboard knows all the statistics, but isn't in posession of sufficient bibliographic information to allow the results to be constrained correctly.

Another thing that's worth noting at this point is that many of the requirements talk about viewing statistics based on a constrained result set, where the constraints can be applied in parallel with other constraints over the complete Jorum dataset.  This kind of problem is best addressed using a search index which supports faceted browsing (the main candidates being [Apache Solr](http://lucene.apache.org/solr/) and [Elasticsearch](http://www.elasticsearch.org/)), and also happens to be something we have a lot of experience in!

So we proposed an alternative system architecture which looks like this:

<div class="row-fluid">
<div class="span3"></div>
<img src="https://docs.google.com/drawings/pub?id=1D2T6nSK1sZOVDuY-u24jAzRCplULGovYcgZykvAZeJg&amp;w=960&amp;h=720" class="img span6">
</div>

At first sight this looks more complex, but it has a number of significant advantages over the existing set up.

First of all, Jorum is still based on DSpace, but Mimas are in the process of upgrading to DSpace 1.8.2 which gives us access to the Discovery and Statistics Solr indices which come as standard in that version.  Second, we have eliminated the Dashboard (the PHP application), and pushed all the functionality into the Front-End, so that we can answer the query that we talked about above.  Third, we propose a Custom Index to be based on Apache Solr or Elasticsearch which will combine data from both the Discovery and Statistics indices in DSpace.  To take advantage of the faceted browse functionality supported by these search indices, we plan to incorporate [FacetView](https://github.com/okfn/facetview) (a JavaScript application) into the Front-End.  In this way we can provide a vertical application stack which can meet all of the essential requirements, and will extend easily to meet all of the further requirements and user stories in the future.

Also, by moving to this model we can simplify the overall development of the system, and create a single environment which will allow end-users to switch between discovery and paradata use cases at will, and for use cases which lie in the grey area between them to arise.

You can read the full Technical Design [here](https://docs.google.com/document/d/18B1DYnm9opm8a2cz2OQ-mbm9N5s22uGmEu9twOrXkf4/edit ).

## Phase 2

With a set of user stories, requirements, and a technical design, we looked at the way forward for the second phase of the project: development.  The key deliverables will be:

1. New system architecture, to replace the existing system.
2. An idealised Custom Index which represents what the Jorum Metadata could be once it has gone through sufficient metadata quality enhancement.
3. Single item statistics view for each OER in the Front-End.
4. Select a set of OERs from the FacetView interface, and allow reports to be generated over the set.
5. Once a set of OERs have been selected (as per (5)) it should be possible to create an aggregated statistical view of the whole set.

The aim for Phase 2 is to have something which provides all of this by late September, so keep an eye on the Jorum service for the changes to take effect some time after then!

In the mean time, you can check out our report on the analysis of [Apache Solr and Elasticsearch to find the best options to provide the Custom Index](/projects/jorum-paradata/indexing)



Original Title: Jorum Paradata Enhancement Phase 1
Original Author: richard
Tags: jorum, paradata, statistics, facetview, news, richard, mark, martyn, jpep, featured, dspace
Created: 2012-08-26 1027
Last Modified: 2013-09-22 1651
