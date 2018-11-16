<div class="row-fluid">
	<div class="span9">
		<div class="hero-unit">
			<h1>Generating ResourceSync Documents in DSpace</h1>
		</div>
	</div>
	<div class="span3">
		<img src="http://cottagelabs.com/media/resourcesync_logo.png">
	</div>
</div>

<em>As part of the [Jisc](http://www.jisc.ac.uk/)-funded work on the [ResourceSync project](http://www.openarchives.org/rs/0.6/toc), we have been carrying out an experimental implementation of the standard against [DSpace](http://www.dspace.org/) using the profile of ResourceSync we developed to meet the [OAI-PMH use case of metadata harvesting](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync).  This series of posts will describe the details of that implementation, highlighting design decisions, pointing out interesting features, and commenting on where the limitations of DSpace have been found when attempting to become ResourceSync-compliant.  This post explores the process of generating the required ResourceSync documents for DSpace, and how clients will interact with them.</em>

There are only 4 documents required in order to provide a basic metadata harvesting interface with ResourceSync (as we [prevously saw](http://cottagelabs.com/news/meeting-the-oaipmh-use-case-with-resourcesync)):

* **Capability List** - providing links to the Resource List and Change List Archive
* **Resource List** - a full list of metadata records and bitstreams in DSpace, providing the initial baseline synchronisation data
* **Change List Archive** - a list of all of the periodically-generated Change Lists
* **Change List** - a list of all metadata records and bitstreams that have changed in DSpace in the time period.

<div class="row-fluid">
<div class="span3"></div><div class="span6"><img src="https://docs.google.com/drawings/d/1qshkS_fYgenh24yN9aTIuOf4Rc7siYWPsOQbDodYdHU/pub?w=960&h=720"></div>
</div>

These documents are generated and kept up-to-date by a back-end process which can be set to run on a schedule (i.e. via cron).  All the documents are stored in the DSpace install directory as static files, and served statically so there are minimal performance implications.

The process of generating and updating these documents is as follows:

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">
			<div class="span8">
				<h2>Initialise</h2>
				<p>This creates initial Capability List and Resource List documents.  The Resource List represents the current state of the resources in DSpace, and in particular those which are in the archive and publically accessible - no access is provided by default to incomplete items or those in approval workflows.  The Capability List just points to that Resource List, and does not - at this stage - point to a Change List Archive.</p>
			</div>
			<div class="span4">
				<h3>DSpace ResourceSync directory contents</h3>
				<pre>
capabilitylist.xml
resourcelist.xml
				</pre>
			</div>
		</div>
	</div>
</div>

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">
			<div class="span8">
				<h2>Update</h2>
				<p>This creates a new Change List which covers the period since the last Change List was created (or the initial Resource List was created, if there is no previous Change List), and then adds it to the Change List Archive.  If the Change List Archive doesn't exist (because this is the first update since the initialise operation), then it is created, and added to the Capability List.</p>
			</div>
			<div class="span4">
				<h3>DSpace ResourceSync directory contents</h3>
				<pre>
capabilitylist.xml
resourcelist.xml
changelistarchive.xml
changelist_2013-05-22T17:21:39Z.xml
				</pre>
			</div>
		</div>
	</div>
</div>

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">
			<div class="span8">
				<h2>Rebase</h2>
				<p>This is effectively a combination of both <strong>Initialise</strong> and <strong>Update</strong>.  It creates a new Resource List representing the current state of the resources, replacing the previous Resource List.  It then generates a Change List which covers the period since the last Change List, and adds it to the Change List Archive (with the same rules as in the <strong>Update</strong> operation)</p>
			</div>
			<div class="span4">
				<h3>DSpace ResourceSync directory contents</h3>
				<pre>
capabilitylist.xml
resourcelist.xml
changelistarchive.xml
changelist_2013-05-22T17:21:39Z.xml
changelist_2013-05-22T17:38:37Z.xml
				</pre>
			</div>
		</div>
	</div>
</div>


The DSpace administrator is responsible for running the <strong>Initialise</strong> operation when the system is ready to provide ResourceSync capabilities.  Then a scheduled task can be set to run the <strong>Update</strong> and <strong>Rebase</strong> operations regularly.  The <strong>Update</strong> operation will always generate a new Change List (even if there have been no changes in the period), and is a relatively quick operation because it only deals with a sub-set of the total content of the archive.  The Rebase operation should therefore be run much less frequently, as it will generate a document which itemises every DSpace item and every available bitstream in those items, which could be quite a substantial document.

As a result of this approach, a consumer of the ResourceSync documents will notice that there are Change Lists which cover periods prior to the last modified date of the Resource List (of which there is only ever one).  This enables both long-term consumers of the resources to remain in sync without ever needing to read the full Resource List (except for purposes of occasional audit), and for new consumers to carry out a baseline synchronisation to a point quite close to the true current state of the service; they would need to simply consume the few Change Lists generated since the Resource List was generated.

<div class="row-fluid">
	<div class="span2"></div>
	<div class="span8">
		<img src="https://docs.google.com/drawings/d/1K8RPOo14iTUiUXkoFV3g_B5wH1AUehKBO9GSzXH3ecU/pub?w=792&amp;h=474">
	</div>
</div>

The diagram shows a representation of this process.  On the right side, there is a client which has been synchronising since the very beginning; the Resource List on which it carried out its baseline synchronisation has since gone, but it keeps up to date with ongoing synchronisation from the Change Lists, and it can audit itself on the most recent Resource List whenever it chooses.  On the left side, there is a client which only just began synchronising, so can start from the recent Resource List and ingore all previous Change Lists.

We have made a decision to generate a new Change List every time that the ResourceSync document generation process runs, rather than attempting to append to existing Change Lists.  We have done this for a couple of reasons:

1. It saves DSpace from having to read in a previous (potentially large) Change List document, append some records to it, and write it out again.  There is both a reduction in complexity, and a gain in performance.

2. It is convenient both for the client and the DSpace administrator to be able to see new Change Lists generated at regular intervals, as it is predictable and easy to verify that it is behaving as expected.

Because of this decision, sometimes those Change Lists will be empty, and for the time being it is the plan to keep the behaviour this way.  We don't believe that this causes the client any particular problems.

##Where next?

Deciding how to structure and carry out the generation of the ResourceSync documents for DSpace in order to meet the metadata harvesting use case is only the first part of the story.  We must also appropriately represent the DSpace item metadata and the associated bitstreams in both the Resource List and the Change Lists, and make it clear that these meet the requirements of the profile.  We must also make metadata resources for DSpace available in a variety of formats, which will mean generating some documents on-the-fly, since those formats may not exist except when requested.  We can also go on to develop more advanced features of ResourceSync such as Resource Dumps and Change Dumps.  We will cover all of these issues in implementation in subsequent blog posts.

<a href="http://cottagelabs.com/news/representing-resourcesync-resources-in-dspace">go to next installment "Representing ResourceSync Resources in DSpace" &gt;</a>








Original Title: Generating ResourceSync Documents in DSpace
Original Author: richard
Tags: dspace, resourcesync, news, richard
Created: 2013-05-23 1057
Last Modified: 2013-05-28 1826
