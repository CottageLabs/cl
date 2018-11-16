<div class="hero-unit">

<h1>G4HE so far</h1>

</div>


The G4HE project has progressed well to date, and we hit the original project deadline this month. However the project has been extended to March, presenting the opportunity to develop further.

We started last week to consider what we should do with the extra time available, and - of course - we were not sure what to do; we had no plan to continue beyond this point. So instead of charging on with no idea, we are taking some time to review. Here is what we have done so far.


<h2>Get the data</h2>

In the early stages of the project, the aim was just to use the GtR API successfully and get as much data out as we could. We had done some early experiments with this that went quite well, and progress was good. We were able to quickly extract all data via the GtR API in short order. Once we had it, we did some work indexing it into a suitable format for our use cases, the reports that we expected to deliver.

At this point we also sorted out some test user groups and arranged development sprints.


<h2>Check and expose the data</h2>

Next we reviewed the data we had extracted and indexed. Overall, we had pretty much everything we were looking for. The main issue arising at this point was the definition of collaborators, which became a more complex problem throughout the project. However, we proceeded on the agreed basis so as not to delay work at this stage.

We also considered pulling data from some alternate sources, and in particular we looked at the Grist API. We decided there was some useful data there, but that it was not core to the project to be taking data from elsewhere yet, so we just reviewed the Grist data and left it at that. We may well revisit it soon.


<h2>Application framework</h2>

During this sprint we began construction of the main application framework in which the reports are serviced, and began prototyping the queries we would need to generate the relevant reports, and started thinking about how to wire them to a user interface.

At this early stage we exposed the data initially using a facetview and a graphview, which allowed users to explore all the data and the relations present in it. This was useful for most, but also caused some concerns because it appeared that we showed data that was not as the users expected. This, we discovered, was down to the definition of collaborator again, so was not actually a development issue and so we pressed on without further delay.

Work also began with the testing group, arranging meetings with them to coincide with our new developments over the Summer.


<h2>Revisit the index</h2>

With work under way on our UI, we were able to start getting a feel for how the reports would look and thus a better idea of the queries we would have to be able to make. So at this stage we revisited the index structure defined earlier, and we made some tweaks and ensured our indexer could re-build what we needed from the updated GtR API.

We had some tricky issues here with our original mapping, after it turned out an error in the design of our first one led to it being many megabytes big, causing increasing delay as the index grew and new fields not previously in the mapping appeared. This was a minor oversight, and easy to fix.


<h2>Collaboration report</h2>

With all the preparatory work out of the way and a reliable index to query against, it was time to really get into the reports. We started with the collaboration report, as the functionality of it was required also for the benchmarking and new potential reports, so it was a good foundation.

We got a good first version of the report completed, and so now with something really interesting to show the testers, we started engaging with them more via screencasts of our developments. Here is the first one: <a href="http://www.youtube.com/watch?v=PX8-27KO4M8">http://www.youtube.com/watch?v=PX8-27KO4M8</a>, and you can find the others in the sidebar there.



<h2>Benchmarking report</h2>

With some feedback from our testers about the first collaboration report, we proceeded to tidy up that foundation and then build on it for the benchmarking report. We did a bit more fixing to the index and improved on our UI, removing some of the original quick displays and linking more closely up to institutional identities. We made the first version of the benchmarking report available, and awaited further feedback.


<h2>Collaboration report feedback</h2>

In the interim we received some more feedback about our collaboration report. We added a first-stage highlight report, a default date range and some better date formats, a better sense of what collaboration size means, and an improved definnition of funding as referring to total project funding. We made these changes available and also used some of these ideas as pointers for our other report developments.


<h2>New potential</h2>

With the foundations in place from both our collaboration and benchmarking reports, we proceeded with the slightly more complex new potential reports. Here we were able to develop quite an interactive UI that enables the user to choose their favourite projects or people, or link to an external web page, and from those we extracted keywords and searched for organisations not already in collaboration with the user. We were then able to display those findings using the same infrastructure as developed for our earlier reports, and we put this out for testing too.


<h2>Make stuff better</h2>

With our core use cases met by our three working reports, we took this sprint to go over what we had made before and review user feedback to make some tweaks and tidy things up. This also resulted in the addition of some nice improvements to the UI in the form of simple graphs of highlight figures for quick perusal by users.


<h2>Person affiliations</h2>

One of the core issues of what it means to be a collaborator revolves around the affiliations of people that are working on particular projects. Knowing that the GtR data does not guarantee to provide person affiliations correct as at time of the given project or at current time, we knew we had to look at a workaround for this. We found a way to collect person affiliation data from GtR and include it into our index so that at a later stage we can start using it to make better connections between people and organisations, but at this stage we are just holding onto the capability for use later, once it becomes clear what would be best to do with it.


<h2>Catch-up</h2>

We ended with a quick catch-up, to do some things that had been missed due to earlier error or absence or simply due to promotion of other ideas. We made further UI improvements to our reports and checked the outputs from them, as well as making the latest report downloadable. We had another look at the definition of collaboration, and started adding in functionality to allow users to override the default definition with their own. We also had a webinar session to update the interested groups about the progress, and that can be viewed here: <a href="http://www.youtube.com/watch?v=ykSGQ-gnEsU">http://www.youtube.com/watch?v=ykSGQ-gnEsU</a>.


<hr></hr>


And so we come to the end of our planned work. We are now thinking about how to proceed with the extra time that has become available, and this review will help to guide the next blog post that will compare our progress so far to our original use cases and present suggestions for going forward.






Original Title: G4HE so far
Original Author: mark
Tags: g4he, mark, news
Created: 2013-11-17 1838
Last Modified: 2013-11-18 0026
