<div class="row-fluid">
	<div class="span9">
		<div class="hero-unit">
			<h1>ResourceSync Module for DSpace</h1>
		</div>
	</div>
	<div class="span3">
		<img src="http://cottagelabs.com/media/resourcesync_logo.png">
	</div>
</div>

<em>As part of the [Jisc](http://www.jisc.ac.uk/)-funded work on the [ResourceSync project](http://www.openarchives.org/rs/0.6/toc), we have been carrying out an experimental implementation of the standard against [DSpace](http://www.dspace.org/) using the profile of ResourceSync we developed to meet the [OAI-PMH use case of metadata harvesting](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync).  This series of posts will describe the details of that implementation, highlighting design decisions, pointing out interesting features, and commenting on where the limitations of DSpace have been found when attempting to become ResourceSync-compliant.  This post describes the software that we have written and its dependencies, installation and configuration.</em>

The software that we have produced as part of this proof-of-concept project is in two distinct parts: [a common java library](https://github.com/CottageLabs/ResourceSyncJava) for handling the ResourceSync document types, and a [DSpace implementation of the standard](https://github.com/CottageLabs/DSpaceResourceSync), employing the common java library.

At this stage of the work, these two code libraries are not complete ResourceSync implementations, but provide support only for the parts of the specification required to enable the [metadata harvesting use case](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync).

<div class="row-fluid">

<div class="span6 well">
<h2>Common Library</h2>
<p>Provides the following concrete classes for ResourceSync documents</p>
<ul>
	<li><p>Capability List</p></li>
	<li><p>Change List</p></li>
	<li><p>Change List Archive</p></li>
	<li><p>Resource List</p></li>
</ul>

<p>Also provides a generic ResourceSync document implementation (from which all the above extend), making the library quick and easy to apply to new areas of the specification.</p>

</div>

<div class="span6 well">
<h2>DSpace Implementation</h2>
<p>Can generate the following ResourceSync documents</p>
<ul>
	<li><p>Capability List</p></li>
	<li><p>Change List</p></li>
	<li><p>Change List Archive</p></li>
	<li><p>Resource List</p></li>
</ul>

<p>It also provides the following features for DSpace:</p>
<ul>
	<li><p>A command line client for managing ResourceSync documents</p></li>
	<li><p>A web application which can serve ResourceSync documents</p></li>
	<li><p>The ability to expose a variety of metadata formats for each DSpace item</p></li>
</ul>

</div>

</div>

# Configuration

We're now into the details of how the implementation actually works in DSpace.  If you are familiar with DSpace, this next section will make perfect sense to you.  If not, it will give you an idea of the kinds of configuration that we might offer the repositories who are offering ResourceSync on their DSpace.  We'll omit the boring config options (about file paths, and such) - if you're really interested [check out the config file](https://github.com/CottageLabs/DSpaceResourceSync/blob/master/dspace/config/modules/resourcesync.cfg) - and focus on those options which modify the behaviour of the server.

## Choosing files to expose

<div class="row-fluid">
<div class="span6">
<p>DSpace holds its content as a collection of Items, each of which can contain metadata and files.  Each Item contains a collection of "Bundles", and each bundle contains the actual files that belong to the item.  Each Bundle can have a different purpose; for example there is always a bundle called ORIGINAL which holds the main content files for the Item, and a LICENSE bundle which contains any licensing information.  But the owner of the repository is free to have whatever bundles they wish in the item, and to partition the file content between them as desired.  Other common bundles include ADMIN, SWORD, and METADATA.</p>

<p>Furthermore, items in DSpace can be in a variety of states with regard to access privileges.  They may be withdrawn from the archive, or simply have access policies which forbit unauthenticated access. </p>

<p>In order to allow the administrator to control access to the restricted items and to only the bundles of files that are to be made available, we provide to config options <code>expose-bundles</code> and <code>changelist.include-restricted</code>
</div>

<div class="span6">
<pre>
# List of bundles to expose via ResourceSync, comma separated list
#
expose-bundles = ORIGINAL

# Include restricted access items in change notifications?
#
changelist.include-restricted = false
</pre>
</div>
</div>

## Exposing Metadata

<div class="row-fluid">
<div class="span6">
<p>DSpace does not store metadata in files, it stores it in a database in its own internal formulation of the DCMI Terms (called Qualified Dublin Core).  This means that for us to server metadata resources we need to generate them on-the-fly, and we can use one of a variety of dissemination crosswalks that DSpace supports.  We describe this in more detail in a <a href="http://cottagelabs.com/news/serving-dspace-metadata-through-resourcesync">previous blog post</a>.</p>
</div>

<div class="span6">
<pre>
# List of metadata formats that we can expose, comma separated list of URIs
#
metadata.formats = \
    qdc = http://purl.org/dc/terms/

# Map of metadata formats (from the metadata.formats option) to the
# mimetypes of those formats.
#
metadata.types = \
    qdc = application/xml
</pre>
</div>
</div>

## Change Frequencies

<div class="row-fluid">

<div class="span6">
<p>The ResourceSync specification allows us to indicate to the client how frequently a resource on the server is likely to change.   Defined values that are permitted are <code>always</code>, <code>hourly</code>, <code>daily</code>, <code>weekly</code>, <code>monthly</code>, <code>yearly</code>, and <code>never</code>.  But how should a server know how frequenctly its content changes?  DSpace is an archive, so it is likely that its content changes relatively infrequently, and perhaps even never, but it will depend on exactly the kind of usage the repository is being put to.  To that end, we make metadata and bitstream change frequencies configurable system-wide, and leave it to the administrator to define the value for the repository in-situ.</p>
</div>

<div class="span6">
<pre>
# Indicative change frequency of metadata records in this repository. 
#
metadata.change-freq = never

# Indicative change frequency of bitstream records in this repository.
#
bitstream.change-freq = never
</pre>
</div>
</div>


# Installation and Usage

We won't go into the details of the installation in this post.  If you want to download and install the software, you can read all about it in the [README](https://github.com/CottageLabs/DSpaceResourceSync/blob/master/README.md) file.

You can generate the documents (as described in a [previous post](http://cottagelabs.com/news/generating-resourcesync-documents-in-dspace)), from the DSpace command line, like this:

Initialise the ResourceSync documents:

<pre>
[dspace]/bin/dsrun org.dspace.resourcesync.ResourceSyncGenerator -i
</pre>

Generate new Change Lists:

<pre>
[dspace]/bin/dsrun org.dspace.resourcesync.ResourceSyncGenerator -u
</pre>

Generate new Change Lists and regenerate the Resource List

<pre>
[dspace]/bin/dsrun org.dspace.resourcesync.ResourceSyncGenerator -r
</pre>

Once you have deployed the code and generated the documents, you'll be able to visit your ResourceSync endpoint at a URL like:

<pre>
http://mydspace.edu/dspace-rs/capabilitylist.xml
</pre>

# Where next?

This post concludes the main theme of the proof-of-concept work to implement ResourceSync generically for the DSpace repository platform.  We have outlined the [Metadata Harvesting use case](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync) that formed the basis of the work.  We have seen how to [generate the documents](http://cottagelabs.com/news/generating-resourcesync-documents-in-dspace) for clients to interact with, [how those documents are structured](http://cottagelabs.com/news/representing-resourcesync-resources-in-dspace), and [how metadata resources are made available](http://cottagelabs.com/news/serving-dspace-metadata-through-resourcesync).  We plan to go on and implement support for Resource Dumps and Change Dumps in the near future, and will blog about the challenges and details of their implementation.












Original Title: ResourceSync module for DSpace
Original Author: richard
Tags: resourcesync, dspace, richard, news, featured
Created: 2013-06-05 1127
Last Modified: 2013-09-22 1650
