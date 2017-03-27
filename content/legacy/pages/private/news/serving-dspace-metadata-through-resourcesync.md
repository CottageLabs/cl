<div class="row-fluid">
	<div class="span9">
		<div class="hero-unit">
			<h1>Serving DSpace Metadata Through ResourceSync</h1>
		</div>
	</div>
	<div class="span3">
		<img src="http://cottagelabs.com/media/resourcesync_logo.png">
	</div>
</div>

<em>As part of the [Jisc](http://www.jisc.ac.uk/)-funded work on the [ResourceSync project](http://www.openarchives.org/rs/0.6/toc), we have been carrying out an experimental implementation of the standard against [DSpace](http://www.dspace.org/) using the profile of ResourceSync we developed to meet the [OAI-PMH use case of metadata harvesting](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync).  This series of posts will describe the details of that implementation, highlighting design decisions, pointing out interesting features, and commenting on where the limitations of DSpace have been found when attempting to become ResourceSync-compliant.  This post describes how DSpace items are presented as metadata resources in a variety of configurable formats.</em>

#Metadata Resources in DSpace

<div class="row-fluid">

<div class="span6">

<p>We saw in a <a href="http://cottagelabs.com/news/representing-resourcesync-resources-in-dspace">previous post</a> how DSpace's metadata resources are presented in ResourceSync.  A DSpace item represents its metadata internally as "Qualified Dublin Core" (its own expression of the <a href="http://dublincore.org/documents/dcmi-terms/">DCMI Terms</a>), and this metadata is stored in a database rather than serialised to a file.  This means that it can't be exposed via ResourceSync like a bitstream is, since there is no static file to be provided for synchronisation.  Instead Metadata Resources must be generated on-the-fly when requested (or, in a future implementation, generated in advance, although this does not affect the discussion here), which means we need to know how to convert the Qualified Dublin Core metadata in the database into a serialised format.</p>

<p>The URL at which the resource can be accessed is the <code>sm:loc</code> field in the example metadata resource listing show here.</p>
</div>

<div class="span6">
<pre>
&lt;sm:url&gt;
    &lt;sm:loc&gt;http://mydspace.edu/dspace-rs/resource/123456789/7/qdc&lt;/sm:loc&gt;
    &lt;sm:lastmod&gt;2013-05-01T19:09:35Z&lt;/sm:lastmod&gt;
    &lt;sm:changefreq&gt;never&lt;/sm:changefreq&gt;
    &lt;rs:md type="application/xml" /&gt;
    &lt;rs:ln href="http://purl.org/dc/terms/" rel="describedby" /&gt;
    &lt;rs:ln href="http://mydspace.edu/bitstream/123456789/7/1/bitstream.pdf"
        rel="describes" /&gt;
    &lt;rs:ln href="http://mydspace.edu/bitstream/123456789/7/2/image.jpg" 
        rel="describes" /&gt;
    &lt;rs:ln href="http://mydspace.edu/123456789/3" rel="collection" /&gt;
&lt;/sm:url&gt;
</pre>
</div>

</div>

The URL has the following components:

<div class="row-fluid">
	<div class="span3"></div>
	<div class="span6"><img src="https://docs.google.com/drawings/d/1vPgP3NH1DXDEZ7eePHMbgkq9A69FtjxbaZS1-6ViT-I/pub?w=894&amp;h=182"></a></div>
</div>

<strong>dspace-rs</strong> - this is the web application that provides the ResourceSync endpoint for DSpace.  DSpace is made up of a number of web applications which provide different interfaces onto the application; for example there are 2 user interfaces (named JSPUI and XMLUI), SWORDv1 and SWORDv2 webapps, and a number of others supporting other APIs or discovery interfaces.  Our implementation of ResourceSync provides a very simple webapp for serving the ResourceSync documents, and the serialisations of the metadata resources.

<strong>123456789/7</strong> - this is the <a href="http://www.handle.net/">handle</a> of the item, which is the persistent external identifier that DSpace assigns to its items.  It is used ubiquotously throughout DSpace to refer to items, and is unambiguous in any context.

<strong>qdc</strong> - an opaque string which represents the format that the metadata resource will be provided in.  In our example "qdc" stands for Qualified Dublin Core, but the client doesn't need to know this; it is a signal to the server which format to serve when this URL is requested (see below).  

The client will no doubt be interested in the format of the metadata available at this URL, and it can obtain the content type (<code>application/xml</code>) and the metadata format identifier (<code>http://purl.org/dc/terms/</code>) by looking at the rest of the resource's entry in the Resource List:

<pre>
    &lt;rs:md type="application/xml" /&gt;
    &lt;rs:ln href="http://purl.org/dc/terms/" rel="describedby" /&gt;
</pre>

From the point of view of a client aware of the metadata harvesting profile that this repository is adhering to, it can therefore identify metadata records that it can interpret by looking for <code>describedby</code> links which point to metadata formats it understands, and by looking at the content type to know how to interpret the serialisation of that format.  Meanwhile, from an unaware client, this is simply another resource which can be dereferenced and synchronised just like any other resource.

# Configuring Exposed Resources

It follows from the fact that DSpace's item metadata is stored in a canonical form in a database that we can expose a variety of formats, not just the standard QDC discussed above.  Our ResourceSync implementation allows us to configure an arbitrary number of formats, with their associated content types and format identifiers.  Our default configuration (supporting only QDC) is as follows:

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">

			<div class="span5">
<pre>
metadata.formats = \
    qdc = http://purl.org/dc/terms/

metadata.types = \
    qdc = application/xml
</pre>
			</div>

			<div class="span2">
				<p><strong>resulting in a metadata resource containing -&gt;</strong></p>
			</div>

			<div class="span5">
<pre>
&lt;sm:loc&gt;
    http://mydspace.edu/dspace-rs/resource/123456789/7/qdc
&lt;/sm:loc&gt;
&lt;rs:md type="application/xml" /&gt;
&lt;rs:ln href="http://purl.org/dc/terms/" 
    rel="describedby" /&gt;
</pre>
			</div>

		</div>
	</div>
</div>

This configuration can be extended with as many metadata formats as we like, so we could have:

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">

			<div class="span5">
<pre>
metadata.formats = \
    qdc = http://purl.org/dc/terms/, \
    mets = http://www.loc.gov/METS/

metadata.types = \
    qdc = application/xml,
    mets = application/xml
</pre>
			</div>

			<div class="span2">
				<p><strong>resulting in TWO metadata resources, one the same as the above, and the other containing -&gt;</strong></p>
			</div>

			<div class="span5">
<pre>
&lt;sm:loc&gt;
    http://mydspace.edu/dspace-rs/resource/123456789/7/mets
&lt;/sm:loc&gt;
&lt;rs:md type="application/xml" /&gt;
&lt;rs:ln href=" http://www.loc.gov/METS/" 
    rel="describedby" /&gt;
</pre>
			</div>

		</div>
	</div>
</div>

We can go on and add any other formats that we are able to support (see below for more about crosswalks).  Each format generates a new resource which appears in the Resource List (and any relevant Change Lists), which indicates that it <code>describes</code> each of the item's bitstreams, and each bitstream in that item indicates that it is <code>describedby</code> every one of the available formats.  The diagram shows all of these relationships, where each line is a <code>describedby</code>/<code>describes</code> bi-directional relationship.

<div class="row-fluid">
<div class="span3"></div>
<div class="span6"><img src="https://docs.google.com/drawings/d/1PZCw3enFWl4LgvQw_jxyJCv6JKDHpth5YwYKbFEG5gs/pub?w=682&amp;h=380"></a></div>
</div>

# Metadata Crosswalks

DSpace has a standard mechanism for exposing metadata in a variety of formats, which is extensible so that plugins for new formats can be easily added.  It uses the concept of a "named plugin" (and in particular what it calls a "self-named plugin") which allows us to ask the DSpace system for a plugin which can provide a crosswalk for a given arbitrary string identifier.  In our simple example above, the name of the plugin is "qdc", so when the client requests the metadata resource the ResourceSync web application uses that name to load a crosswalk which is then executed over the DSpace item's metadata, resulting in a document which is then served.

The standard configuration of the self named plugins in DSpace looks like this (and we haven't had to change it in any way in order to provide the ResourceSync functionality):

<pre>
plugin.selfnamed.org.dspace.content.crosswalk.DisseminationCrosswalk = \
  org.dspace.content.crosswalk.MODSDisseminationCrosswalk , \
  org.dspace.content.crosswalk.XSLTDisseminationCrosswalk, \
  org.dspace.content.crosswalk.QDCCrosswalk, \
  org.dspace.content.crosswalk.XHTMLHeadDisseminationCrosswalk
</pre>

Each of these (Java) plugins has its own configuration options which allow it to know which names it responds to.  For example, the <code>QDCCrosswalk</code> class has the following configuration, which implicitly tells it to respond to the name "qdc", and provides other technical details that it needs to know in order to make the crosswalk itself work.

So when we request the URL ending in "qdc" this results in the ResourceSync webapp asking for any plugin which can respond to the name "qdc", and the <code>QDCCrosswalk</code> plugin is loaded and executed.  It is also not accidental that this is exactly the same plugin which is loaded and executed when performing an OAI-PMH harvest from DSpace while requesting the metadata prefix <code>oai_dc</code>.

<pre>
crosswalk.qdc.namespace.qdc.dc = http://purl.org/dc/elements/1.1/
crosswalk.qdc.namespace.qdc.dcterms = http://purl.org/dc/terms/
crosswalk.qdc.schemaLocation.qdc  = \
  http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2006/01/06/dcterms.xsd \
  http://purl.org/dc/elements/1.1/ http://dublincore.org/schemas/xmls/qdc/2006/01/06/dc.xsd
crosswalk.qdc.properties.qdc = crosswalks/QDC.properties
</pre>

When executed, the <code>QDCCrosswalk</code> produces a document like this:

<pre>
&lt;dcterms:qualifieddc 
    xmlns:dcterms="http://purl.org/dc/terms/" 
    xmlns:dc="http://purl.org/dc/elements/1.1/" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://purl.org/dc/terms/ 
        http://dublincore.org/schemas/xmls/qdc/2006/01/06/dcterms.xsd 
        http://purl.org/dc/elements/1.1/ 
        http://dublincore.org/schemas/xmls/qdc/2006/01/06/dc.xsd"&gt;
    &lt;dcterms:dateAccepted&gt;2013-05-01T18:07:45Z&lt;/dcterms:dateAccepted&gt;
    &lt;dcterms:available&gt;2013-05-01T18:07:45Z&lt;/dcterms:available&gt;
    &lt;dcterms:issued&gt;2013-05-01&lt;/dcterms:issued&gt;
    &lt;dc:identifier type="dcterms:URI"&gt;http://hdl.handle.net/123456789/5&lt;/dc:identifier&gt;
    &lt;dc:title xml:lang="en"&gt;My Interesting Article&lt;/dc:title&gt;
&lt;/dcterms:qualifieddc&gt;
</pre>

# Where next?

Through this and [previous posts](http://cottagelabs.com/news/generating-resourcesync-documents-in-dspace) we have seen how both DSpace metadata and bitstream resources are represented in ResourceSync documents, how those documents are generated, and how the individual metadata resource formats are generated and served.  This fully provides, then, for the metadata harvesting use case that we [set out initially to meet](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync), and any further work that we do on a ResourceSync implementation for DSpace will be to improve its performance and give it additional nice-to-have features, rather than for improved support for that use case.  We will go on to look at Resource Dumps and Change Dumps, to see how feasible they are from the point of view of the spec and from the point of view of DSpace, and will post about those when they are ready.  In the next post, though, we'll present the software itself; how it is structured, deployed and used, etc.

<a href="http://cottagelabs.com/news/resourcesync-module-for-dspace">go to next installment "ResourceSync Module for DSpace" &gt;</a>



Original Title: Serving DSpace Metadata Through ResourceSync
Original Author: richard
Tags: resourcesync, news, dspace, richard, featured
Created: 2013-06-04 1834
Last Modified: 2013-09-22 1650
