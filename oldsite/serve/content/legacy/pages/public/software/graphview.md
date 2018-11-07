<div class="row-fluid">
    <div class="span12">
        <div class="hero-unit">
            <h1>Using graphview</h1>
        </div>
    </div>
</div>

Graphview is a jQuery plugin that enables you to visualise the relationships between entities in a dataset.

Whereas straightforward search and faceted browse can help you to find particular pieces of information, it does not do so well at showing the relations between them, so this is the particular part that graphview focuses on. Subsequent to that, it is possible to look in more depth at the particular entities involved in the relationships.

NOTE: graphview is still very new, and there are parts of it that may not be as described. We are working on it though, and it will stabilise soon.

Graphview relies on some other really useful things, which you may want to learn about: <a href="http://jquery.com">jQuery</a>, <a href="http://jqueryui.com">jQuery UI</a>, <a href="http://d3js.org">d3</a>, <a href="http://www.elasticsearch.org">elasticsearch</a>, <a href="http://twitter.github.io/bootstrap/">bootstrap</a>, <a href="http://ivaynberg.github.io/select2/">select2</a>.

Graphview is designed to be modular, so it has some default functions that are triggered at particular times, and all of them can be overwritten. Also, the useful information retrieved from the queries that it runs are available throughout the operations. So graphview can be used as a search interface via which you can extract query results and use them to form whatever UI interactions you need.

## Basic config

How to set the thing up so you can get a response.

Copy down graphview from <a href="http://github.com/CottageLabs/graphview">the repo</a>, then link it from your web page along with the other things it depends on, (which come included in the repo) like so:

<pre>
    &lt;!-- get jquery --&gt;
    &lt;script type="text/javascript" src="jquery-1.7.1.min.js"&gt;&lt;/script&gt;

    &lt;!-- get bootstrap js and css --&gt;
    &lt;link rel="stylesheet" href="bootstrap.min.css"&gt;
    &lt;link rel="stylesheet" href="bootstrap-responsive.min.css"&gt;
    &lt;script type="text/javascript" src="bootstrap.min.js"&gt;&lt;/script&gt;  

    &lt;!-- get jquery-ui js and css --&gt;
    &lt;link rel="stylesheet" href="jquery-ui-1.8.18.custom.css"&gt;
    &lt;script type="text/javascript" src="jquery-ui-1.8.18.custom.min.js"&gt;&lt;/script&gt;
                
    &lt;!-- get select2--&gt;
    &lt;link rel="stylesheet" href="select2.css"&gt;
    &lt;script type="text/javascript" src="select2.min.js"&gt;&lt;/script&gt;

    &lt;!-- get d3 --&gt;
    &lt;script type="text/javascript" src="d3.min.js"&gt;&lt;/script&gt;

    &lt;!-- get graphview --&gt;
    &lt;script type="text/javascript" src="jquery.graphview.js"&gt;&lt;/script&gt;
</pre>

Then instantiate the graphview and set at least the most important options:

<code>
    jQuery(document).ready(function($) {
        $('#graphview').graphview({
            "option":"value",
            ...
        })
    });
</code>

<table class="table table-striped table-bordered">
<tr><td>target</td><td>The URL of the query endpoint, which must accept elasticsearch queries. You need at least to set this.</td></tr>
<tr><td>ajaxtype</td><td>How to send the queries - GET or POST</td></tr>
<tr><td>datatype</td><td>JSON or JSONP, depending on whether you want to make cross-site requests or not</td></tr>
</table>

And set up some default behaviours for the queries and result sizes:

<table class="table table-striped table-bordered">
<tr><td>suggestsize</td><td>How many suggestions to show in the suggestion dropdown</td></tr>
<tr><td>nodesize</td><td>the number of each sort of entity to show on screen</td></tr>
<tr><td>titlefield</td><td>The field in the data that should be used as the title string of the main entities</td></tr>
<tr><td>defaultquery</td><td>What to query for by defualt. NOTE: setting the facets here, along with the extra "suggest" and "node" options, is how you set what suggestion dropdowns to offer and what node types to offer.</td></tr>
<tr><td>default_operator</td><td>Whether to do AND or OR searches</td></tr>
<tr><td>query_string_fuzzify</td><td>Set to * to make search terms use the * wildcard, or to ~ to use the similarity wildcard. Or set to false to use neither.</td></tr>
</table>

## Customising functions and reading query results

The following options can be used to change the functions that run around the searches, and also shows where the query result information can be acquired from. To learn more about them, look at the ones already written.

<table class="table table-striped table-bordered">
<tr><td>showresults</td><td>What to do with the results received from the search query</td></tr>
<tr><td>response</td><td>Here you can find the query response as it comes direct from elasticsearch</td></tr>
<tr><td>nodes</td><td>The default showresults calculates nodes for display on the default visualisation. They can be accessed here.</td></tr>
<tr><td>links</td><td>Like nodes, but these are the links between them.</td></tr>
<tr><td>linksindex</td><td>A list of the links and what nodes they attach to</td></tr>
<tr><td>afterresults</td><td>This can be defined as a function that will be run after results are received from each query.</td></tr>
<tr><td>dragging</td><td>The default visualisation allows for dragging of nodes into the search box. When an object is being dragged, it can be read from here.</td></tr>
<tr><td>query</td><td>A function that returns the current query - so define here how to read the query from your UI.</td></tr>
<tr><td>executequery</td><td>This is the function that gets triggered whenever a query should be submitted.</td></tr>
<tr><td>uitemplate</td><td>This is a function that should return a template (some HTML) for the UI controls you would like.</td></tr>
<tr><td>uibindings</td><td>This function should bind things to your UI once it has been built by the uitemplate function.</td></tr>
<tr><td>searchonload</td><td>If true, then search is run as soon as the page / graphview loads.</td></tr>
</table>





Original Title: Using graphview
Original Author: mark
Tags: graphview, mark
Created: 2013-07-15 0020
Last Modified: 2013-07-15 0119
