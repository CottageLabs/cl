<div class="row-fluid">
<div class="span12">
<div class="hero-unit">
<h2>Using our various open source softwares to realise desired architectures</h2>
<h3>An example from G4HE</h3>
</div>
</div>
</div>

<div class="row-fluid">

<div class="span12">
<h2>Everything has architecture</h2>
<p>The architecture of a thing is its form; it is a beauty identifiable by ability - the form of the thing informs us of what it can do.</p>
<p>When we spend a lot of time being creative, we not only become aware of the regularity with which these forms become apparent, but with the similarity between them &mdash; there are but a few basic forms, which can be combined in many different ways.</p>
<p>None of these are particularly new in the theory of architecture or of software development, and indeed, there are many flaws in the software that I write and many messy constructions where I have not made the effort to build as well as I should have.</p>
<p>But what is most important about good architecture is not how well a thing is built, but how well the built thing meets the needs of those who utilise it; to know the answer to this, we must know more about those needs. This is not new either - the theories of requirements gathering and the application of requirements to the design of good software architectures are also well known.</p>
<p>So, what can we learn here? Nothing, really - somebody somewhere probably already knows more than I do. But, within this context, we can simply move forward with the most useful forms and combinations of forms. If we can make things that are actually used we will have had some measure of success, and from the people that actually <i>use</i> our creations we will learn more about the rough edges to our forms.</p>

<h2>Are there ugly forms that we can ignore?</h2>
<p>Yes. Of course. But the definition of beauty is subjective &mdash; although not to an individual but to a community. We share our perceptions of things and make communal assertions as to their beauty, based on the application of form to our needs. So forms that cannot be expressed in terms of community needs are undesirable, and should be avoided.</p>
<p>However we cannot prettify a thing by trying to make it look like something we used before &mdash; this is a weakness, a short cut; we must work hard to build something of <i>appropriate</i> form.</p>
<p>So we will not list the ugly forms; there is no need. We will know them when we see them. Instead, we will think of the pretty forms.</p>

<h2>What are the pretty forms?</h2>
<p>They are the ones that reflect the things we want to do.</p>

<h2>What do we want to do?</h2>

<table class="table table-striped table-bordered">
<tr><td>Find things in the world of relevance to us</td></tr>
<tr><td>Consume information about those things</td></tr>
<tr><td>Organise and query what we consume</td></tr>
<tr><td>Manage and improve what we have learnt by further reflection and reference to additional external sources as required</td></tr>
<tr><td>Make connections between the various things we have learnt about</td></tr>
<tr><td>Select particular subsets as foundations for further analyses or conjectures</td></tr>
</table>

<h2>How can we do it?</h2>

<table class="table table-striped table-bordered">
<tr><td>Find things</td><td>APIs</td><td>By using APIs between our own and other software systems we can access and share information. Read more about <a href="/reports/advantages-of-apis">the advantages of APIs</a></td></tr>
<tr><td>Organise and query</td><td>Elasticsearch</td><td><a href="http://www.elasticsearch.org">Elasticsearch</a> is an index instead of a database - that means it focuses on making data easy to search (of course it still does storage like a database too). </td></tr>
<tr><td>Manage and improve</td><td>Portality</td><td>We need an infrastructure to expose and access the data that we find via APIs and store in our index; <a href="/software/portality">portality</a> is a collection of useful methods that can be easily strung together into an app that meets a range of such requirements.</td></tr>
<tr><td>Connect</td><td>Graphview</td><td>Once we can query our collected information, a great thing to do that goes beyond just searching the data is to visualise the relationships between different entities. This allows us to learn more from our corpus of information. <a href="/software/graphview">Graphview</a> does this for us.</td></tr>
<tr><td>Select subsets</td><td>Facetview</td><td>Using the power of search, we can select subsets of data based on particular criteria and use those subsets for futher processing. <a href="http:/github.com/okfn/facetview">Facetview</a> provides a simple app that can be customised to this use case.</td></tr>
</table>

<h2>In relation to G4HE</h2>

<p>On the <a href="/projects/g4he">G4HE</a> project we have a specific set of data available that we would like to make good use of - the <a href="http://gtr.rcuk.ac.uk">GtR API</a> provides information about research projects funded in the UK by seven major research councils. So we can use that API as a source, and extract data into our own local index. Then we can customise our Portality software to provide specific functionality of use to the Higher Education community, integrating with facetview and graphview to provide powerful UI features that enable people in the community to find the information that interests them and learn more from it, for example by building collaboration and benchmarking reports.</p>

<p>What is great about the way we create and share software (and not just because we do it, but because a worldwide community of people do it) is that there are no restrictions to what can be done with the software or how many times it can be done or by whom it can be done; the software are blocks that exist solely to enable us to build the architectures that we need to support our community.</p>

</div>
</div>



Original Title: Using our various open source softwares to realise desired architectures
Original Author: mark
Tags: g4he, open access, mark, elasticsearch, facetview, graphview, portality, news
Created: 2013-07-14 2321
Last Modified: 2013-07-17 1137
