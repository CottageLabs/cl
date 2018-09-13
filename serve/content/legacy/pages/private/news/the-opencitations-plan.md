#The OpenCitations Plan
<br>

This project is actually a second phase of an original OpenCitations project funded by Jisc back in 2010, with the stated aim to *"promote citation datasets as first class information objects"* [[1](http://opencitations.wordpress.com/2010/07/15/jisc-open-citations-aims-objectives-and-final-outputs/)].  As part of this project a large dataset of citation information was gathered and made available from the [PMC Open Access Subset](http://opencitations.wordpress.com/2011/07/01/input-data-for-open-citations-the-pmc-open-access-subset/), which became known as the Open Citations Corpus (OCC).  The data was marked up as RDF and housed in a large triplestore which was then exposed through the [OpenCitations.net website](http://opencitations.net/explore-the-data/).

At the end of the final blog post from that first phase of the project, the project team stated:

>*While this is the formal Final Blog Post for the JISC-funded Open Citations Project, that was funded for a year from 1st July 2010, our work is not yet finished. We cherish grand ideas for the liberation of the reference lists from all scholarly journal articles, using the Open Citations Corpus as an exemplar, in collaboration with publishers and organizations such as CrossRef who handle such citation data on behalf of publishers on a daily basis.* [[2](http://opencitations.wordpress.com/2011/07/01/jisc-open-citations-project-%E2%80%93-final-project-blog-post/)]

And now, in phase 2 we have an opportunity to work further towards that vision.  Cottage Labs became involved in the project through its regular contacts with the University of Oxford, and prior work with the OpenCitations lead Dr David Shotton (such as [DataFlow](http://cottagelabs.com/projects/dataflow), the [DataStage extension to DataFlow](http://cottagelabs.com/projects/datastage)), and [Oxford DMPOnline](http://cottagelabs.com/projects/oxforddmponline).

Working with colleagues at the University of Oxford, we devised a plan to quickly and effectively move the OpenCitations project forward in some essential ways.  We want to achieve the following objectives within the project:

* Improve the data processing pipeline so that the OCC can be kept up to date continuously
* Incorporate more data sources into the OCC, and in particular [arXiv](http://arxiv.org/) and [CrossRef](http://crossref.org/) data
* Enhance the OCC data software, to make it easier to store and explore
* Provide enhanced user tools and visualisations over the data
* Provide an API which is more accessible to developers than the exisitng SPARQL endpoint (i.e. a REST API)

The rest of this post describes the approach and technologies that we are planning to use to achieve this goals ...

##Divide and Conquer

The project divides neatly into two parts, so we divide the project team at Cottage Labs into two parts to carry out a two-pronged attack on the problem:

###1. Back-End: data processing pipeline and storage
Led by [Ben O'Steen](/people/ben) and working with [Martyn](/people/martyn), they will take the [code written in the first phase of the project](https://github.com/opencitations), streamline it and generalise it so that it can incorporate other data sources (and in particular arXiv and CrossRef).  The result will be a pipeline which can be connect to a data source and which can ultimately produce [BibJSON](http://www.bibjson.org/) for storage in the OCC.  The decision has also been taken to employ [Elasticsearch](http://www.elasticsearch.org/) and [BibServer](https://github.com/okfn/bibserver) as the storage layer for the OCC; the use of BibServer in particular is valuable as this is in-line with other Jisc-funded endeavours such as [OpenBiblio](http://cottagelabs.com/projects/open-biblio)/[OpenBiblio 2](http://cottagelabs.com/projects/open-biblio-2), and therefore gives us many essential bibliographic handling features "for free", as well as a REST API and an easy data source from which to build good user interface tools and visualisations.

As part of this process, we will be working with the developers of the Related Work service (see below).

###2. Front-End: user interface and visualisations
Led by [Mark](/people/mark) and working with Daleep (a Cottage Labs Associate), they will start from the BibJSON specification (as will be produced by the Back-End) and develop interesting and useful user tools and visualisations on the data.  This will involve first working to ensure that the BibServer software and index are appropriate for the form of the BibJSON used by the OCC.  They will then carry out some analysis of the data, and in collaboration with the project team produce a plan for useful views or visualisations on the data.  The remainder of their work will then be in developing those visualisations for the benefit of the OpenCitations project, but also for the benefit of all users of BibServer.

[Richard](/people/richard) is the Cottage Labs Lead on the project, and is dealing with coordinating the two teams, as well as liaising with Oxford and external data providers (in particular CrossRef), and making sure that the whole thing hangs together by the end of this phase of work. 

##Related Work

[Related Work](http://blog.related-work.net) was developed by Mathematicians Hienrich Hartmann and Rene Pickhardt based on the arXiv dataset.  It has remarkable similarities to the OpenCitations project, and since both David Shotton and Heinrich Hartmann were based at the University of Oxford, it was easy for us to see that a tie-up between the two projects would be beneficial to both parties.

The key benefit that we can make is by combining Related Work's understand of arXiv and OpenCitation's understanding of the PMC OASS we can quickly produce a dataset incorporating both data sources.  Heinrich and Rene are therefore collaborating with Ben and Martyn on the Back-End development, combining our data processing approaches into one more generic approach, and combining our data formats into BibJSON.

Related Work also already has its own user interface, and we have decided that OpenCitations will develop its own user interface separately to this.  Although this may sound counter-intuitive, it is actually beneficial in a number of ways:

1. By developing separate user interfaces we can prove that the Back-End that we develop is sufficiently generic and de-coupled that it can be re-used in context which we had previously not considered (e.g. a 3rd party user interface, or integrated into a 3rd party service)
2. We can explore different user interface idioms for presenting the data in parallel, over the short timescale of this phase of the project, increasing the likelihood of producing valuable outputs.

##CrossRef

CrossRef is an excellent source of bibliographic and citations data, and [CrossRef Labs](http://labs.crossref.org/) has a number of useful services.  Using the DOI lookup we are able to obtain a record for a given record which may include its citation data (if CrossrRef receive it from the publisher).  We have already - at this early stage of the project - been to visit CrossRef in Oxford, received valuable insights into their data, and encouraged them to provide a BibJSON export format, which will make the data acquisition pipeline very short for getting data from them.

##So, In Summary

There were a number of ways that this phase of the OpenCitations work could have gone (such as deep-dives on erroneous reference corrections, or detailed integrations with a variety of 3rd party services), and what we have chosen to push ahead with in this short phase is that which delivers the most benefit in the shortest time:

<div class="row-fluid">
<div class="span6"><div class="hero-unit"><h3>More data in the OpenCitations Corpus</h3></div></div>
<div class="span6"><div class="hero-unit"><h3>Better ways of accessing and understanding that data</h3></div></div>
</div>

We've got an experienced team all set up and going on the project, with a clean distinction between the parts of the work, and with a Cottage Labs Founding Partner overseeing the work.  By early 2013 we expect to be producing something that can be seen by the outside world, and we'll keep you posted on this blog as to the developments.








Original Title: The OpenCitations Plan
Original Author: richard
Tags: opencitations, news, richard, elasticsearch, bibserver, facetview, graphview
Created: 2012-12-29 1212
Last Modified: 2013-09-22 1646
