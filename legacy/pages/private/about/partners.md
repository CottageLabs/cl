<h1 style="color: #ED1C24; padding-bottom: 10px">Organisations we work with</h1>

Mockup of how we want to the page segments associated with an organisation that we work with.

Facetview layout specifications:

 * Result title in bold, colour #ED1C24
 * Result excerpt text following on directly from result title, in normal text
 * Each result separated by a line break (so each line is directly below the one above, not separated by a paragraph break - might be a matter of paragraph styles instead)
 * 3 results per page (already configurable with facetview as-is)
 * a concise paging feature 

<div class="row-fluid">

<!-- start organisation record -->
<div class="span6">
<div class="row-fluid">
<div class="span4">
<img src="http://www.cam.ac.uk/global/images/identifier4.gif" class="img">
</div>
<div class="span8">
<div class="facetview facetview-compact facetview-descending" data-search="tags:universityofcambridge AND tags:project"></div>
</div>
</div>
</div>
<!-- end organisation record -->

</div>

<br><br><br>
<h1>Organisations we work with</h1>

Using the current standard facetview list view of project names, limiting to 2 results per result set, with the paging feature.  Presented on the left without a "Projects" title and on the right with one.

<div class="row-fluid">

<!-- start organisation record -->
<div class="span6">
<div class="row-fluid">

<div class="span4" style="background: #000000">
<img src="http://www.brunel.ac.uk/__data/assets/image/0017/1349/logo.png" class="img">
</div>

<div class="span8">
<div class="facetview facetview-titles" data-search="tags:brunel"></div>
</div>

</div>
</div>
<!-- end organisation record -->


<!-- start organisation record -->
<div class="span6">
<div class="row-fluid">
<div class="span4">
<img src="http://www.ox.ac.uk/display_images/logo.gif" class="img">
</div>
<div class="span8">
<h3>Projects</h3>
<div class="facetview facetview-titles" data-size="2" data-search="tags:oxford"></div>
</div>
</div>
</div>
<!-- end organisation record -->

</div>

<h3 style="color: #ED1C24; padding-bottom: 10px">Blog posts by Richard</h3>

<style type="text/css">

.cl_black_leader {
    color: #000000;
    font-weight: bold;
}

.cl_news_line {
     border-bottom: 1px dashed #cccccc;
     padding-bottom: 5px;
     margin-bottom: 10px;
     text-align: justify;
}

.cl_news_line strong {
    font-size: 110%;
    font-weight: bold;
}

</style>

<script type="text/javascript">
jQuery(document).ready(function() {
    var myopts = {
        "embedded_search" :  false,
        "search_url": '/query/record/_search?q=author:richard AND url:"/news/*"',
        "datatype": "json",
        "display_images": false,
        'searchwrap_start': '<div class="row-fluid"><div id="facetview_results" class="clearfix">',
        'searchwrap_end': '</div></div>',
        'resultwrap_start': '<div class="cl_news_line">',
        'resultwrap_end': '</div>',
        'result_display': [
            [
                {
                    "pre": '<strong><a class="cl_black_leader" href="',
                    "field": "url"
                },
                {
                    "pre": '">',
                    "field": "title",
                    "post": "</a></strong><br>"
                },
                {
                    "field" : "excerpt"
                }
            ]
        ]
    }
    $('.myfacetview').facetview(myopts);
});
</script>

<div class="row-fluid">
<div class="span6">
<div class="myfacetview"></div>
</div>
</div>




Original Title: partners
Original Author: richard
Created: 2013-01-13 1056
Last Modified: 2013-07-26 0232
