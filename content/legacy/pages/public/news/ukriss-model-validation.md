# UKRISS Model Validation

As part of the [UKRISS](http://ukriss.cerch.kcl.ac.uk) project investigating the feasibility of national initiatives around research information, we are prototyping tools and approaches to validating expressions of this information, to improve data quality and thus the ability for it to interoperate.

This post describes how we are going about the validation of the data through the development of a framework and process which provide us with a very flexible and powerful approach to enhancing research information.

To begin with, let's start with a diagram showing all of the parts.  This might not make sense straight away, but we'll go on to discuss each of the parts in depth.

<div class="row-fluid">
	<div class="span3"></div>
	<div class="span6">
		<img src="https://docs.google.com/drawings/d/1rT2d5hJGHvITzgX-5V9qHohwzBngPEP78AhjBtcnKSE/pub?w=777&h=849">
	</div>
</div>

## The Model Document

The project is producing XML serialisations in [CERIF](http://www.eurocris.org/Index.php?page=CERIFintroduction&t=1) of a variety of aspects of the research information space, including Research Outputs (e.g. Journal Publications), Collaborations and Partnerships, Exploitation/Spin-Outs, and Engagement Activities.  The validation framework will ingest that XML document and pass it in to a process which will extract the information from the model document...

## Extract FieldSets from Model Document

In order to actually validate the content of the model, we have to extract the information from the serialisation.  We therefore convert the XML into a list of documents we call **FieldSets**; each FieldSet is a group of information fields and their values which can be validated as a whole; for example a set of fields which make up a single bibliographic record for a journal article.  The FieldSet also annotates each field with its intended datatype and a generic name for the field that may allow it to be related to data in external data sources.

Consider the following exampe: a snippet of a CERIF XML file describing a publication, with some basic publication metadata.  This is converted into the displayed fieldset:

<div class="row-fluid">
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

## Validating Fields

For each field in the FieldSet we can carry out a validation just based on the datatype of the field and its value.  There are two kinds of validation that we can do to the field:

1. **Format Validation** - check that the field conforms to the intended schema or form.  For example, we could check that an ISSN is of the form <code>nnnn-nnnn</code>, and then we could go on to check that its [checksum digit](http://en.wikipedia.org/wiki/International_Standard_Serial_Number#Code_format) is legitimate.  This gives us a high confidence in the validity of the ISSN, but does not tell us whether the ISSN is <em>actually</em> real.  So we need to do...

2. **Reality Validation** - see if we can locate the value of the field in some remote dataset, to increase our confidence that it is genuine, and not just a good-looking fake.  For example, if we have a DOI which fits with the overall structure of a DOI (say, by applying a regular expression), we might then go and look up the DOI in the CrossRef database, or follow it to the digital object that it identifies, in order to check that it really exists in the real world!

The good thing about (2) is that we may discover further metadata about the FieldSet that we are interested in.  In our DOI example, we may discover a bibliographic record in the [CrossRef](http://crossref.org) database, or data embedded in <code>html</code> <code>meta</code> headers on the publisher's website.  In those cases we take copies of that data and bring it in to the validation environment to be used in the next stage.


## Cross-Referencing FieldSets

Once we have validated all of the individual fields, we may have retrieved from external sources a number of other records which may include interesting information about the FieldSet we are attempting to validate.  So our final stage of validation is to cross-reference every field in our FieldSet (via its generic name) with each of these external source's data to see if we can:

1. Confirm that the data in our original FieldSet is valid
2. Discover that the data in our original FieldSet differs from some other source, so may not be valid
3. Discover additional data from external sources that we don't have in our original FieldSet

This process is very complex, and requires the use of some clever algorithms such as [Levenshtein Distance](http://en.wikipedia.org/wiki/Levenshtein_distance), in order for us to make these assertions.  But if successful can take the validation of the data in the model to a whole other level - we can use this information to potentially confirm that an ISSN which we have confirmed is format valid, and is in use in the real world is **actually the ISSN which relates to the other information in the FieldSet**.

## The Result

The output of this validation process is two-fold:

Firstly, there is a large, machine-readable (in JSON) report of the validation process.  This would allow an external service (such as a CRIS, a Repository or some other metadata-bearing system) to send documents for validation and receive back machine-readable (and in some cases machine-actionable) validation information which can be acted upon automatically or presented to an end-user in a custom fasion.

Second, there is a standard HTML report produced directly from the UI of the validation service, which a human user can use to find ways to enhance the model document they have provided.

There are many further details around the software that carries out these tasks, such as: how is it structured, and how are plugins for validation written and executed, and what do the validation reports actually look like.  These points and more will be covered in upcoming blog posts ...
























Original Title: UKRISS Model Validation
Original Author: richard
Tags: ukriss, richard, news, researchinformationmanagement, python
Created: 2013-08-09 1343
Last Modified: 2013-08-09 1833
