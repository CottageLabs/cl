<div class="row-fluid">

<div class="span9">
<div class="hero-unit">
<h1>Open Citations - Doing some graph visualisations</h1>
</div>
</div>

<div class="span3">
<div>
<img src="http://cottagelabs.com/media/shotton.png">
</div>
</div>

</div>



<div class="row-fluid">

<div class="span12">

<p>Ongoing work on the <a href="/projects/opencitations">Open Citations extensions project</a> is now reaching the point of visualising - at very much a prototype level at this stage - the outputs of our earlier efforts to <a href="http://cottagelabs.com/news/open-citations-import-process">import</a> and <a href="http://cottagelabs.com/news/open-citations-indexing">index</a> the PubMed Central Open Access subset and <a target="_blank" href="http://arxiv.org">arXiv</a>.</p>

<p>Earlier in this project I asked David to specify a list of questions that he thought researchers might hope to answer by querying our Open Citations Corpus; the aim was to use these questions to guide our developments, in the hope of providing a striking interface that also did something <b>useful</b> - there are too many visualisations of data that look very pretty but that do not actually add much to the data. So, considering that list of questions and how one might visualise the data to not only a pretty but functional end, I set myself the following problem:</p>

<div class="well">
<h3>Identify what it is in a dataset that is not easy to find in a textual representation, and make it useful for search</h3>

<p>Based on our earlier <a href="http://occ.cottagelabs.com">text search demonstrator</a> the answer pretty soon became - of course - interactions; whilst the properties of a result object are obvious in a textual result set, the interactions between those objects are not - and sometimes, it is the interactions that one wishes to use as search parameters. 
</div>

<h2>What I did</h2>

<p>Having found my purpose, I set about applying the superb <a href="http://d3js.org/">D3.js</a> library to the problem, using it to draw SVG representations of elasticsearch query results directly into the browser. After testing with a number of different result layouts, I settled upon using a zoomable-pannable force-directed network graph and combined it up with some code from my PhD work to build in some connections on the fly. This is as mentioned earlier still a work in progress, but results so far are pretty good.</p>

<p>Take the image above, for example: this is a static representation of the interactions between David Shotton and all other authors (purple) with whom he has published an article (green) in the PMC OA subset. The red dots are the journals these articles are in, and the brown are citations. As a static image this could be fairly informative when marked up with appropriate metadata, and it does look quite nice; <i>but</i>, more than that, it can act as part of a search interface to enable a much improved search experience.</p>

<p>So far, the production of a given image also reduces the result set size; so whilst viewing the above image, the available suggestion dropdowns are automatically restricted to the subset of values relevant to the currenlty displaying image - dropdown suggestions are listed in order of popularity count, then upon typing one letter they switch to alphabetical, and with multiple letters they become term searches. By typing in free text search values or choosing suggestions, this visual representation of the current subset of results combined with the automated restriction of further suggestions should offer a simple yet powerful search experience. It is also possible to switch back to "list" view at any time, to see the current result set in a more traditional form. Further work - described below - will bring enhancements that add functionality to the elements of the visualisation too.</p>

</div>
</div>

<div class="row-fluid">

<div class="span6">

<h2>Try it</h2>

<p>Similarly to the search result list demonstrator, it is possible to embed the visual search tool in any web page. However, as it looks better with full screen real estate I have saved that particular trick for the time being, and simply made it available at <a target="_blank" href="http://occ.cottagelabs.com/graphview">http://occ.cottagelabs.com/graphview</a>.</p>

<p>Now before you rush off to try it, given the prototype state, you will need some pointers. Taking the above image as example once more, in order to reproduce it, do the following:</p>

<p>
<ul>
<li>Use a modern browser - Chrome renders javascript the fastest - on a reasonably decent machine to access <a target="_blank" href="http://occ.cottagelabs.com/graphview">http://occ.cottagelabs.com/graphview</a> - a large screen resolution would be particularly nice</li>
<li>Choose <b>authors</b> as a search suggestion type</li>
<li>Start typing <b>Shotton</b> - click on <b>Shotton David</b> when it appears in the list</li>
<li>(If the error where it appears to return all results again appears - described below - just keep going)</li>
<li>tick the various display options to add authors, journals and citations objects to the display</li>
</ul>
</p>

<p>The next step would be to click an author or other entity bubble then choose to add that to the search terms, or start a new search based on that bubble or perhaps a subset of the returned bubbles; however this is all still in development.</p>

<p>For a more complex example, try choosing <b>keywords</b> then type <b>Malaria</b>. Once displayed, increase resultset size to 400 so they are all displayed. Then try selecting the various authors, journals and citations tickboxes to add those objects; try increasing the sizes to see how many you can get before your computer melts... On my laptop, asking for more than about 1000 of each object results in poor performance. But here is an example of the output - all 383 articles with the Malaria keyword in the PMC OA, showing all 70 journals in which they are published, with links to the top 100 authors and citations. Which journal do you think is the large purple <a target="_blank" href="http://www.malariajournal.com/">dot</a> in the middle?</p>

</div>

<div class="span6">
<div class="img thumbnail">
<img src="http://cottagelabs.com/media/malaria.jpg">
</div>
</div>

</div>



<div class="row-fluid">
<div class="span12">

<h2>Outstanding issues</h2>

<h3>Interface</h3>

<ul>
<li>Numerous buttons have no action yet - clear / help / prev / next / + search / labels. Once these and other search action buttons are added, the visualisation can become a true part of the search experience rather than just a pretty picture</li>
<li>Searches are sent asyncrhonously and occasionally overlap, resulting in large query result sizes overwriting smaller ones. This needs a delay on user interactions added.</li>
<li>Some objects should become one - for example some citations are to the same article via both DOI and PMID, and some citations are also open access articles in our index, so they shold be linked up as such.</li>
<li>There is as yet no visual cue that results are still loading, so it feels a bit in limbo. Easy fix.</li>
<li>Some of the client-side processing can be shifted to the backend (already in progress)</li>
<li>The date slider at the bottom is twitchy and needs smoother implementation and better underlying data (see below)</li>
</ul>

<h3>Data quality</h3>

<p>Apart from the above technical tasks, we will need to re-visit our data pipeline in order to answer more of the questions set by David. For example we have very little affiliation data at present, and we are also missing a large amount of date information. Also some data cleaning is necessary - for example, keywords should all be lowercased to ensure we do not have subsets due solely to capitalisation. There are also certain types of data that we have no idea about as yet - for example author location, h-index, ORCID. However, this is all as to be expected at this stage, and overall our ability to so easily spot these issues shows great progress.</p>

<h2>More to come</h2>

<p>There is still work to be done on this graph interface, and in addition, we have some more demonstrators on the way too. In combination with the work on improving the pipeline and data quality, we should soon be able to perform queries that will answer more of our set questions - then we will identify what needs done next to answer the remaining ones!</p>


</div>

</div>




Original Title: Open Citations Graphing
Original Author: mark
Tags: opencitations, elasticsearch, d3, visualisations, news, mark, graphview
Created: 2013-02-27 0434
Last Modified: 2013-05-14 1932
