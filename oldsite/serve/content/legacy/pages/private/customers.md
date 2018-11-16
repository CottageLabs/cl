

<div class="row-fluid">
<div class="span8">

<h1 style="color:white;">Our work with <select id="companies" style="background-color:#66bbff;font-size:1em;height:60px;font-weight:bold;color:white;margin-top:5px;width:400px;">
<option></option>
<option value="jisc">Jisc</option>
<option value="universityofoxford">University of Oxford</option>
<option value="universityofedinburgh">University of Edinburgh</option>
<option value="lanl">LANL</option>
<option></option>
<option></option>
</select></h1>

<p class="lead companies jisc">Jisc are a UK funding body and charity, and we work with them on numerous projects, both in direct partnership and on projects for other organisations that are funded by Jisc.</p>

<p class="lead companies universityofoxford"></p>

<p class="lead companies universityofedinburgh">We work with the University of Edinburgh on a number of projects to increase access to higher education in Scotland.</p>

<p class="lead companies lanl">Los Alamos National Laboratory are a US Government body working in a variety of defence and internet technology related fields.</p>

</div>
<div class="span4">

<img class="img thumbnail companies jisc" src="/media/jisc-logo.jpg">

<img class="img thumbnail companies universityofoxford" src="/media/oxford.gif">

<img class="img thumbnail companies universityofedinburgh" src="/media/edinburgh.png">

<img class="img thumbnail companies lanl" src="/media/LANL_logo.png">

</div>
</div>



<input type="hidden" id="searching" name="q">




<BREAK_CONTAINMENT>



<div class="facetview facetview-alternates facetview-descending" data-size="100" data-searchbox_class="#searching" data-predefined_filters='{"tags":{"query_string":{"query":"tags:project"}}}'></div>


<style>
.facetview_metadata{
    display:none;
}
.fvpublished{
    display:none;
}
.fvtags{
    display:none;
}
.companies{
    color:white;
}
img.companies{
    background-color:white;
}
</style>


<script type="text/javascript">
jQuery(document).ready(function () {

$('.companies').hide();

var companies = function(event) {
    $('.companies').hide();
    var c = $(this).val();
    $('#searching').val( c );
    $('.' + c).show();
    $('#searching').trigger('keyup');
}
$('#companies').bind('change',companies);

var q = $.getUrlVar('q');
if ( q ) {
    $('#companies').val( q );
    $('.' + q).show();
}

$('#mainnav').css({'background-color': '#66bbff'});
$('#main').css({
    'background-color': '#66bbff',
    'margin-bottom': '-10px'
});


});
</script>



Original Title: Our customers
Original Author: mark
Created: 2013-09-23 1920
Last Modified: 2013-10-21 1840
