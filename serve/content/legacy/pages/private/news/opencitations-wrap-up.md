#Open Citations Wrap Up

Over the course of the Open Citations project, we have been working to develop a new and enhanced Open Citations Corpus and the technical infrastructure to support the expansion of that corpus.  This meant not just tidying up some code, but revisiting the way that the architecture works, such that it is extensible enough to support new data sources in whatever form they might take.  It also meant providing a storage and dissemination platform that would scale with an increasing number of bibliographic records and relationships between them.

This post describes the main areas of work that we undertook to complete this challenge:

* Development of a general framework for importing data sources and support for [arXiv](http://arxiv.org) and [PubMed-Central](http://www.ncbi.nlm.nih.gov/pmc/)
* Development of two visualisations to provide insights into the OCC data

The OCC software that we wrote to achieve these goals can be found at: [https://github.com/opencitations/OpenCitationsCorpus]( https://github.com/opencitations/OpenCitationsCorpus) along with installation and usage instructions.

##Import Process

We have [previously blogged](http://cottagelabs.com/news/open-citations-import-process) about our plans for the OCC import process, during the planning phase, and much of the work went as planned there.  The architecture of the approach which incorporates arXiv and PMC is:

<div class="row-fluid">
<div class="span3"></div>
<div class="span6"><img src="http://cottagelabs.com/media/opencitations_pipeline.png"></div>
</div>

The import process provides a general OAI-PMH implementation which can be used to harvest new content in an ongoing way from the data sources concerned.  Both arXiv and PMC provide OAI-PMH endpoints so they can be regularly and easily kept up to date.

Records are extracted from the OAI-PMH responses, converted into BibJSON (see Data Structure below), and stored directly into Elasticsearch (see Data Store below).

Data sources offer different ways to access their citation data, so each source has its own custom process to obtain that information.

<div class="row-fluid">
<div class="span6 well">
<h3>arXiv</h3>
arXiv makes its full-text publications available in an Amazon S3 instance (which requires the end-user to pay for the download).  These full-texts are available in LaTeX format, which means they can be mined for citation information.  The import pipeline downloads the latest publications from the S3 instance, parses the LaTeX and produces a BibJSON formatted list of citation objects.  These citations are then added to the corresponding bibliographic record already in Elasticsearch, created during the original OAI-PMH harvest.
</div>

<div class="span6 well">
<h3>PMC</h3>
The bulk load of PMC data is performed by retrieving the raw data from the <a href="http://ftp.ncbi.nlm.nih.gov/pub/pmc">NLM FTP server</a>. They are then translated to BibJSON and added to the corpus. Subsequent updating is performed by synchronising with the <a href="http://www.pubmedcentral.nih.gov/oai/oai.cgi">PMC OAI-PMH feed</a>. The synchronise operation retrieves the full text of articles in the Open Access subset, translates them to BibJSON and then either updates an existing article in the index, or creates a new one.
</div>

</div>

Periodically, then, we run a matching process across the whole OCC, which looks for bibliographic records which also appear in the reference lists of the bibliographic records and asserts links between them.  This helps us produce a corpus with relationships between bibliographic records which are both 

1. open
2. potentially in different data sources

which gives the OCC tremendous value as both a map of the open access literature and its references and an aggregation of those features across different datasets which alone could not present this information.

<div class="alert alert-success">
<strong>Technical aside</strong>: to build the OCC we transform all the data into <a href="http://bibjson.org">BibJSON</a> and store it in an <a href="http://elasticsearch.org">Elasticsearch</a> instance.  Each bibliographic record is a document containing the metadata about the item it represents and a list of references; a reference may have been matched to another bibliographic record in the OCC, in which case there will be an explicit reference to that other record - this is what makes it possible for us to build maps and graphs of the shape of open access research
</div>

##Visualisations

We have [previously blogged](http://cottagelabs.com/news/open-citations-graphing) about our prototyping work on the visualisations for the OCC.

The objective of the visualisation work has been to look at how to answer certain questions that we might want to ask of the corpus.  The questions range from the relatively simple to the relatively hard, both in terms of calculating but more imporantly in terms of presentation, such as the following sample:

<h3>Easy</h3>

<div class="row-fluid">
	<div class="span1"></div>
	<div class="span8 well" style="background: #49FC3F">How many times has our 2009 paper on graphene been cited?</div>
</div>

<div class="row-fluid">
	<div class="span1"></div>
	<div class="span8 well" style="background: #AAFC3F">Who, among the academics we fund, has published the most papers on graphene?</div>
</div>

<div class="row-fluid">
	<div class="span1"></div>
	<div class="span8 well" style="background: #F6FC3F">Show me the time-line of publication dates of papers citating our 2009 graphene paper, by month.</div>
</div>

<div class="row-fluid">
	<div class="span1"></div>
	<div class="span8 well" style="background: #FCAA3F">How many papers on graphene have been published by Oxford University academics over the past four years?</div>
</div>

<div class="row-fluid">
	<div class="span1"></div>
	<div class="span8 well" style="background: #FC3F3F">What has generated more impact, in terms of the sum of all citations to all the papers that we have funded on that topic â graphene research or fuel cell research?</div>
</div>

<h3>Hard</h3>

In order to answer these questions (and others) we have developed two kinds of visualisation: one which focusses on the strength of the relationships between papers, journals and authors, and another which looks at the timeline of citation events:

<div class="row-fluid">
	<div class="span3"></div>
	<div class="span3">
		<h3>Force-Directed Graphs</h3>
		<img src="http://cottagelabs.com/media/shotton.png">
		<a href="http://cottagelabs.com/news/open-citations-graphing">read more about the force-directed graphs</a>
	</div>
	<div class="span3">
		<h3>Timeline Representations</h3>
		<img src="http://cottagelabs.com/media/occ_timeline.jpg">
		<a href="http://cottagelabs.com/news/open-citations-timelines">read more about the timeline graphs</a>
	</div>
</div>

These graphs are built using our <a href="https://github.com/CottageLabs/graphview">Graphview</a> software - a new user interface library for building graphic views over searchable datasets.  They each provide different ways of visualising the data which allow - at least in principle - the questions above to be answered.

You also watch a [video demonstration](http://cottagelabs.com/news/open-citations-demo-video) of the software.

Here are a couple of examples as to how we might answer the questions above with this technology, then:

**How many times has our 2009 paper on graphene been cited?**
We can start by using the FacetView and searching for articles which cite our article's id; the number of times it has been cited would be the number of results from that query.  We could then go on to do the same query in the GraphView, and we would see all the papers that cite our one laid out in the chart in front of us.  From there we could switch to the timeline view, to see the rate at which those citations have actually been added, which answers yet another of our questions.

**Who, among the academics we fund, has published the most papers on graphene?**
Using the author faceting features, we would locate the authors we are interested in.  We would have to construct a complex OR query to get all of their papers out of the corpus, which would be difficult but not impossible.  We would then want to look at them in GraphView and display the papers authored by each of those users.  This would allow us to see which of those authors are the most prolific within the corpus.  We would then constrain our search results by the graphene keyword, so that only papers which mention graphene in the bibliographic metadata would be presented.

The harder questions are also answerable, but to do so requires a more sophisticated understanding of the query API the corpus provides - if you're feeling adventurous, follow the links to the above demonstrations and have a go for yourself!

##Looking Forward

Throughout this project we've developed an enhanced corpus, with an updated data model and import pipeline.  We have then demonstrated that this new model can be used to provide interesting interfaces to explore the data.

But there is much more to do.

We are currently exploring options for future funding, where we would aim to bring the corpus and the exploration tools up to a production quality.  The other clear next steps include the incorporation of more datasets into the pipeline, to expand both the number of bibliographic records in the corpus and the links between them.









Original Title: OpenCitations Wrap Up
Original Author: richard
Tags: opencitations, richard, news, python, oaipmh, universityofoxford, elasticsearch, bibjson, facetview, graphview
Created: 2013-04-18 1502
Last Modified: 2013-09-22 1641
