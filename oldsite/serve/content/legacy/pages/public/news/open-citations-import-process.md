#Open Citations Corpus Import Process

As part of the Open Citations project, we have been asked to review and improve the process of importing data into the Open Citations Corpus, taking the [scripts from the initial project](https://github.com/opencitations/PubMed-OA-network-analysis-scripts) as our starting point.
 
The current import procedure evolved from several disconnected processes and requires running multiple command line scripts and transforming the data into different intermediate formats. As a consequence, it is not very efficient and we will be looking to improve on the speed and reliability of the import procedure. Moreover, there are two distinct procedures depending on the source of the data ([arXiv](http://arxiv.org) or [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/)); we are hoping to unify the common parts of these procedures into a single process which can be simplified and normalised to improve code re-use and comprehensibility.

##The Workflow

As PubMed Central provides an [OAI-PMH feed](http://www.ncbi.nlm.nih.gov/pmc/tools/oai/), this could be used to retrieve article metadata, and for some articles, full text. Using this feed, rather than an FTP download (as used currently) would allow the metadata import for both arXiv and PubMed Central to follow a near-identical process, as we are already using the OAI-PMH feed for arXiv.
 
Also, rather than have intermediate databases and information stores, it would be cleaner to import from the information source straight into a datastore. The datastore could then be queried, allowing matches and linking between articles to be performed <em>in situ</em>.  The process would therefore become:
 
1. Pull new metadata from arXiv (OAI-PMH) and PubMed Central (OAI-PMH) and insert new records into the Open Citations Corpus datastore
2. Pull new full-text from arXiv and PubMed Central, extract citations, and match with article data in Open Citations server, creating links between these references and the metadata records for the cited articles. Store unmatched citations as nested records in the metadata for each article.
3. On a scheduled basis (e.g. nightly), review each existing article's unmatched citations and attempt to match these with existing bibliographic records of other articles.

In outline, this looks like this:

<img src="http://cottagelabs.com/media/opencitations_pipeline.png">

##The Datastore

[Neo4J](http://www.neo4j.org/) is currently used as the final Open Citations Corpus datastore for the arXiv data, by the [Related Work](http://www.related-work.net/) system. We propose instead to use [BibServer](http://bibserver.org/) as the final datastore, for its flexibility and scalability, and suitability for the Open Citations use cases.

##The Data Structure

The data stored within BibServer as [BibJSON](http://bibjson.org) will be a collection of linked bibliographic records describing articles. Associated with each record and stored as nested data will be a list of matched citations (i.e. those for which the Open Citations Corpus has a bibliographic record), a list of unmatched citations, and a list of authors.
 
Authors will **not** be stored as separate entities. De-coupling and de-duplicating authors and articles could form the basis of a future project, perhaps using proprietary identifiers (such as ORCHID, PubMed Author ID or arXiv Author ID) or email addresses, but this will not be considered further in this work package.

##Overall Aim

The overall aim of this work is to provide a consistent, simple and re-usable import pipeline for data for the Open Citations Corpus.  In the fullness of time we'd expect it to be possible to add new data sources with minimal additional complexity.  By using an approach whereby data is imported into the datastore at as early a stage as possible in the import pipeline, we can use common tools for extracting, matching, deduplicating citations; the work for each datasource, then, is just to convert the source data format into [BibJSON](http://bibjson.org) and store it in BibServer.



Original Title: OpenCitations Import Process
Original Author: richard
Tags: opencitations, news, richard, martyn, elasticsearch, bibjson
Created: 2013-02-18 1952
Last Modified: 2013-05-24 1412
