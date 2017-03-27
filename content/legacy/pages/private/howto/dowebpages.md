<a name="newpages"></a>
# Make new pages

You can make a new webpage just by going to the address where you want the page to be. A new one will be created there, and you will be asked to confirm some settings then you can write your new page. The pages are collaboratively editable by default, so you can share the link with other people and work together on it.

Remember as well when making pages that a useful way to learn how to do something is to look at other pages for examples. Check out other pages on this site and open the editable versions to see how they are made. (This page uses markdown headers, for example.)


<a name="pagesettings"></a>
# Changing page settings / publishing pages

New pages start off just as collaboratively editable pads that are open to anyone but not discoverable via the site search unless you are logged in. When you are happy with your page, you can change the page settings to display as a proper webpage by default, then it can only be edited by selecting the "edit page" in the options menu, which only logged in people can see. You can also make the page discoverable via site search. Remember also to give your page a good title and set the author and a short excerpt for use in search result displays, along with some relevant tags to make it easier to find.

Pages can also be moved to new URLs by just editing the URL string in the page settings.

If you need to delete a page, you can do that via the page settings too.


<a name="clstyles"></a>
# Cottage Labs colours, fonts, logos

If you are wanting to style stuff in theme with the Cottage Labs colours, here they are:

Cottage Labs black: #333333

Cottage Labs blue/grey: #c9d2d4

Cottage Labs red: #ed1c24

Our text font is Open Sans, or Verdana. Usually 11px size.

Also you can access our logos here:

Website header - large, rectangular: <http://cottagelabs.com/media/cropped-Cottage-on-hill-bubble-smoke.jpg>

Cottage Labs logo - smallish, square: <http://cottagelabs.com/media/cottage_hill_bubble_small.jpg>

Website favicon - very small, square: <http://cottagelabs.com/static/favicon.jpg>


<a name="markdown"></a>
# Make a simple webpage using markdown

Our text editor understands the markdown syntax, so when you want to quickly make a simple page of text content that does not require complex formatting and layout, you can just use markdown instead of writing full HTML.

You can also use a combination of markdown and HTML on the same page, but note that markdown syntax will not be converted if it is inside an HTML object. So don't make a <code>&lt;div&gt;</code> then put markdown inside it - it won't work.

Read the markdown docs: <http://daringfireball.net/projects/markdown/basics>


<a name="bootstrap"></a>
# Style a page using bootstrap

This website has twitter bootstrap CSS options built in, so you can do really nice complex styling of your page content. This requires you to know a bit about HTML and CSS, and to read the twitter bootstrap documentation.

NOTE - we use the responsive layout styles so that our content can be re-used in many places and so that it works well on different browsers and devices. So when creating divs where there is an option for them to be fluid, you should use the fluid ones (such as <code>&lt;div class="row-fluid"&gt;</code>). See the bootstrap docs for more info about responsive layout

Twitter bootstrap docs: <http://twitter.github.com/bootstrap/>

Intro to HTML: <http://www.htmldog.com/guides/htmlbeginner/> 

More about HTML5 (the version we use): <http://www.html5rocks.com/en/>

Intro to CSS: <http://www.htmldog.com/guides/cssbeginner/>

For generic info, just [google](http://google.co.uk) anything you are unsure about, and you can check out [w3schools](http://w3schools.com), although they are not always 100% accurate.


<a name="facetview"></a>
# Embed content search / browse panels using facetview

[Facetview](http://github.com/okfn/facetview) is also built in to this site. You can use it to display search result lists as browseable content, or to embed search panels into webpages. You can put more than one facetview section in any page, so you can have collections of browseable content.

In order to make this work, all you need to do is use a little bit of HTML to enable it. Create a new <code>&lt;div&gt;</code> with the class "facetview" and you will get your search panel:

<code>
&lt;div class="facetview"&gt;&lt;/div&gt;
</code>

Then you need to choose some layout settings by adding more classes - HTML allows multiple classes, so just add them to the class string.

<pre>
facetview-slider: nice big left-right buttons at the bottom instead of the pager counter
facetview-descending: order the results by descending created date
facetview-ascending: order by ascending created date
facetview-searchable: include a search bar at the top so the results can be filtered

For example, a facetview in descending date order: &lt;div class="facetview facetview-descending"&gt;&lt;/div&gt;
</pre>

Then you can add some data attributes to control how things are displayed:
<pre>
data-search: use this attribute to set a search term to limit what is displayed
data-size: use this to set how many results to display
data-from: choose where to start displaying results from e.g. from 4 starts showing results from the fourth result onwards

For example, a facetview in descending date order with a search filter of everything tagged "admin":
&lt;div class="facetview facetview-descending" data-search="tags:admin"&gt;&lt;/div&gt;
</pre>

The searches are managed by elasticsearch. If you want to read more about how to write search terms, check out the [elasticsearch docs](http://www.elasticsearch.org/guide/reference/query-dsl/)


<a name="dynamicembed"></a>
# Dynamically embed one page inside another

When writing one page, you may want to use the content of another page, and you probably want that content to stay up to date. In this case, use the dynamic embed functionality. Again, it can be done just by using a <code>&lt;div&gt;</code> with class="dynamic", and set the data-source attribute to the URL of the page you want to include.

<pre>
&lt;div class="dynamic" data-source="/index"&gt;&lt;/div&gt;
</pre>

So, using the above would embed the content of the index page into whatever page you put this code. You can also wrap the dynamic div with more divs and style them using bootstrap, to control the layout of how the embedded content will fit into the containing page.

Note that dynamic embeds cascade, so if the page you are embedding also includes dynamically embedded pages, they will be include too. Don't create an infinte loop! e.g. don't embed a page that embeds the page you are embedding into - it will never end...







Original Title: Use the CL website page functionality - dynamic embeds, embedded search panels, etc
Original Author: mark
Tags: howto, webpages, dynamic, static, embed, search, facetview, bootstrap, paging, style, styling, content
Created: 2013-01-24 1915
Last Modified: 2013-01-26 1144
