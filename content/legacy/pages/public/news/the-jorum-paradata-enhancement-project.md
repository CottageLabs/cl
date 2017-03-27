# The Jorum Paradata Enhancement Project
<br>

Cottage Labs and [Mimas](http://www.mimas.ac.uk/) have joined forces to enhance the exposure of usage statistics from the [Jorum](http://www.jorum.ac.uk) OER repository, giving users, developers and managers access to them in new and useful ways.

Jorum is a national service to UK HE and FE, for sharing open learning and teaching resources, built on [DSpace](http://www.dspace.org).  The current version is 1.5.2, but work is going on right now to upgrade to DSpace 1.8.3.  This is going to bring some significant advantages, particularly around usage statistics (a.k.a [paradata](http://en.wikipedia.org/wiki/Paradata_(learning_resource_analytics))), since this version of DSpace keeps its statistics in an [Apache Solr](http://lucene.apache.org/solr/) instance which we can therefore extract by querying its web API.

The project is focussed around two bits of work:

## The New Jorum Front-End

The new Jorum Front-End is a Ruby-on-Rails application which provides an interface to the underlying DSpace repository, but which is customised for usage by the learning community.  It uses the [DSpace REST API](https://wiki.duraspace.org/display/DSPACE/REST+API) which originally came from a [Google Summer of Code](http://code.google.com/soc/) project, and has been enhanced by Mimas to meet the needs of this new interface.

Up until now we have been getting the statistics for the DSpace items through an ad-hoc process which exports the stats from the old mechanism (pre Apache Solr), which is a bit of a hack.  The plan now is to replace this with a direct query on the Solr API and allow the user interface to display real-time statistics alongside the items themselves.

## The Jorum Dashboard

The [Jorum Dashboard](http://dashboard.jorum.ac.uk/) is a PHP application which provides a view on the current status of the paradata for the Jorum repository.  At the moment it provides some very basic statistics, but the aim is to develop some much more advanced ways of interacting with the paradata.


The project that we're embarking on is broken into two parts:

## Requirements and Deliverables

The needs of the project are still relatively unformed, so we're starting off with a period of analysing user stories and developing a set of requirements. 

The user stories include:

* As a content creator, I want to select time periods over which to aggregate stats so that I can correlate usage with particular events.

* As an e-learning manager, I want to be able to filter stats by both institution and subject area to monitor how different schools or departments in my institution are using OERs.

* As a JISC Programme Manager I want reports by Resource Type/Format to monitor and report on sector trends.

We will go through these stories and figure out what the essential requirements behind them are.  We can then prioritise those requirements for development in the second phase of the project.  Part of this work will also involve outlining the technical solutions necessary, which will allow us to efficiently enter the second phase of the project ...

## Development

The project is being run using the agile development methodology, and our developers are currently preparing to start working on the Front-End and the Dashboard so they are up-to-speed and ready to roll when the deliverables have been defined.

We know that the list of requirements is going to be much longer than what can be achieved within the time-frame of the project, though.  What this means is that we will take on the highest priority/key requirements first, and ensure that they are delivered.  Then we'll be free to develop as many of the nice-to-have features as possible in the remaining project time.


This project is due to run until September, so it's brisk, focussed and geared towards maximum impact in as short a period of time. Watch <a href="/projects/jorum-paradata">this space</a> for more updates on progress.



Original Title: Jorum Paradata Enhancement
Original Author: richard
Tags: jorum, paradata, statistics, facetview, mimas, oer, richard, news, dspace, elasticsearch, solr
Created: 2012-07-21 1058
Last Modified: 2013-05-24 1412
