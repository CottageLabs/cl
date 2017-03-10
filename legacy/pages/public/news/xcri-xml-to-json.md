#XCRI XML to JSON
<br>

This post describes the process of taking the mixed variety of XCRI XML formats that we can get from the services listed in the [XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory) and converting it to JSON.  The source data is in one of two XCRI versions (1.1 or 1.2), and with variable data quality and formatting issues.  We want to put everything into a consistent data structure that we can build our course data demonstrator over, and weed out erroneous data.

In a [previous post](http://cottagelabs.com/news/xcri-cap-json) we introduced a JSON serialisation of XCRI-CAP that we plan to use to build the dataset for our demonstrator.  We have then written some [software](https://github.com/CottageLabs/xcri) which can take the XML we harvest from the various sources, validate it, upgrade it to version 1.2 and convert it to JSON.

<br>

<div class="row-fluid">
<div class="span4">
<img src="https://docs.google.com/drawings/pub?id=1KSQUHTjU4XQg5i268l0KkK4cyrry85PMQz2VuSP-xYE&w=495&h=1036" class="img"/>
</div>

<div class="span8">
<p>We begin with a directory of XML files that we have harvested from the various services/endpoints (you can find out more about this process by looking at <a href="http://cottagelabs.com/news/extracting-xcri">this previous post</a>) which is a mixture of 1.1 and 1.2 compliant XCRI and may or may not contain technical errors.</p>

<p>We pass this directory of files to a script which carries out two important tasks: it verifies that the XML is valid and correctly structured, and then applies a conversion from XCRI 1.1 to 1.2 if necessary.</p>

<p>Validation takes the form of a simple parse of the XML, which itself picks up many errors, such as incorrectly encoded special characters, or the presence of invalid XML.  We then verify that the XML's root element is the "catalog" element from the <a href="http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2">XCRI specification</a>, which is sufficient to verify that the XML is actually XCRI (it doesn't tell us that the XCRI is schema valid, but it does tell us that we can probably extract some data from it, which is all we really want)</p>

<p>Conversion from XCRI 1.1 to 1.2 takes place dependent on the namespace of the XML document.  XCRI 1.1. uses <code>http://xcri.org/profiles/catalog</code>, while XCRI 1.2 uses <code>http://xcri.org/profiles/1.2/catalog</code>, so they are easy to tell apart (there is no <code>version</code> element in the XCRI schema itself).  The actual conversion apples an XSLT to the XML, which is helpfully <a href="http://www.xcri.co.uk/h2-info-models/149-mapping-11-to-12.html">provided by the XCRI knowledge base</a>.</p>

<p>By the end of this first script, then, we have a directory full of XCRI 1.2 compliant XML files, and a short report on which of the files failed to pass our minimal validation (on our initial work on the 50 feeds that we have harvested, 3 of them do not pass validation)</p>

<p>There is then a second script which we can execute which converts the XCRI 1.2 XML into <a href="http://cottagelabs.com/news/xcri-cap-json">our own JSON format</a>.  It does this by first applying a straightforward and generic mapping from XML to a Python dictionary using an excellent open source <a href="https://github.com/martinblech/xmltodict">3rd party utility</a>.  We then go on to apply a large number of rules which allow us to do two important things:</p>

<ol>
<li>apply a standard structure to the data, so that - for example - all properties which the XCRI specification says can be multiple are represented as lists (even if those lists are empty or have only one value)</li>
<li>make corrections for common errors and idioms that we see in the data</li>
</ol>

<p>When we complete this cleanup work, we can just serialise the Python data structure out as JSON using standard language tools, and we are left with a set of JSON files which are consistently formatted, and therefore useful for our indexing process and for being part of an aggregation over which we can build new tools are services</p>

<p>
</div>

</div>

##Invoking the code

The software is located [here](https://github.com/CottageLabs/xcri) and developers will find extensive documentation there for executing the scripts.  A brief summary of how the above process can be executed, though, is:

    python upgrade.py -d [original xml files directory] -o [1.2 xml files output directory]

This validates all the XML and ensures that it is in XCRI 1.2 format

    python xcrixml2json.py -d [1.2 xml files output directory] -o [json output directory]

This converts all the XML to JSON and ensures that it is consistently formatted



Original Title: XCRI XML to JSON
Original Author: richard
Tags: xcri, json, xml, news, richard
Created: 2013-01-02 1612
Last Modified: 2013-03-02 1924
