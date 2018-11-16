<div class="row-fluid">
	<div class="span9">
		<div class="hero-unit">
			<h1>Representing ResourceSync Resources in DSpace</h1>
		</div>
	</div>
	<div class="span3">
		<img src="http://cottagelabs.com/media/resourcesync_logo.png">
	</div>
</div>

<em>As part of the [Jisc](http://www.jisc.ac.uk/)-funded work on the [ResourceSync project](http://www.openarchives.org/rs/0.6/toc), we have been carrying out an experimental implementation of the standard against [DSpace](http://www.dspace.org/) using the profile of ResourceSync we developed to meet the [OAI-PMH use case of metadata harvesting](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync).  This series of posts will describe the details of that implementation, highlighting design decisions, pointing out interesting features, and commenting on where the limitations of DSpace have been found when attempting to become ResourceSync-compliant.  This post explores how resources (metadata and bitstreams) in DSpace are represented such that they conform to the metadata harvesting use case.</em>

##Declaring the metadata harvesting profile

<div class="row-fluid">
	<div class="span6">
		<p>Our first step is to declare that the ResourceSync endpoint supports the metadata harvesting use case.  There is no standard way of declaring the "profile" of the synchronisation service, so we have to do this ad-hoc.  We take advantage of the <code>describedby</code> relationship in the Capability List document to point to a human-readable resource which describes the way that clients should understand the structure of the ResourceSync documents that they can find on the server.  In fact, that document - by default in our DSpace implementation - says some of what this post says.</p>
<pre>
&lt;urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:rs="http://www.openarchives.org/rs/terms/"&gt;

    &lt;rs:md capability="capabilitylist" modified="2013-01-02T14:00:00Z"/&gt;
    &lt;rs:ln rel="describedby" 
            href="http://mydspace.edu/dspace-resourcesync/about.txt&gt;

    ...
&lt;/urlset&gt;
</pre>
	</div>

	<div class="span6">
	<div class="alert alert-info">
<p><strong>A Note about Profiles</strong>: A profile of a standard is a way of understanding a standard-compliant service in an appropriate context.  It is important that a "profile" does not change the meaning of any of the underlying standard, as then a user who does not comprehend the profile can still work meaningfully with the standard, unaware that there is a higher-level interpretation of the information.  Therefore, the metadata harvesting profile is an enhanced way of understanding the service, but does not prevent the service being interpreted in the most simple way possible by a client (i.e. just an ordinary collection of resources).</p>
	</div>

	<div class="alert alert-success">
		<p><strong>Feedback on the ResourceSync spec</strong>: The specification does not provide us with a clear way to give machine-readable profiles to the service, but something of this nature could be valuable.</p>
	</div>
	</div>
</div>

##DSpace Item Records

A DSpace Item is the top-level container for a single logical repository entry (e.g. a journal publication, a learning resource, etc), which consists of zero or more bitstreams (files, see below) and some metadata.  DSpace Items listed in the Resource List or the Change List represent the metadata aspect of the resources held by the DSpace instance, and look something like this:

<div class="row-fluid">

<div class="span6" style="margin-right: 30px">
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

<h3>Features to note</h3>

<p><strong>loc</strong> - this URL is in the URL space of the DSpace ResourceSync webapp (dspace-rs), meaning that it is being served by a separate web application to the main DSpace UI.  Also, the URL ends with a string which tells the repository which format the metadata is in, allowing it to generate the actual resource on-the-fly. In a future post we will look in more detail at how metadata resources are actually served.</p>

<p><strong>changefreq</strong> - this is set to "never" by default because DSpace is an archiving system, and it is relatively rare for metadata records which are available to be synchronised to change.</p>

<p><strong>describedby</strong> - this is a key part of the metadata harvesting profile: it tells the client what the format of the metadata is.  The <code>describedby</code> link indicates to a content-aware client that this is the full DCMI terms by referencing the namespace of that metadata schema; a client which is aware of that format will be able to pick this out and recognise the record for what it is.</p>

<p><strong>describes</strong> - this allows the metadata record to reference the bitstreams that it describes.  In a Resource List the client can expect to find resource entries for those bitstreams.  There can be zero or more such references in a normal DSpace.</p>

<p><strong>collection</strong> - indicates the collections/sets this item appears in, by providing the default DSpace user interface's human-readable web-page URL.  In DSpace, an item will always appear in at least one collection, but may appear in several.  This effectively provides the same information as an OAI-PMH Set would provide.</p>

</div>

###Implementation Issues and Consequences

<p>As a consequence of the fact that DSpace has quite poor machine-readable provenance, there are only certain circumstances under which we can detect item deletions.  DSpace has a feature where an item can be "withdrawn" from the archive - the content is not deleted, but the item is no longer available except through a particular part of the administrator interface.  In these cases, when an item gets withdrawn we can announce a "delete" operation in the Change List.  If the item is truly deleted (totally purged from the system) there is no record of it, and so no "deleted" operation can be announced.</p>

<p>This gives rise to one further question, which is what happens if the item is "re-instated" (that is, it is moved from its withdrawn status to back in the archive)?  This can happen in the case of embargoed items or under certain other administrative/workflow conditions.  It is not clear from the ResourceSync specification whether this is a "create" or an "update" operation, but for the purposes of the DSpace implementation we have chosen to represent this as an "update".</p>


##DSpace Bitstream Records

A Bitstream is DSpace-speak for a file associated with an archived item (see above); that file may be a binary or a text file or even a licence file, but it is distinct from the item's metadata, which is held separately.  DSpace Bitstreams listed in the Resource List and Change List documents look something like this:

<div class="row-fluid">

<div class="span6" style="margin-right: 30px">
<pre>
&lt;sm:url&gt;
    &lt;sm:loc&gt;http://mydspace.edu/bitstream/123456789/7/1/bitstream.pdf&gt;
    &lt;sm:lastmod&gt;2013-05-01T19:07:45Z&lt;/sm:lastmod&gt;
    &lt;sm:changefreq&gt;never&lt;/sm:changefreq&gt;
    &lt;rs:md hash="md5:75d0ea94097a05fce9aca5b079e2f209" 
        length="419805" 
        type="application/pdf" /&gt;
    &lt;rs:ln href="http://mydspace.edu/dspace-rs/resource/123456789/7/qdc" 
        rel="describedby" /&gt;
    &lt;rs:ln href="http://mydspace.edu/dspace-rs/resource/123456789/7/mets" 
        rel="describedby" /&gt;
    &lt;rs:ln href="http://mydspace.edu/dspace-rs/resource/123456789/12/qdc" 
        rel="describedby" /&gt;
    &lt;rs:ln href="http://mydspace.edu/123456789/2" rel="collection" /&gt;
&lt;/sm:url&gt;
</pre>

</div>

<h3>Features to note</h3>

<p><strong>changefreq</strong> - this is set to "never" by default because DSpace is an archiving system, and it is very rare for bitstreams which are available to be synchronised to change.</p>

<p><strong>hash</strong> - this gives the md5 checksum of the bitstream in a hex format.  The specification allows for further hash values to be included, but DSpace only records a single hash (almost always the md5) for a bitstream.</p>

<p><strong>describedBy</strong> - indicates the metadata resources which describe this bitstream.  There are three different "describedby" links in the example: the first links to a Dublin Core (qdc) metadata record which describes the bitstream, the second links to a METS metadata record which is an alternative serialisation of the preceeding Dublin Core record, while the third is also a Dublin Core metadata record, but for a different DSpace item.  These things can happen because DSpace allows metadata to be exposed in a variety of formats and also permits bitstreams to belong to more than one item.</p>

<p><strong>collection</strong> - indicates the collections/sets this bitstream appears in, in the same way that it does for the item resource (see above).</p>

</div>

###Implementation Issues and Consequences

As noted above, DSpace has relatively poor machine-readable provenance, which makes some ResourceSync documents difficult to build with accurate information.  For example, DSpace Bitstreams do not record their last modified dates, which means we can't tell the difference between a "create" and an "update" operation.  In our implementation, therefore, all changes to bitstreams are labelled "update" in the Change List, with the assumption that the client is smart enough to realise that "create" is a kind of "update".  You will notice that although there is no last modified date in DSpace for the Bitstream, there is a <code>lastmod</code> element in the resource description above; this is because we <em>do</em> have a last modified date for the item to which the bitstream belongs, and so we provide this as a best-guess.

DSpace also does not record deletions of bitstreams; once a bitstream has gone it is gone, so any attempt to ask for a list of deleted bitstreams provides an empty result set.  DSpace does not have an event-based history mechanism from which we can gather this information.  Therefore, there are never any "delete" changes in the Change Lists - if a bitstream gets deleted it is simply never mentioned again.

Finally, DSpace can contain items with complex structure which is not reflected in the resource listings.  Each item can contain many bitstreams, and those bitstreams have sequence information and can be in "bundles" of content; some of those bundles are public, others are private, and others can be administrative.  As part of our implementation, we have therefore made the bundles which are exposed via ResourceSync a configurable option, and only the primary bundle (ORIGINAL, in DSpace terms) is available by default.  Meanwhile, sequence information is lost, and left to more sophisticated metadata exports (such as to METS) to allow an aware client to re-build an item's structure, if that is important.

##Where next?

We have now seen from the above (and from a [previous post](http://cottagelabs.com/news/generating-resourcesync-documents-in-dspace)) how DSpace's ResourceSync documents are structured and how they are generated and served to the client via a custom web application.  In the next post we will go on to look at how metadata resources are generated and served on-the-fly based on the configuration we have provided in our ResourceSync code module.  Future posts will cover the structure and deployment of the software and some of the more advanced features such as Resource Dumps and Change Dumps that we may wish to provide to enhance the client experience of the metadata harvesting use case.

[go to next installment "Serving DSpace Metadata Through ResourceSync" &gt;](http://cottagelabs.com/news/serving-dspace-metadata-through-resourcesync)



Original Title: Representing ResourceSync Resources in DSpace
Original Author: richard
Tags: richard, resourcesync, dspace, featured, news
Created: 2013-05-28 1824
Last Modified: 2013-09-22 1650
