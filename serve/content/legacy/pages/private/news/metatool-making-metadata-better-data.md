<div class="hero-unit">
<h1>Metatool:<h1>
<h1>Making Metadata Better Data</h1>
</div>

In a [previous post](http://cottagelabs.com/news/ukriss-model-validation) we described an approach for validating coherent metadata records, which might represent bibliographic records, grant information, people, etc.

To briefly recap, in outline this works as follows:

1. Extract the information from the expression of the record
2. For each information point validate the form of the content (does it match a regex, or is a specific datatype)
3. For each information point see if there's a way to verify that the value itself is present in an external data service (such as by looking up a DOI with CrossRef)
4. Retrieve data from external data services (such as the CrossRef record for a DOI)
5. Cross-reference the external data fields with the source data fields and see if we can successfully match one to the other

What we didn't talk about in that post was how this would actually work in practice.  This is the role of metatool!  This post will go on to describe the key aspects of metatool: the Generators which extract the data from expressions (point 1), the Validators which format and reality validate fields and obtain data from remote sources (points 2 - 4) and the Comparators which allow records to be cross-referenced with external data (point 5).

## Generators: Turning source documents into FieldSets

A metadata record will be expressed in some particular serialisation.  For example, an [RDF](http://en.wikipedia.org/wiki/Resource_Description_Framework) metadata record might be expressed in [RDF/XML](http://en.wikipedia.org/wiki/RDF/XML) or [Turtle](http://en.wikipedia.org/wiki/Turtle_(syntax)), or a [Dublin Core](http://dublincore.org/documents/dcmi-terms/) record may be expressed as XML, or a bibliographic record may be expressed in [BibJSON](http://bibjson.org).  Before we can validate **the information held in the serialisation** we must know how to extract that information.  This is the function of metatool's Generators.

<div class="row-fluid">
<div class="span4">&nbsp;</div>
<div class="span4 alert alert-success">
<p>A Generator takes an expression of a metadata record and gives you back a FieldSet.</p>
</div>
</div>

A *FieldSet* is metatool's internal representation of the information in the record and its validity, and we'll see an example of it in a moment.  Consider first the example from our [previous post](http://cottagelabs.com/news/ukriss-model-validation), which shows an expression of some metadata in [CERIF XML](http://www.eurocris.org/Index.php?page=CERIF-1.6&t=1), and then a table of the information points within that XML that we are interested, annotated with their datatypes.  The code snippet below is the source of the data and the table which follows are the information points.

<div class="row-fluid" style="margin-top: 10px; margin-bottom: 10px">
<div class="span6">
<pre>
&lt;cfResPubl&gt;
        &lt;cfResPublDate&gt;2013-07-01&lt;/cfResPublDate&gt;
        &lt;cfStartPage&gt;185&lt;/cfStartPage&gt;
        &lt;cfEndPage&gt;194&lt;/cfEndPage&gt;
        &lt;cfTotalPages&gt;15&lt;/cfTotalPages&gt;
        &lt;cfURI&gt;http://eprints.rclis.org/17176/&lt;/cfURI&gt;
&lt;/cfResPubl&gt;
</pre>
</div>
<div class="span6">

<table border="1" cellspacing="0" style="width: 100%">
<thead>
<tr style="background: #aaaaff; font-weight: bold">
<td>Field</td><td>Value</td><td>datatype</td><td>generic name</td>
</tr>
</thead>
<tbody>
<tr><td>cfResPublDate</td><td>2013-07-01</td><td>date</td><td>date_published</td></tr>
<tr><td>cfStartPage</td><td>185</td><td>integer</td><td>start_page</td></tr>
<tr><td>cfEndPage</td><td>194</td><td>integer</td><td>end_page</td></tr>
<tr><td>cfTotalPages</td><td>15</td><td>integer</td><td>page_count</td></tr>
<tr><td>cfURI</td><td>http://eprints.rclis.org/17176</td><td>uri</td><td>identifier</td></tr>
</tbody>
</table>

</div>
</div>

The Generator takes the serialisation and converts it into this set of key/value pairs, the datatype expected of the value, and a generic name for the kind of content we expect in that field.  So, we expect <code>cfResPublDate</code> to contain a date (in format) but specifically to contain the <code>date_published</code> of the resource described by the metadata.

It is worth noting at this point that a Generator may generate more than one FieldSet.  A FieldSet is a **coherent** set of fields that we want to evaluate together; we are asserting that these fields are in some way critically related - this becomes important when we come to cross-reference the FieldSet with external data sources, as we will see.  An example might be as follows:

<div class="row-fluid" style="margin-top: 10px; margin-bottom: 10px">
<div class="span6">
<pre>
&lt;cfResPubl&gt;
    &lt;cfURI&gt;http://eprints.rclis.org/17176/&lt;/cfURI&gt;
    &lt;cfTitle cfLangCode="en"&gt;
		Entities and Identities in Research Information Systems
    &lt;/cfTitle&gt;
&lt;/cfResPubl&gt;
</pre>
</div>
<div class="span6">
<h3>FieldSet 1</h3>
<table border="1" cellspacing="0" style="width: 100%">
<thead>
<tr style="background: #aaaaff; font-weight: bold">
<td>Field</td><td>Value</td><td>datatype</td><td>generic name</td>
</tr>
</thead>
<tbody>
<tr><td>cfURI</td><td>http://eprints.rclis.org/17176/</td><td>uri</td><td>publication_identifier</td></tr>
<tr><td>cfTitle</td><td>Entities and Identities in Research Information Systems</td><td>title</td><td>title</td></tr>
</tbody>
</table>

<h3>FieldSet 2</h3>
<table border="1" cellspacing="0" style="width: 100%">
<thead>
<tr style="background: #aaaaff; font-weight: bold">
<td>Field</td><td>Value</td><td>datatype</td><td>generic name</td>
</tr>
</thead>
<tbody>
<tr><td>cfTitle/cfLangCode</td><td>en</td><td>iso-639-1</td><td>en</td></tr>
</tbody>
</table>

</div>
</div>

In this case we have two FieldSets that we want to evaluate - one which contains only a single field, the language, (*FieldSet 2* above) and another which contains both the title and the URI (*FieldSet 1* above).  We wouldn't want to evaulate the language of the title along with the title itself as the language that this particular title is expressed in does not relate directly to the language of the resource the metadata record is describing - such a field would be a separate language field in the metadata record.

Ultimately the Generator outputs one or more FieldSet objects which form the datastructure that metatool uses to validate the document, and they look basically like this (with example for the title field):

<div class="row-fluid">
<div class="span6">
<pre>
{
    "&lt;field name&gt;" : {
        "values" : [],
        "datatype" : "&lt;datatype of field&gt;",
        "crossref" : "&lt;generic name of field&gt;"
        "comparison": { "&lt;value&gt;" : [] },
        "additional" : { },
        "validation" : { "&lt;value&gt;" : [] }
    }
}
</pre>
</div>

<div class="span6">
<pre>
{
  "cfTitle" : {
    "values" : [
        "Entities and Identities in Research Information Systems"
    ],
    "datatype" : "title",
    "crossref" : "title"
    "comparison": { 
        "Entities and Identities in Research Information Systems" : [] 
    },
    "additional" : { },
    "validation" : {
         "Entities and Identities in Research Information Systems" : [] 
    }
  }
}
</pre>
</div>
</div>

It is a document like this that goes into the next stage of validation

## Validators: format and reality validation for fields

Once we know what the information points in the source metadata record are, then the job of a metatool validator is three-fold:

1. Check the format of the value in the field
2. Check the reality of the value in the field
3. Get any external data related to real usages of the value in the field

The validator is applied to individual fields in the FieldSet separately from eachother - we are not yet treating the FieldSet as the coherent whole that it should be, but that bit is coming.

<div class="row-fluid">
<div class="span4">&nbsp;</div>
<div class="span4 alert alert-success">
<p>A Validator takes an information point and determines its correctness on its own merit</p>
</div>
</div>

The best way to see how this works is to consider a real example, and [DOI](http://www.doi.org/)s are a good one to work through.  So, consider the DOI:

    10.1386/padm.7.2.155_1

You know and I know that this is a DOI, but why?  The obvious reason is that it looks like a DOI; it starts with **10.** and goes on to have a forward slash and some numbers and letters.  So, we know that DOIs have a format, so our validator can make a good guess as to whether a DOI is legitimate by checking its format against a [regular expression](http://en.wikipedia.org/wiki/Regular_expression).  A simple regex that will recognise a DOI is as follows:

    ^((http:\/\/){0,1}dx.doi.org/|(http:\/\/){0,1}hdl.handle.net\/|doi:|info:doi:){0,1}(?P<id>10\\..+\/.+)

If you're not familiar with regular expressions, don't worry.  You can take it as read that this will match DOIs in all their various forms.  In particular it will spot that all of the following are DOIs, which makes it flexible enough to deal with variable quality metadata:

    10.1386/padm.7.2.155_1
    http://dx.doi.org/10.1386/padm.7.2.155_1
    doi:10.1386/padm.7.2.155_1
    info:doi:10.1386/padm.7.2.155_1
    hdl.handle.net/10.1386/padm.7.2.155_1

It's also smart enough to be able to pull out the operational part of the DOI itself, which is the bit that starts with **10.**.

The next thing we need to do, then, is check that the DOI is real.  We can do that easily enough by just de-referencing it.  So we take the operational bit, and we send it to the DOI resolver, which just means requesting the following URL:

    http://dx.doi.org/10.1386/padm.7.2.155_1

If this URL returns successfully (i.e. doesn't give us a Not Found or cause an error), then we can be confident that this DOI exists in the real world.

We can then go one step further.  As it happens the DOI resolver (hosted by [CrossRef](http://crossref.org)) is also a source of bibliographic data.  When we de-reference the URL above in our web browser we most likely arrive at the publisher's home page where we can (depending on the paywall) access the artifact.  But if, instead, we ask CrossRef for a specific content type that we are interested in, we can get the metadata itself.  Specifically was ask for the format <code>application/vnd.citationstyles.csl+json</code>, which is a JSON expression of the bibliographic metadata.  So we not only verify that the DOI really exists, but we find out what data CrossRef thinks should be associated with any bibliographic record claiming to represent the referenced object.

As a result, we can extend the content of our FieldSet with both some field validation information as well as some data that we will be able to use in the next stage, like so:

<div class="row-fluid">
<div class="span12">
<pre>
{
    "cfFedId/doi" : {
        "values" : ["10.1386/padm.7.2.155_1"],
        "datatype" : "doi",
        "crossref" : "publication_identifier"
        "comparison": { "10.1386/padm.7.2.155_1" : [] },
        "additional" : { },
        "validation" : { 
            "10.1386/padm.7.2.155_1" : [<div style="color: #0000ff; font-weight: bold">
                {
                    "info" : ["DOI meets the format criteria", "doi.org successfully responded to this DOI"],
                    "warn" : [],
                    "error" : [],
                    "correction": [],
                    "alternative" : [],
                    "provenance" : "bibliographics.DOI",
                    "data" : &lt;CrossRefCSL DataWrapper&gt;
                }</div>
            ]
        }
    }
}
</pre>
</div>
</div>

Here we have some **INFO** for the human end-user saying what the validator did, some provenance, which records the plugin which carried out the validation, and very importantly the data that we retrieved from crossref (wrapped in something called CrossRefCSL DataWrapper, which we'll talk about in the next section).

Once we have done this field-level validation for every information point in the FieldSet then we can move on to the next, and trickiest, bit of the validation...

<div class="row-fluid">
<div class="span12 well">
<h3>Interlude: DataWrappers</h3>

<p>One of the challenges of using data from external data sources is working out how to compare data which might be represented in dramatically different ways.  For example, some data is in deeply nested and structured XML (e.g. <a href="http://www.ncbi.nlm.nih.gov/sites/gquery">Entrez</a>) while other data might be in simple key/value pairs, while other data might be inferred from other fields (for example, an article page count might not exist as an information point in the record, but be calculated from the difference between the start and end pages).</p>

<p>The metatool DataWrapper is a container within which the data retrieved from an external source is placed so that it has a consistent interface that it can present to the rest of the software.  When we come on to the next stage of the validation, this interface will allow metatool to ask <em>any</em> data for the values which it regards to be the <code>title</code> or the <code>abstract</code> or the <code>page_count</code>, and it will be up to the DataWrapper specific to that data source which can return an answer (or not, if it can't).</p>

</div>
</div>

## Comparators: cross-referencing source fields with external data sources

Sometimes a field in a FieldSet will lead to an external dataset which purports to describe the same resource (such as our above example of a CrossRef metadata record); examples of such fields are DOIs, Pubmed IDs, URLs to web-pages with embedded metadata, [CNRI Handles](http://www.handle.net/).  Meanwhile, other fields can lead to searches in other datasets which can return results which might also describe the resource; examples of such fields are ISSNs and ISBNs.

<div class="row-fluid">
<div class="span4">&nbsp;</div>
<div class="span4 alert alert-success">
<p>A Comparator compares the source record with an external record to determine if they agree</p>
</div>
</div>

To see how this works, let us consider the title of a publication that we want to compare with the data that we retrieved from CrossRef in the previous step.  Here is how it appears in the FieldSet at this point (we haven't done any format or reality validation on it!):

<div class="row-fluid">
<div class="span12">
<pre>
{
    "cfTitle" : {
        "values" : ["Entities and Identities in Research Information Systems"],
        "datatype" : "title",
        "crossref" : "title"
        "comparison": { "Entities and Identities in Research Information Systems" : [] },
        "additional" : { },
        "validation" : { "Entities and Identities in Research Information Systems" : [] }
    }
}
</pre>
</div>
</div>

So we know that the <code>datatype</code> of the field is <code>title</code>, and we will have a metatool validator which knows how to decide if a title looks like a title.  But here we are interested in the field that we should <code>crossref</code> the field as.  In the case of the title, the datatype and the crossref type are the same, but this isn't necessarily always the case for all field types (and in fact, will mostly not be the case); for example, a start page might be of datatype <code>integer</code>, but of crossref type <code>start_page</code>.

When we come to cross-reference this field we ask each of the DataWrappers (described above) for anything that they might identify as a <code>title</code>, then we compare the two lists of values with each other and attempt to find a successful match.  If we find one, then we record that in the "comparison" aspect of the FieldSet, which ultimately allows the end-user to see that their record is consistent with someone else's record of the same artefact.

Let us assume for the sake of argument that the title of the item in CrossRef is:

	Entities and identities in research info systems

this is not the *same* title as provided in our source record, but it is - as any human would tell you - the same title, albeit expressed slightly differently.  The comparator must be smart enough to notice this, and in fact metatool's plugin for comparing titles uses something called the [Levenshtein Distance](http://en.wikipedia.org/wiki/Levenshtein_distance) to determine the likelihood that these two titles are the same or at least similar.

This results in an enhanced FieldSet, which would look something like this:

<div class="row-fluid">
<div class="span12">
<pre>
{
    "cfTitle" : {
        "values" : ["Entities and Identities in Research Information Systems"],
        "datatype" : "title",
        "crossref" : "title"
        "comparison": { <div style="color: #0000ff; font-weight: bold">
            "Entities and Identities in Research Information Systems" : [
                {
                    "correction": ["Entities and identities in research info systems"],
                    "data_source" : "crossref",
                    "comparator" : "text.TitleComparator",
                    "success" : true,
                    "compared_with" : "Entities and identities in research info systems"
                }
            ]</div>
        },
        "additional" : { },
        "validation" : { "Entities and Identities in Research Information Systems" : [] }
    }
}
</pre>
</div>
</div>

As you can see, the <code>comparison</code> part of the field for the title shows a successful cross-reference was done against the <code>crossref</code> data source by a plugin called <code>text.TitleComparator</code>.  

It also goes a little further, though - it shows the string in CrossRef that we compared our title to; and because the title in CrossRef is different (albeit subtly) it suggested that we modify our title to be in-line withCrossRef, by placing a value in the <code>correction</code> field.

As with the Validators, we proceed through every field in the FieldSet and compare every source value with every other value from all externally discovered data sources.

## So what does it mean?

What this means is that when we respond to the end-user, we can provide a deep insight into the quality of the metadata record provided.  We can tell them whether their fields are actually formatted correctly - that number fields are actually numbers, that ISSN fields are the right shape to be ISSNs, etc.  It also means that we can determine whether those field values are likely to be real, by going out and attempting to find them in the outside world, such as resolving DOIs to their objects, or looking up ISBNs in catalogues of books.  We can then try to assert whether a metadata record is consistent; that the ISSN in the record pertains to the Journal Title that it says it pertains to, or that the author name is really associated with the journal article the record says it is.

This approach could give us incredible potential to ensure that our metadata records are both correct and consistent with the rest of the world.  It doesn't necessarily tell us what the correct metadata is, but it gives us a very useful guide that anyone working to manage metadata records can use to enhance their quality and more importantly their global consistency; ultimately this can lead to an improvement in the capacity for interoperabiltiy of metadata and integration of metadata-bearing systems.

<div class="row-fluid">
<div class="span4">&nbsp;</div>
<div class="span4 alert alert-success" style="text-align: center">
<p>LOTS OF POTENTIAL!!!!!</p>
</div>
</div>

<!--
## Things we didn't talk about

We've skimmed over a few details, as the process is very complex and hard to cover in a single post.  Here are a few points that we didn't talk about, and a couple of hints as to what they might be about:

1. There's something about the "crossref" property of a field/value which seems to indicate that there is a "global" metadata schema that we can use to extract data from any metadata record.  This is not true!  Instead metatool works with a "good enough" or "best guess" policy - plugins are free to essentially make up their metadata fields, and we hope that in general we get away with a common-sense approach to naming information points.

2. We mentioned that there are plugins for metatool.  These will be the subject of a future post.

3. We didn't really talk about "alternatives" which appear in the FieldSet data structure.  These are there to record values from external data sources which may be suitable for the metadata record owner to add to their metadata record in the future.  These are effectively values from those external data sources which we couldn't cross-reference against values in the source record.

Some of these things we'll talk about more later.  In the mean time, you can check out the code on github, and watch this space for more details.
-->



Original Title: Metatool: Making Metadata Better Data
Original Author: richard
Tags: metatool, ukriss, news, richard, metadata
Created: 2013-09-17 1759
Last Modified: 2013-09-18 1526
