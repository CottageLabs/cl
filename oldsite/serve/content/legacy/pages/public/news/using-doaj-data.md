<h1>The nature of DOAJ data</h1>

<p>The <a href="http://cottagelabs.com/projects/ukriss">UKRISS project</a> has allowed us to bring an idea we've had for a long time to fruition - an openly licensed <a href="http://cottagelabs.com/news/an-academic-catalogue">Academic Catalogue</a>, currently only at journal level. One of the data sources chosen was the <a href="http://www.doaj.org/">Directory of Open Access Journals (DOAJ)</a>.</p>

<p>The main aspect of the DOAJ seems to be maintaining a list of records about more than 9900 Open Access journals. They are also very open with their data. Initially the way to access it was not obvious. They have a really good FAQ section, but it can be a bit difficult to find the first time ("About" -&gt; "FAQ"). Asking got a really prompt response  pointing out their <a href="http://doaj.org/doaj?func=loadTemplate&template=faq&uiLanguage=en#metadata">instructions for using the DOAJ metadata</a>.</p>

<p>DOAJ have both journal and article-level metadata available. Both can be accessed in great detail through the <a href="http://www.oaforum.org/tutorial/" title="Open Archives Initiative Protocol for Metadata Harvesting Tutorial">OAI-PMH protocol</a>. In addition, information about all the journals is accessible in <abbr title="Comma Separated Values">CSV</abbr> format.</p>

<p>The DOAJ only aggregates all this information, of course. However, the same is true of Thompson Reuters and the widely known (among scholars) <a href="http://wokinfo.com/">Web of Knowledge</a>, or their <a href="http://ip-science.thomsonreuters.com/mjl/">Master Journal List</a>. They do not produce any of the works involved in any manner - as authors, publishers, or otherwise, to the best of my knowledge. Yet sharing those collections of metadata openly is currently not on the menu according to the T&C-s (Note: we did not ask). Given the way publishers and Thompson Reuters view their data, we (initially &amp; briefly) expected the same of the DOAJ.</p>

<p>There is nothing inherently wrong about selling a compilation of content. The contested points are usually the nature of the content and the pricing. In this case, many would see bibliographic information as a basic need of the scholarly sector. That is to say, while it is possible to compile and sell <em>access</em> to this information, it would be preferable if it was proper, easily accessible Open Data. Organisations (<abbr title="Higher Education Institutions">HEI-s</abbr>, libraries) as well as individuals would reap greater benefits if this sort of data was collated into a good <a href="http://opendefinition.org">Open</a> collection. The <abbr title="Academic Catalogue">ACAT</abbr>'s use can be rather mundane at first, such as validation and enhancement of metadata. </p>

<p>The DOAJ are then not just another publisher of bibliographic collections, they are an excellent example of how it can be done in a sustainable manner while keeping the core data openly available. Whether the DOAJ really is financially sustainable is not relevant at this point, because they are trying to be (or have already achieved it - we have not investigated). Such attempts at open innovation in bibliographic information publishing may pave the way forward for this sector, and eventually result in services which are both open and sustainable. In a way, the DOAJ may provide much of the sustainability / business knowledge in an area where principles, technologies and interoperability has been explored by projects like <a href="http://openbiblio.net/about/">OpenBiblio</a>.</p>

<h1>Using the DOAJ data</h1>

<p>Using <abbr title="Open Archives Initiative Protocol for Metadata Harvesting">OAI-PMH</abbr> was be the first option investigated. The data is structured well and the records contain a variety of fields, in comparison to the CSV data dump which contains seemingly less information.</p>

<p>However, we only really wanted journal titles, publisher names and (<abbr title="Electronic">e</abbr>)ISSN-s, and this was present in the CSV data. Emanuil, the UKRISS project member who dealt with including the DOAJ data into ACAT, had no previous experience with OAI-PMH. Thus, we went with consuming the CSV data. Furthermore, processing XML is usually more involved than reading in a bunch of CSV columns. In this case we discovered the <a href="https://pypi.python.org/pypi/pyoai">pyoai</a> Python third-party library which seems like an excellent way of simplifying working with OAI-PMH and we will definitely try it the next time we have to use OAI-PMH.</p>

<p>All code that we produce during the UKRISS project is open-sourced under the MIT license (our preferred approach to the vast majority of our coding work). The UKRISS-related code currently spans <a href="https://github.com/CottageLabs/metatool">metatool</a> and <a href="https://github.com/CottageLabs/catflap">catflap</a> utilities, the latter including <a href="https://github.com/CottageLabs/catflap/blob/master/catflap/sources/doaj_csv.py">the script which imports the DOAJ data into ACAT</a>.</p>

<div>The script itself  is nothing very complex:
<ol>
	<li>loads the latest data from DOAJ into memory, ignoring fields which only hold a "-" or whitespace</li>
	<li>imports the data into ACAT using the small catflap tool. This ensures that incoming data is connected to previously available records. For example, if we took <pre>{"issn":"1234-5678", "publisher_name": "A Publisher Inc."}</pre> from a different data source, and then obtained <pre>{"issn":"1234-5678", "journal_title":"A Journal"}</pre> from DOAJ, we would like to "connect the dots". So now we know that A Publisher Inc. is publishing A Journal, just by virtue of the two data sources providing us with the same ISSN-s.<br>
<br>
We call fields like the ISSN identity fields, i.e. they identify a journal somewhat uniquely. Currently these are ISSN-s, print ISSN-s, electronic ISSN-s, journal titles and journal abbreviations.</li>
</ol>
</div>



Original Title: Using DOAJ Data
Original Author: emanuil
Tags: news, ukriss, emanuil, doaj
Created: 2013-10-16 2303
Last Modified: 2013-10-22 2149
