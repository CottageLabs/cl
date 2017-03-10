<div class="row-fluid">
	<div class="span9">
		<div class="hero-unit">
			<h1>Meeting the OAI-PMH use case with ResourceSync</h1>
		</div>
	</div>
	<div class="span3">
		<img src="http://cottagelabs.com/media/resourcesync_logo.png">
	</div>
</div>

[OAI-PMH](http://www.openarchives.org/pmh/) has been in wide use since around 2001.  Its take-up within the repository community has been nearly total.  It is clear, therefore, that it scratches a particular itch, fits a particular niche, satisfies an essential use case.

And what is that use case, exactly?  It is quite complex, as it happens, and goes something like this:

<div class="alert alert-success" style="color: #000000">
"I want to be able to retrieve a list of metadata records from a service - in a format that I understand - so that I can take copies of them (possibly for the purposes of building an aggregation).  I want to be able to ask the service for the metadata records periodically and only get those which are new or which have changed since I last asked.  I don't just want to see new records, I also want to see updated records and know when records have been deleted, so that I can keep in step.  I also want to be able to harvest only certain partitions on the service, so that I don't have to wade through everything to find the particular areas that I'm interested in copying."
</div>

So what we have, arising from this use case, are a set of features which are essential to OAI-PMH's success and to the servers and clients which utilise it, and they are:

<hr>
<div class="row-fluid">
	<div class="span6">
<p><strong>1. Identification of metadata records within a service</strong> - a service may provide all kinds of content and not all of it will be metadata.  OAI-PMH picks out just those resources which are metadata and makes them available.</p>

<p><strong>2. Use of standards in metadata formats</strong> - if clients and servers are going to exchange information in a meaningful way, they need not only to understand the protocol but also the content.  The OAI-PMH solution to this is to provide metadata prefixes which the server supports and which the client can choose from, with Dublin Core being the essential lowest-common denominator</p>

<p><strong>3. Incremental updates</strong> - Being able to request only records which were added or changed during a particular time period dramatically reduces the load on a client (and the server, hopefully).  This is very consistent, as well, with how protocols like RSS deal with providing latest updates to blogs without providing the full archives each time a user requests an update.</p>
	</div>

	<div class="span6">
<p><strong>4. Create, Update, Delete</strong> - For a client to remain in sync with a source it will be looking for not just creates, but also updates and deletes.  OAI-PMH provides mechanisms to consistently identify records, and to indicate whether a delete has taken place, so a client can easily tell by looking at their local register of identifiers whether this is a new record or one they have seen before, and if a delete notification is presented know that they should delete their copy of the record.</p>

<p><strong>5. Sets</strong> - For services which have a large amount of content, clients may only want to consume changes from certain areas; for example from the arXiv you may only be interested in the "astro-ph" feed.  This concept has many analogies in computing systems, like directories on a desktop or collections in a repository.</p>
	</div>
</div>
<hr>

But there are limitations to OAI-PMH too.

It has been argued that OAI-PMH has caused excessive use of Dublin Core for interchange metadata - effectively eliminating rich metadata from harvesting services.  This compounds another issue which is that metadata records in DC-based OAI-PMH feeds do not contain clear references to any content files (e.g. article full-texts) which are related to or described by the metadata record.

Additionally, OAI-PMH has an interface or API style which now appears quite dated.  It is heavily reliant on URL query parameters which indicate a "verb" or action to take, which is a style common a decade ago.  With the rise of RESTful web services, and the way that they fit neatly into the web architecture, there is a strong desire to see the way that clients interact with servers for harvesting updated.

*Any pretender to the OAI-PMH crown, therefore, must meet that use case and must provide equivalent implementations of those features, or new features which allow the clients to achieve much the same effect.  It must also have something to say about the limitations of OAI-PMH.*

#Enter ResourceSync

We have [previously blogged](http://cottagelabs.com/news/resourcesync) about ResourceSync itself, and there are lots of resources you could look at, such as the [current verison of the spec](http://www.openarchives.org/rs/0.5/resourcesync), the [prototype software in development](https://github.com/resync) or the [mailing list](https://groups.google.com/forum/#!forum/resourcesync), so we won't go into too much detail about the background here.

ResourceSync is a protocol also under development by the Open Archives Initiative (the OAI bit of OAI-PMH), which looked to solve the more general problem of synchronising content between client and server environments.  It does not limit itself to consideration of only metadata records, and it does not provide a thick API over the top of the content; it is intended as a modern, RESTful, part of the web architecture.  Instead of having one essential (if complex) use case like OAI-PMH, there are many use cases which drive the ResourceSync development, and these include (but are not limited to, by a long shot):

<div class="row-fluid">
<div class="span3"><img src="https://lh3.googleusercontent.com/tj7gXh8jN0_Dy9KOPck-Du-JbB3p4q8rNz979M8cm22JxWKj7RKNZvpAhYAzgagbLaReGzMIAEn61c6PC1u4hVHtXDLczwjnTGQX_gM3nAn0fwOMmywp"><p>Full synchronisation of resources beetween two systems</p></div>
<div class="span3"><img src="https://lh5.googleusercontent.com/LKP5kBapb2d3E61s2je8L6_rfmiRO4WnVUQKerpLgLxaSUX-qV-X9AlzOVu_mLasyW5-xlJs-WorW5KwUyONzfktPzEJWZmQAhE1hrNlXjox9vTfDMsw"><p>Smart cacheing locally of remote resources</p></div>
<div class="span3"><img src="https://lh6.googleusercontent.com/kijxReaBIUs8KynyotRXyZBOsTrXmWAcufzFfclaKOhAG6RW0zewqVbAWWPSPypiUf-TQf7DDPDcdGma88zj-OWK8xCS84yiA5GZ2unU2qU_RnUCIm6B"><p>Synchronisation of metadata resources between two systems</p></div>
<div class="span3"><img src="https://lh4.googleusercontent.com/-sUj_rOE4piF-lNejSIWx8-1t4Oo_WWzH9zIQek2Hc1VuJ8RTS6KVPk_JTIHyeRbLNta7ds-fw4ppDV1o9LoutKLYubJFm_Wb0hq2tWn12RQ2QoASY2F"><p>Selective filtering of resources for synchronisation</p></div>
</div>

Now, it might occur to you that the last two points there actually fit into the functional scope of OAI-PMH, which is entirely deliberate.  ResourceSync has been developed very much as a successor to OAI-PMH, so we have taken care to see that the OAI-PMH use case is supported in some way.  Nonetheless, the ResourceSync approach to that use case is not very similar to OAI-PMH, as we will see.  The remainder of this post serves to describe how ResourceSync meets those essential features above, and how we could go ahead and implement a replacement for OAI-PMH using the new standard.

Consider ResourceSync's responses to the features provided by OAI-PMH:

<hr>
<div class="row-fluid">
	<div class="span6">
<p><strong>1. Identification of metadata records within a service</strong> - As ResourceSync does not specifically care about metadata records, only resources, then it is up to the server to identify which of those resources are metadata.  This can be done by annotating a resource's entry with an appropriate piece of administrative metadata indicating that it is a metadata resource.  Furthermore, because ResourceSync allows the exposure of all resources, both content and metadata, the resource's entry can also point to related files, meaning that a client can harvest not just the metadata record but also all the content; a feature which has long been missing from OAI-PMH and which has long been needed.</p>

<p><strong>2. Use of standards in metadata formats</strong> - as we discussed in the previous point, ResourceSync does not care about metadata records, and therefore it does not care about the formats of those metadata records.  Again, we are free to annotate a resource's entry with appropriate metadata to indicate the format. In fact, as we shall see further down, we can take a combined approach to identifying metadata records and metadata formats.</p>
	</div>

	<div class="span6">
<p><strong>3. Incremental updates</strong> - this is one of the key features of ResourceSync, but instead of offering a time-boxed query feature for the client to use, ResourceSync publishes changes as static documents (or nearly static, at least).  The client is then free to walk up and down the change lists provided by the server. </p>

<p><strong>4. Create, Update, Delete</strong> - this is also a key feature of ResourceSync.  All resources that can be obtained from a change list will be annotated with the kind of change that happened to them, providing exactly equivalent functionality to OAI-PMH.</p>

<p><strong>5. Sets</strong> - ResourceSync does not implement Sets in the way that you would understand them from OAI-PMH.  Instead ResourceSync allows the server to publish lists of resources and changes and indexes of those lists  all annotated - optionally - with metadata.  So to provide an equivalent experience for the OAI-PMH client, we're going to need to introduce some special metadata into the ResourceSync documents to allow clients to select the appropriate lists.  There are several ways you might do this, and below we will present the most straightforward of these approaches, even though it is the most dissimilar to OAI-PMH.</p>
	</div>
</div>
<hr>

In terms of easing some of the limitations of OAI-PMH, we can also provide the following responses:

* **Over-reliance on Dublin Core** - ResourceSync does not care about Dublin Core.  It will be interesting to see whether implementations of ResourceSync do rely on Dublin Core as one of their primary means of transporting metadata.  It is our feeling that Dublin Core is a widely used transmission standard *because* it is the lowest-common denominator, and that it's widespread use is at least partially independent of it being a minimum requirement in OAI-PMH.  In fact, it being a minimum requirement in OAI-PMH is likely a result of it being the most useful transmission standard.

* **Lack of links to related content files** - ResourceSync explicitly solves this problem

* **Not RESTful** - ResourceSync is fully restful, uses pre-existing standards where possible, and fits very well into the web architecture

# The Details

Ok, so that's quite a high-level look at how we might be able to meet the OAI-PMH use case, and certainly we can feel confident that it is a contender for replacing OAI-PMH and bringing with it those extra benefits above.  So let's look into the details.

Here are the ResourceSync documents that we need in order to fully implement the OAI-PMH use case (note that ResourceSync has many other document types, and they could all be used in appropriate ways in an OAI-PMH replacement, but they are not strictly *necessary*):

<div class="row-fluid">
<div class="span3"></div><div class="span6"><img src="https://docs.google.com/drawings/d/1qshkS_fYgenh24yN9aTIuOf4Rc7siYWPsOQbDodYdHU/pub?w=960&h=720"></div>
</div>

The **Capability Lists** just points us to our **Resource List** (where we'll do our initial full synchronisation from), and a **Change List Archive** (where we will look later for our **Change Lists** to keep up to date).

<div class="row-fluid">

	<div class="span6">
<p>The <strong>Capability List</strong> is pretty straightforward, and looks something like this (showing us the URLs for the <strong>Resource List</strong> and the <strong>Change List Archive</strong>):</p>

<pre>
&lt;urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:rs="http://www.openarchives.org/rs/terms/"&gt;

    &lt;rs:md capability="capabilitylist" modified="2013-01-02T14:00:00Z"/&gt;

    &lt;url&gt;
        &lt;loc&gt;http://example.com/resourcelist.xml &lt;/loc&gt;
        &lt;rs:md capability="resourcelist"/&gt;
    &lt;/url>
    &lt;url>
        &lt;loc>http://example.com/changelistarchive.xml &lt;/loc&gt;
        &lt;rs:md capability="changelist"/&gt;
    &lt;/url&gt;
&lt;/urlset&gt;
</pre>
	</div>

	<div class="span6">

<p>The <strong>Change List Archive</strong> is similarly vanilla (showing us the URLs for a couple of <strong>Change Lists</strong>, in ascending order):</p>

<pre>
&lt;sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
              xmlns:rs="http://www.openarchives.org/rs/terms/"&gt;

    &lt;rs:ln rel="resourcesync" href="http://example.com/capabilitylist.xml"/&gt;
    &lt;rs:md capability="changelist" modified="2013-01-03T09:00:00Z"/&gt;

    &lt;sitemap>
        &lt;loc>http://example.com/changelist1.xml&lt;/loc&gt;
        &lt;lastmod>2013-01-01T09:00:00Z&lt;/lastmod&gt;
    &lt;/sitemap&gt;
  
    &lt;sitemap&gt;
        &lt;loc>http://example.com/changelist2.xml&lt;/loc&gt;
        &lt;lastmod>2013-01-07T09:00:00Z&lt;/lastmod&gt;
    &lt;/sitemap&gt;

&lt;/sitemapindex&gt;
</pre>
	</div>

</div>

<div class="row-fluid">

<div class="span6">
<pre>
&lt;urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:rs="http://www.openarchives.org/rs/terms/"&gt;

    &lt;rs:ln rel="resourcesync" href="http://example.com/capabilitylist.xml"/&gt;
    &lt;rs:md capability="resourcelist" modified="2013-01-03T09:00:00Z"/&gt;

    &lt;url>
        &lt;loc&gt;http://example.com/metadata-resource&lt;/loc&gt;
        &lt;lastmod&gt;2013-01-02T17:00:00Z&lt;/lastmod&gt;
        &lt;rs:ln rel="describes" href="http://example.com/bitstream1"/&gt;
        &lt;rs:ln rel="describedBy" href="http://purl.org/dc/terms/"/&gt;
        &lt;rs:ln rel="collection" href="http://example.com/collection1"/&gt;
        &lt;rs:md hash="md5:1584abdf8ebdc9802ac0c6a7402c03b6"
             length="8876"
             type="application/xml"/&gt;
    &lt;/url&gt;

    &lt;url>
        &lt;loc&gt;http://example.com/bitstream1&lt;/loc&gt;
        &lt;lastmod&gt;2013-01-02T17:00:00Z&lt;/lastmod&gt;
        &lt;rs:ln rel="describedBy" href="http://example.com/metadata-resource"/&gt;
        &lt;rs:ln rel="describedBy" href="http://example.com/other-metadata"/&gt;
        &lt;rs:ln rel="collection" href="http://example.com/collection1"/&gt;
        &lt;rs:md hash="md5:1e0d5cb8ef6ba40c99b14c0237be735e"
             length="14599"
             type="application/pdf"/&gt;
    &lt;/url&gt;
&lt;/urlset&gt;
</pre>
</div>

<div class="span6">
<p>Things get interesting when we get to the <strong>Resource List</strong>. </p>

<p>Here we have added lots of new metadata to the <code>url</code> elements that describe the resources.  Let us consider each one separately:</p>

<p><strong>The metadata resource: http://example.com/metadata-resource</strong> - we can see that this metadata resource <code>describes</code> a bitstream, thus linking those two resources together.  It is also <code>describedBy</code> the namespace of the extended Dublic Core metadata schema (<a href="http://dublincore.org/documents/dcmi-terms/">DCMI Terms</a>), indicating to the client that this is both a metadata resource and the format of that resource.  It also asserts a <code>collection</code> which tells us, effectively, which Set the resource belongs to.</p>

<p><strong>The content resource: http://example.com/bitstream1</strong> - we can see the reciprocal link to the metadata here in the <code>describedBy</code> link, and we can also see that the bitstream might be described by more than one metadata recoard (for example, in different formats).  It also asserts that it is a member of the same <code>collection</code>.</p>

<p>Exactly the same features, then, are present in the <strong>Change List</strong> - which is omitted here, since it looks almost identical to the <strong>Resource List</strong>.

<p>The use of the metadata namespace to annotate the resource has a number of benefits: it is very specific about the format of the metadata; it serves to indicate that the record is a metadata resource; additionally, any client that does not understand the metadata format will just regard this record as <em>yet-another-resource</em>, and may choose to synchronise it or not depending on its mission, without necessarily treating it as metadata.</p>

<p>A key difference to the OAI-PMH implementation is that the client is required to trawl through the full list of items in the service and only synchronise those which is interested in.  Therefore, to obtain metadata resources in DC format from a specific collection, the client would look for any <code>url</code> described by <code>http://purl.org/dc/terms/</code>, with the collection's URL in the <code>collection</code> link.  This does push the onus of filtering the content onto the client, which is a reasonable trade-off, as it means the client can apply any number of complex rules to determine the resources to synchronise, at no extra cost to the server.</p>

</div>
</div>

# Conclusion

What we have done here is take a very bottom-up approach to presenting information about metadata formats and sets.  We could have taken a top-down approach and had a <strong>Resource List</strong> and <strong>Change List Archive</strong> for every metadata format and for every Set, but this makes creating and navigating the index documents much more complex.  The approach we present here is not only the easiest for the server to generate, it is also the neatest, and most consistent with the intent of the ResourceSync protocol.  

As part of the [Jisc](http://www.jisc.ac.uk/)-funded portion of the ResourceSync project, we are currently engaged in developing a demonstrator using this approach, based on [DSpace](http://www.dspace.org/).  If successful - which we are confident it will be - we hope that this will set a precedent for the best way to represent metadata harvesting using ResourceSync.  It may be that there is a need for additional ResourceSync documentation which provides profiles of the standard for use in certain contexts, and that the work here will form the basis for the OAI-PMH profile.












Original Title: Meeting The OAI-PMH Use Case with ResourceSync
Original Author: richard
Tags: richard, resourcesync, news, dspace
Created: 2013-04-26 0941
Last Modified: 2013-09-22 1650
