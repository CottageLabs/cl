<div class="row-fluid">
<div class="span12">
<div class="hero-unit">
<h1>G4HE - what it means to be correct</h1>
</div>
</div>
</div>

In the G4HE project we are taking data from the GtR API and presenting it in ways that should be beneficial to people in the research and higher education community. Our requirements gathering exercise identified the use cases that people wanted, and the first one to be worked on is the 
collaborations report.

We began our software development using old data from GtR as we are not currently concerned with data quality but with building functionality. However, last week we updated our data to match the latest available from GtR, and via some feedback from the community we made some interesting discoveries about what it means for data to be correct.

<h2>An example problem</h2>

For example, feedback from the Medical Research Council raised concerns that our beta G4HE user interface showed collaborations between organisations that had no such collaborations, or included organisations that did not actually 
exist. Despite not focusing on data quality for the moment, we found this odd because we have yet to do any work that would cause our processing of GtR data to have any effect on the entities present in it, or their relations to one another. So we did some further investigation.


<h2>What we found</h2>

As far as we can tell our data is accurate. We have the most 
recent information from GtR and we do not appear to have corrupted it in any 
way during our processing of it.

However, what we have of course done is augment the data to fit our requirements, and displayed it via our UI with our particular use cases in mind, and this is what appears to have led to the apparent data inconsistency. But here is where 
it gets interesting - we do not think this is an inconsistency.


<h2>Our analysis of GtR</h2>

The MRC pointed out to the GtR team that our G4HE UI shows a collaboration 
between MRC and the Paul Scherrer Institute, but the MRC state that they have no 
such collaboration. The project that shows this collaboration is titled <strong>GPCR Signalling: Rhodopsin and beta-adrenergic receptor structure</strong>, and by viewing it on the GtR website rather than our own, we can check that the data GtR hold about it is what MRC expect. MRC did this too, and were happy GtR shows the correct information. Here is the link: <a href="http://gtr.rcuk.ac.uk/project/E09CECE0-26E8-4F5C-96AE-F41F4A009C2A">http://gtr.rcuk.ac.uk/project/E09CECE0-26E8-4F5C-96AE-F41F4A009C2A</a>.

So MRC believe they hold the correct data about this project, and they believe GtR holds the correct data about this project. If we are also correct that our G4HE work has not corrupted the data, what has gone wrong?

If we look further at the data in GtR, we can find the list of people involved in the project. It lists the Principal Investigator as Gebhard Franz Schertler and the GtR website conveniently lists information about him on another page, here: <a href="http://gtr.rcuk.ac.uk/person/1F9B0EB9-CEEC-4F67-83CF-CFB00F90EF31">http://gtr.rcuk.ac.uk/person/1F9B0EB9-CEEC-4F67-83CF-CFB00F90EF31</a>. It turns out that he works for Paul Scherrer Institute.

So, using only the GtR website, it would seem sensible to assume that MRC <strong>do</strong> have a collaboration with Paul Scherrer Institute, even though MRC do not believe so, and despite the fact that MRC believe they hold correct data about the project and also believe that GtR hold that same correct data. So the analysis must continue.


<h2>Our analysis of G4HE</h2>

When we started our dev work, one of our first concerns was the definition of collaboration. What we agreed, between the people and organisations so far involved in the G4HE project, was that collaboration would mean the following:

<div class="well">
a collaborator is any organisation affiliated with a PI or CI (co-investigator), and any organisation with the role "Lead Research Organisation" or "Fellow"
</div>

So, of course, by the agreed definition Paul Scherrer Institute is a collaborator of MRC even if MRC are unaware of it.

Perhaps then, given that our aim in the G4HE project is to make the GtR data more useful to people in the research and higher education community, we have achieved exactly that &mdash; we have taken data provided by multiple institutions and used it to identify collaborations that were previously unknown. This would be quite a success for our project.

However, it is still possible that GtR holds the correct data that MRC provided whilst holding incorrect data about Gebhard Franz Schertler &mdash; and as we have not corrupted the data in the G4HE project, we may be emulating an error there.


<h2>What are affiliations in GtR?</h2>

We believe that GtR affiliations - e.g. that Gebhard Franz Schertler is at Paul Scherrer Institute - are current affiliations. So Gebhard Franz Schertler may not have been there at the time he was involved with the MRC project.

If this is the case, then MRC would be correct that we are once again displaying wrong collaboration data &mdash; but in this case, it would not be because our definition of collaborator is wrong but because GtR makes affiliation assertions that cannot be known to be correct at the time a given collaboration took place.


<h2>The proposed solutions</h2>

It seems that our definition of collaboration still stands, and would still show useful information to people in the target community, and has the potential to surface collaborations they were otherwise unaware of. It would also probably be useful to know that someone historically involved in a project has now moved on to a different place of work, and so has a different affiliation &mdash; there is the potential for new collaborations there.

But if we cannot know the temporal relevance of the affiliation information in GtR, we cannot be certain we are displaying this correctly in G4HE.

This is not necessarily a failing of GtR, however &mdash; individual institutions such as MRC may be holding data that was correct at the time a project took place but has since become stale, leading them for example to be unaware of the current affiliations of their PI.

So we must either:

* augment our definition of collaboration so as not to include affiliations of people involved in projects, and hence lose a great deal of the potential to learn more from the data (the very thing our project aims to do)

* get GtR to provide temporal information about the affiliations of people

* find an alternative method of identifying the affiliations of people at the time a project took place <strong>and</strong> at the current time.


We would like to know what people think about these options. Please get back to us via the comments below or through our mailing lists. More information and our current demonstrator are available at <a href="http://g4he.cottagelabs.com">http://g4he.cottagelabs.com</a>.



Original Title: G4HE - what counts as correct?
Original Author: mark
Tags: g4he, mark, news
Created: 2013-07-25 1108
Last Modified: 2013-09-05 1202
