<a id="An-Academic-Catalogue">&nbsp;</a>
<h1>An Academic Catalogue</h1>
An openly licensed collection of metadata about all of humanity's scholarship would be extremely useful to UK and international Higher Education. Libraries, developers and even researchers and authors would be able to find the data they need in seconds.

The UKRISS project is investigating various options for building a UK national research information infrastructure. Right now University administrators, managers, even scholars themselves need to report data to multiple funding organisations, each time sending a very similar dataset which nonetheless takes a lot of time to compile .. again and again.

In order to help UKRISS fix this situation, Cottage Labs is looking at how information from different data sources can be mingled, enhanced and validated so that it's more accurate, useful and finally, so that end-users have to type a lot less to achieve reporting requirements.

But how does one detect a misspelling in a journal name? A non-existent DOI? <a href="/people/richard">Richard</a> tells a part of the tale in <a href="http://www.cottagelabs.com/news/ukriss-model-validation">UKRISS Model Validation</a>. While he describes the <em>process</em> of validation, that process needs a lot of <strong>data</strong> - research information - to become a high-calibre time saver for multiple users.

And this is where the Academic Catalogue, an index of all scholarship, comes into play. Initially we are focussing on <strong>journal-level data</strong> only, but will most probably refine this to article-level data at some point.

<a id="Data-Sources">&nbsp;</a>
<h1>Data Sources</h1>
The word "catalogue" suggests some original source of data which has been included or described in this catalogue. We will be extracting <strong>journal titles, journal title abbreviations, ISSN-s and publisher names</strong> from:


<ul>
<li><a href="http://www.ncbi.nlm.nih.gov/books/NBK25497/#_chapter2_The_Nine_Eutilities_in_Brief_">NCBI Entrez E-Utilities</a></li>
<p>We are interested in their PubMed database, containing more than 20 million bibliographic records in the medical field. Also famous for the MEDLINE dataset, which is a subset of the whole database. (For a nice distinction between the different subsets and bits of PubMed see WHAT DATASET ARE WE TALKING ABOUT at <a href="http://openbiblio.net/2011/05/03/getting-open-bibliographic-data-from-pmc/">the related OpenBiblio project blog post</a>.)</p>
<p>PubMed contains article-level information - we will be harvesting journal-level data from that.</p>
<li><a href="http://www.doaj.org/">DOAJ</a> - Directory of Open Access Journals</li>
<p>This is a journal-level resource. It only describes a smallish subset of all academic journals (some open access ones). Nonetheless, they have kindly provided us with a data dump and are keen to share their information openly, for example through the building of a suitable lightweight API. This is very welcome in a world in which institutions try to hold on to their data as much as possible.</p>
</ul>

<p>We are looking into <a href="http://www.sherpa.ac.uk/romeo/apimanual.php">SHERPA RoMEO</a>, <a href="http://dev.mendeley.com/">Mendeley</a>, <a href="http://support.orcid.org/knowledgebase/articles/116874-orcid-api-guide">ORCID</a> and the <a href="http://datahub.io/dataset/bluk-bnb">British National Bibliography</a> for extracting more journal-level data. These links will take you to the API / Developer documentation for each of these services.</p>


<a id="Reconciling-the-different-sources">&nbsp;</a>
<h1>Reconciling the different sources</h1>
<p>We plan to ultimately provide records which look like this:</p>
<pre>
<code>
{
    "canonical_journal_title" : "Journal of Stuff", # <-- calculate these later
    "journal_title" : ["Journal of Stuff", "International Journal of Things", ...],
    "canonical_issn": "1234-5678" # <-- calculate these later
    "issn" : ["1234-5678", "9876-5432", ...],
    "canonical_publisher_name" : "Elsevier" # <- calculate these later
    "publisher_name" : ["Elsevier", "Elsevier GmbH", ...]
    "provenance" : [
        {"issn" : "1234-5678", "source" : "pubmed/12345678", "date" : "<yesterday>"},
        {"issn" : "9876-5432", "source" : "repo/item/456", ...},
        {"journal_title" : "Journal of Stuff", "source" : "pubmed/12345678", ...},
        {"journal_title" : "Journal of Stuff", "source" : "repo/item/456", ...},
        {"journal_title" : "International Journal of Stuff", "source" : "repo/item/456", ...},
        {"publisher_name" : "Elsevier" : "source" : "repo/item/456"},
        {"publisher_name" : "Elsevier GmbH", "source" : pubmed/12345678, }
    ],
    # other fields we've chosen to pick up from some data source or another
    "electronic_issn": ["1555-2101"], 
    "print_issn": [], 
}
</code>
</pre>

<p>In essence, when we collect a piece of information - say, an ISSN, from a data source like DOAJ, we add it to that journal's record, but <strong>do not change the canonical fields</strong>. We would only add a new ISSN to a journal record's <strong>list of known ISSN-s</strong>.</p>

<p>"Later", as the comments above helpfully state, we run a script over our dataset. This script trusts some data sources more than others - e.g. it may trust the DOAJ more than information from a single institutional repository. However, if multiple less-trusted sources confirm the same information, then that overrides the more-trusted source and becomes the canonical value. We have not implemented this in practice yet, but plan to run it every day, possibly several times per day.</p>

<p>We still provide the lists of <em>possible</em> ISSN-s, or possible titles, as not all applications (including within UKRISS) will need the canonical fields.</p>

<a id="More-Data-Sources">&nbsp;</a>
<h1>More Data Sources</h1>
<p>In order to  create an Open index of all scholarship, even if it's just journal  information, we need to look at a lot more data sources than we have  listed above. We don't  really know how many journals we need to have information on in order  to cover a <em>substantial</em> amount of the world's  scholarship, but a previous attempt to build this kind of catalogue left  us in the <strong>50 - 60 thousand</strong> range, so we  will reevaluate the situation once we get there.</p>

<p><strong>Please tell us about data sources which might have journal information in the comments!</strong></p>



Original Title: An Academic Catalogue
Original Author: emanuil
Tags: ukriss, emanuil
Created: 2013-08-21 0832
Last Modified: 2013-08-28 1054
