
<div class="span12">
<h1 style="color: #ED1C24; padding bottom: 10px">Update from the GtR / G4HE hackday</h1>
<p>Earlier this month, members of the G4HE  project team from Cottage Labs and Cambridge kicked off the technical stage of the project at a hackday hosted by the GTR team in Swindon. The objective of the hackday was to explore the GTR API to find out a&#41; the quality of the GTR data, b&#41; what can be done with current GTR data and c&#41; how this affects the use-cases. The team were pleased to discover that the API works well, and is only lacking an update mechanism which will hopefully be added soon.</p>
</div>

<div class="row-fluid">
<div class="span6">

<h2>Data Quality</h2>

<p>One of the concerns that had been raised in earlier project meetings was the quality of the GTR data. The team from Cambridge did some analysis of the data and have clarified a bit of what is missing - essentially output data such as publications derived from grants is a bit light on the ground, as it was not always collected when grants were input on systems. The team found that there are some errors and duplication in the data, however a lot of this appears to be due to input errors pre-GtR collation, such as users typing organisation names differently because there are no canonical versions, or because users simply use the fields in different ways, for example treating organisations and collaborations as the same in some cases, whereas others treat them as different. &#40; It is worth mentioning that GtR do however have a clear distinction of the appropriate function of each field.&#41; Where there is data missing due to historic reasons such as publication data not being required pre-2011, we expect to be able to encourage significantly higher submissions of such data by offering solutions to the desired use cases. Where there is data missing because it has never been of interest for collection, we should encourage increased submission of such data where it supports the desired use cases. Once that becomes the case, then it should be possible to answer our use cases from the perspective of grant outputs in addition to grant specifications. One of the next tasks for the GtR team is the simple deduplication of entities, such as organisations with similar names. This is good news for the G4HE project as it will be useful for improving our intended functionality as well as the GtR data, so the project team will be keen to keep up to date with the changes being made at GtR as the work progresses.</p>

</div>


<div class="span6">
<a class="span12 img thumbnail" href="http://cottagelabs.com/media/cam_data_pubs_all_unis.jpg"><img src="http://cottagelabs.com/media/cam_data_pubs_all_unis.jpg"/></a>
<p>The above graph was put together by the members of the project team from Cambridge and shows the number of publications that can be found for all universities available in the GtR data. The headline figure shows that about 75% do not have any publications listed against them, although we also know that numerous data sources did not require collection of such information until recently. So, the downside for Cambridge is that there is not a great deal of data currently available in GtR about publications, but the upside is that what is there is easily found and usable, so we can demonstrate value based on that and give people an incentive to provide more of that sort of data. Cambridge also did similar analyses for publications just for Cambridge, and also for outcomes from all universities and for Cambridge - in all cases the numbers are similar, with about 75% currently not listing any outcomes.</p>
</div>
</div>

<div class="row-fluid">
<div class="span6">
<h2>What can be done with the current GtR data?</h2>

<p>Our  developers had a play around with the API to see what we could do with the GtR data during the hackday.  We have written a Python client library which can interact with the GtR API, giving developers a quick route to the data and dealing with complexities such as paging through result sets. It currently supports the XML and JSON data formats from the native data format, however it does not currently support the CERIF API. We  retrieved all the data from the API and used it to build an index. Using Facetview, we have set up a simple faceted search interface which can be viewed<a title="Faceted search interface" href="http://test.cottagelabs.com/gtr/facetview/" target="_blank"> here </a>. We have also set up a rather nice visual interface via Graphview (this is currently a prototype, so does not yet function fully, but gives a nice indication of how the data might be presented when we come to build the G4HE tools.) This can be viewed<a title="Graph view" href="http://test.cottagelabs.com/gtr/graphview/" target="_blank"> here. </a></p>

</div>

<div class="span6">
<a class="span12 img thumbnail" href="http://cottagelabs.com/media/brunel.jpg"><img src="http://cottagelabs.com/media/brunel.jpg"/></a>
<p>The above visualisation shows how the search results for all collaborations and publications involving Brunel look on the Graphview visual interface. </p>

</div>
</div>

<h2>How does this affect the use cases?</h2>

<p>What we were able to ascertain from the hackday is that of the use cases currently outlined, none are blocked by the current state of the data or by the API; some could be better answered by additional data being made available - something which could be achieved through future engagement and motivating users to provide such additional data. This will require community development rather than (or in addition to) technical development - e.g. a desire and agreement on how best to provide such data - formats, naming conventions, reporting standards, etc. and how best to make it worthwhile for people to put post-data in, such as research outputs after a project is complete.</p>

<h2>So what's next?</h2>

<p>Based on the work our developers were able to do at the hackday, we have discovered the following:</p>
<div id="main">
<div>
<div id="article">

<p>Our top three use cases are do-able on the basis of grants information available on GtR:</p>
<ul>
        <li>As a Research Manager I want to report to senior management about key collaborations within the grant portfolio because they need to identify institutions with whom to build partnerships</li>
        <li>As a senior manager/head of research I want to be able to benchmark funding awarded between groups of researchers at my institution with groups at other institutions because I want to ensure that we are performing at the expected level</li>
        <li>As a senior manager/head of research I want to be able not just to see who we are collaborating with in particular areas but also which other institutions engaged in the same area are not collaborating with us because I want to identify possible future collaborations in my area of interest</li>
</ul>
<p>The remaining two are conceptually possible but would require clarification of the terms "commercial/industrial partners", "knowledge transfer", and "department":</p>
<ul>
        <li>As a research manager I want to see number and value of collaborations with commercial/industrial partners because it helps me understand the value and extent of our knowledge transfer activities and information that could be helpful for internal and external (e.g. HE-BCI) reporting</li>
        <li>As a senior manager/research group leader I want to see how much a department has brought in because it helps me show the success of our groups</li>
</ul>
<p>The next steps for the project team will be to define the project deliverables based on the above use cases, along with plans for sustaining the deliverables after the end of our project.</p>

</div>
</div>
</div>
<div id="comments"></div>









Original Title: G4HE Hackday
Original Author: bex
Tags: g4he, mark, hack, elasticsearch, brunel, richard, emanuil, cambridge, bex, facetview, graphview, news
Created: 2013-03-18 0932
Last Modified: 2013-05-24 1552
