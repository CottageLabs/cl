<h1 class="cl_red_leader">Software and Standards</h1>

<p>At Cottage Labs we use and contribute to a wide variety of open source software.  Below you can see a selection of our most popular and important ones, what our involvement with them is, what services or support we can provide for you around them, and links to projects and blog posts that involve them.</p>

<p>We also understand that good open source software is standards-compliant, andwe don't just produce software but also work on the underlying standards wherever we can.  Below you can see a list of the standards we've been involved in defining, and content related to that work.</p>

<p>What you see on this page isn't everything that we use or work on.  You might also be interested in <a href="http://github.com/CottageLabs">Cottage Labs on GitHub</a>, where you can see a lot more of the code that we've written (although still not all, by any means!) 

<div class="row-fluid">
	<div class="span12 well">
		<div class="row-fluid">
			<div class="span3">
				<h3>Software</h3>
				<a href="#dspace">DSpace</a><br>
				<a href="#swordv2libs">SWORDv2</a><br>
				<a href="#facetview">FacetView</a><br>
				<a href="#graphview">GraphView</a><br>
				<a href="#elasticsearch">Elasticsearch</a><br>
				<a href="#bibserver">BibServer</a><br>
				<a href="#dmponline">DMPOnline</a><br>
			</div>
			<div class="span3"> 
				<h3>Standards</h3>
				<a href="#swordv2">SWORDv2</a><br>
				<a href="#resourcesync">ResourceSync</a><br>
				<a href="#bibjson">BibJSON</a>
			</div>
		</div>
	</div>
</div>
<div class="hero-unit" style="padding-top: 15px; padding-bottom: 10px; padding-left: 50px">
<h2 class="cl_red_leader" style="font-size: 250%">Software</h2>
</div>
<div class="row-fluid">
	<div class="span4">
		<a name="dspace"><img src="http://cottagelabs.com/media/dspacelogo.gif" class="span6" style="margin-right: 10px; margin-bottom: 10px"></a>
		<p><em>"DSpace is the software of choice for academic, non-profit, and commercial organizations building open digital repositories."</em></p>
		<p><a href="/people/richard">Richard</a> has been involved in DSpace development since its initial release in 2002, and over the years has contributed many lines of code, mailing list support, contributions to the community and countless conference papers.  We use DSpace in a number of our projects, and while we don't offer hosting or day-to-day support, we are experienced developers with the platform and can help you figure out the best approach for your development project, and build you the modules and extensions you need.</p>
		<p><a href="http://dspace.org">http://dspace.org</a></p>
	</div>
	<div class="span4">
		<h2>DSpace Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:dspace"></div>
	</div>
	<div class="span4">
		<h2>DSpace Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:dspace AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="swordv2libs"><img src="http://cottagelabs.com/media/swordlogo.jpg" class="span6" style="margin-right: 10px; margin-bottom: 10px"></a>
		<p><em>"SWORD is a lightweight protocol for depositing content from one location to another."</em></p>
		<p><a href="/people/richard">Richard</a> has been involved in the SWORD protocol since it's inception in 2007 and in 2011 took over as the technical lead driving the development of the second major version: SWORDv2.  With the involvement of <a href="/people/mark">Mark</a> and <a href="/people/martyn">Martyn</a> in a number of projects, Richard has developed - or commissioned the development of - a number of client and server software libraries to support content deposit in scholarly systems.  We therefore have extensive experience analysing and modelling system-to-system deposit scenarios and providing implementations using the code libraries we and others have worked on.  If you have a deposit integration project, we can most certainly help at any level of the work.</p>
		<p><a href="http://swordapp.org/">http://swordapp.org/</a></p>
	</div>
	<div class="span4">
		<h2>SWORDv2 Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:swordv2"></div>
	</div>
	<div class="span4">
		<h2>SWORDv2 Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:swordv2 AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="facetview"><h1>FacetView</h1></a>
		<p><em>"FacetView is a pure javascript frontend for ElasticSearch search indices."</em></p>
		<p><a href="/people/mark">Mark</a> led the initial development of FacetView in parallel with the development of <a href="#bibserver">BibServer</a> through a number of bibliography projects.  We routinely deploy FacetView instances in many of our projects, as it provides an instant and powerful way of analysing and dissecting large datasets.  We can deploy <a href="#elasticsearch">ElasticSearch</a> indices for your search/discovery needs, and can provide a flexible interface over your data using this software.</p>
		<p><a href="https://github.com/okfn/facetview">https://github.com/okfn/facetview</a></p>
	</div>
	<div class="span4">
		<h2>FacetView Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:facetview"></div>
	</div>
	<div class="span4">
		<h2>FacetView Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:facetview AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="graphview"><h1>GraphView</h1></a>
		<p><em>"A jquery / js thingy that lists and visualises search results from an elasticsearch index."</em></p>
		<p><a href="/people/mark">Mark</a> started working on GraphView in response to an increasing need in our projects to not just provide searchable data but to provide visualisations of that data.  We can deploy <a href="#elasticsearch">ElasticSearch</a> indices for your search/discovery needs, and can provide a flexible graphical interface over your data using this software.</p>
		<p><a href="http://cottagelabs.com/software/graphview">http://cottagelabs.com/software/graphview</a></p>
	</div>
	<div class="span4">
		<h2>GraphView Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:graphview"></div>
	</div>
	<div class="span4">
		<h2>GraphView Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:graphview AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="elasticsearch"><h1>Elasticsearch</h1><img src="/media/elasticsearch.png" class="span6"></a>
		<p><em>"flexible and powerful open source, distributed real-time search and analytics engine for the cloud"</em></p>
		<p>While we don't contribute any code to the Elasticsearch code-base, we use it extensively as a storage and indexing back-end to lots of our software, including <a href="#facetview">FacetView</a>, <a href="#graphview">GraphView</a>.  If you have a project which requires large scale indexing or analysis of data, we can deploy an effective Elasticsearch solution which will provide you with all the power you need.</p>
		<p><a href="http://elasticsearch.org">https://elasticsearch.org</a></p>
	</div>
	<div class="span4">
		<h2>Elasticsearch Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:elasticsearch"></div>
	</div>
	<div class="span4">
		<h2>Elasticsearch Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:elasticsearch AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="bibserver"><img src="http://cottagelabs.com/media/bibserverlogo-300x54.png" class="span6" style="margin-right: 10px; margin-bottom: 10px"></a>
		<p><em>"BibServer is a tool for quickly and easily sharing collections of bibliographic metadata."</em></p>
		<p><a href="/people/mark">Mark</a> led the initial development of BibServer through a number of bibliography projects, where the <a href="#name">BibJSON</a> standard also emerged.  BibServer is now maintained by the Open Knowledge Foundation, and drives the <a href="http://bibsoup.net">BibSoup</a> service.  If you have customisations to the platform to support your requiremens, or you want to deploy your own instance, we are able to help.</p>
		<p><a href="http://bibserver.org">http://bibserver.org</a></p>
	</div>
	<div class="span4">
		<h2>BibServer Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:bibserver"></div>
	</div>
	<div class="span4">
		<h2>BibServer Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:bibserver AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="dmponline"><img src="http://cottagelabs.com/media/dmp_logo.png" class="span6" style="margin-right: 10px; margin-bottom: 10px"></a>
		<p><em>"DMP Online has been developed by the Digital Curation Centre to help researchers and research support staff produce data management plans (DMPs)."</em></p>
		<p><a href="/people/martyn">Martyn</a> and <a href="/people/richard">Richard</a> have both worked on the SWORDv2 development for this software, enabling deposit of data management plans to institutional repositories.  The software is maintained and hosted by the Digital Curation Centre, but if you need us to help getting you set up, or if you need to run a version of the software yourself we can assist.</p>
		<p><a href="https://dmponline.dcc.ac.uk/">https://dmponline.dcc.ac.uk/</a></p>
	</div>
	<div class="span4">
		<h2>DMPOnline Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:dmponline"></div>
	</div>
	<div class="span4">
		<h2>DMPOnline Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:dmponline AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<br><br><br>
<div class="hero-unit" style="padding-top: 15px; padding-bottom: 10px; padding-left: 50px">
<h2 class="cl_red_leader" style="font-size: 250%">Standards</h2>
</div>
<div class="row-fluid">
	<div class="span4">
		<a name="swordv2"><img src="http://cottagelabs.com/media/swordlogo.jpg" class="span6" style="margin-right: 10px; margin-bottom: 10px"></a>
		<p><em>"SWORD is a lightweight protocol for depositing content from one location to another."</em></p>
		<p><a href="/people/richard">Richard</a> has been involved in the SWORD protocol since it's inception in 2007 and in 2011 took over as the technical lead driving the development of the second major version: SWORDv2.  He has worked to build a community of contributors and users of the specification throughout the whole of Higher Education. This standard has become the de-facto approach for machine-to-machine deposit in scholarly systems.  If you have a deposit integration project, we can most certainly help at any level of the work.</p>
		<p><a href="http://swordapp.org/">http://swordapp.org/</a></p>
	</div>
	<div class="span4">
		<h2>SWORDv2 Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:swordv2"></div>
	</div>
	<div class="span4">
		<h2>SWORDv2 Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:swordv2 AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr>
<div class="row-fluid">
	<div class="span4">
		<a name="resourcesync"><h1>ResourceSync</h1><img src="http://cottagelabs.com/media/resourcesync_logo.png" class="span6"></a>
		<p><em>"describes a synchronization framework for the web consisting of various capabilities that allow third party systems to remain synchronized with a server's evolving resources"</em></p>
		<p><a href="/people/richard">Richard</a> was part of the technical committee advising the core ResourceSync team on the development of this web standard, and went on to develop proof-of-concept implementations against DSpace.  We anticipate great success for this standard, and if you are looking to implement compliance, we can offer support at any level of your project.</p>
		<p><a href="http://www.openarchives.org/rs">http://www.openarchives.org/rs</a></p>
	</div>
	<div class="span4">
		<h2>ResourceSync Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:resourcesync"></div>
	</div>
	<div class="span4">
		<h2>ResourceSync Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:resourcesync AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>
<hr><div class="row-fluid">
	<div class="span4">
		<a name="bibjson"><h1>BibJSON</h1></a>
		<p><em>"BibJSON is a convention for representing bibliographic metadata in JSON; it makes it easy to share and use bibliographic metadata online."</em></p>
		<p><a href="/people/richard">Mark</a> led the initial work in distilling the BibJSON standard from previous work in the sector, and this has now taken on a life of its own as a community of best practice.</p>
		<p><a href="http://bibjson.org/">http://bibjson.org/</a></p>
	</div>
	<div class="span4">
		<h2>BibJSON Projects</h2>
		<div class="facetview facetview-compact facetview-descending" data-search="tags:project AND tags:bibjson"></div>
	</div>
	<div class="span4">
		<h2>BibJSON Stories</h2>
		<div class="facetview facetview-compact facetview-descending" data-search='tags:bibjson AND (url:"/news/*" OR tags:news)'></div>
	</div>
</div>




Original Title: software
Original Author: test
Created: 2012-07-10 2350
Last Modified: 2013-12-05 1118
