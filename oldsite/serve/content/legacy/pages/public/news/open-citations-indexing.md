<div class="row-fluid">

<div class="span9">
<div class="hero-unit">
<h1>Open Citations - Indexing PubMed Central OA data</h1>
</div>
</div>

<div class="span3">
<div class="alert alert-success">
<a target="_blank" href="http://www.elasticsearch.org">
<img src="http://www.elasticsearch.org/content/uploads/2013/02/bonsai1.png">
</a>
</div>
</div>

</div>



<div class="row-fluid">

<div class="span12">

<p>As part of our work on the <a href="/projects/opencitations">Open Citations extensions project</a>, I have recently been doing one of my favourite things - namely indexing large quantities of data then exploring it.</p>

<p>On this project we are interested in the PubMed Central Open Access subset, and more specifically, we are interested in what we can do with the citation data contained within the records that are in that subset - because, as they are open access, that citation data is public and freely available.</p>

<p>We are building a pipeline that will enable us to easily import data from the PMC OA and from other sources such as <a target="_blank" href="http://arxiv.org">arXiv</a>, so that we can do great things with it like explore it in a facetview, manage and edit it in a bibserver, visualise it, and stick it in the rather cool related-work prototype software. We are building on the earlier work of both the original Open Citations project, and of the <a href="http://openbiblio.net">Open Bibliography</a> projects, and following the <a href="http://openbiblio.net/principles">Open Bibliographic Principles</a>.</p>

</div>

</div>



<div class="row-fluid">

<div class="span6">
<h2>Work done so far</h2>
<p>We have spent a few weeks getting to understand the original project software and clarifying some of the goals the project should achieve; we have put together a design for a processing pipeline to get the data from source right through to where we need it, in the shape that we need it. In the case of facetview / bibserver work, this means getting it into a wonderful <a href="http://www.elasticsearch.org">elasticsearch</a> index.</p>

<p>While Martyn continues work on the bits and pieces for managing the pipeline as a whole and pulling data from <a target="_blank" href="http://arxiv.org">arXiv</a>, I have built an automated and threadable toolchain for unpacking data out of the compressed file format it arrives in from the <a href="ftp://ftp.ncbi.nlm.nih.gov/pub/pmc">US National Institutes of Health</a>, parsing the XML file format and converting it into <a href="http://bibjson.org">BibJSON</a>, and then bulk loading it into an elasticsearch index. This has gone quite well, as you can see on the right &raquo;&raquo;</p>

<div class="alert alert-success">
<p>To fully browse what we have so far, check out <a href="http://occ.cottagelabs.com">http://occ.cottagelabs.com</a>.</p>

<p>For the code: <a href="https://github.com/opencitations/OpenCitationsCorpus/tree/master/pipeline">https://github.com/opencitations/OpenCitationsCorpus/tree/master/pipeline</a>.</p>
</div>

<h2>The indexing process</h2>

<p>Whilst the toolchain is capable of running threaded, the server we are using only has 2 cores and I was not sure to what extent they would be utilised, so I ran the process singular. It took five hours and ten minutes to build an index of the PMC OA subset, and we now have over 500,000 records. We can full-text search them and facet browse them.</p>

<p>Some things of particular interest that I learnt - I have an article in the PMC OA! And also PMIDs are not always 8 digits long - they appear in fact to be incremental from 1.</p>

<h2>What next</h2>

<p>At the moment there is no effort made to create record objects for the citations we find within these records, however plugging that into the toolchain is relatively straightforward now.</p>

<p>The full pipeline is of course still in progress, and so this work will need a wee bit of wiring into it.</p>

<p><strong>Improve parsing</strong>. There are probably improvements to the parsing that we can make too, and so one of the next tasks will be to look at a few choice records and decide how better to parse them. The best way to get a look at the records for now is to use a browser like Firefox or Chrome and install the JSONview plugin, then go to <a href="http://occ.cottagelabs.com">occ.cottagelabs.com</a> and have a bit of a search, then click the small blue arrows at the start of a record you are interested in to see it in full JSON straight from the index. Some further analysis on a few of these records would be a great next step, and should allow for improvements to both the data we can parse and to our representation of it.</p>

<p><strong>Finish visualisations</strong>. Now that we have a good test dataset to work with, the various bits and pieces of visualisation work will be pulled together and put up on display somewhere soon. These, in addition to the search functionality already available, will enable us to answer the questions set as representative of project goals earlier in January (thanks David for those).</p>

</div>

<div class="span6">

<script type="text/javascript">
jQuery(document).ready(function () {
    var o = {
        search_url: 'http://zoo-opencitations.zoo.ox.ac.uk:9200/occ/record/_search?',
        sharesave_link: false,
        paging:{
            size: 10
        }
    };
    $('.occ').facetview(o);
});
</script>

<div class="occ">
</div>

</div>

</div>





Original Title: Open Citations Indexing
Original Author: mark
Tags: opencitations, elasticsearch, indexing, news, mark, bibjson
Created: 2013-02-12 1641
Last Modified: 2013-05-24 1412
