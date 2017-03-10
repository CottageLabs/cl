<!--
need a fix for opacifying extra panels when enabling from javascript
<style type="text/css">
.step:not(.active) {
    opacity:"0.3";
}
</style>
-->

<script type="text/javascript">
jQuery(document).ready(function () {
var slideshow = function(event) {
      event ? event.preventDefault() : "";
      $('#enableslideshow').hide();
      $('#topstrap').hide();
      $('hr').hide();
      $('#bottom').hide();
      $('#home').before('<div class="hint">use space bar, arrow keys, or swipes (on touchscreens) to navigate</div>');
$('.step').css({
        width: '900px',
        'font-size': '1em',
        'min-height': '500px',
        'background-color': 'white',
        'margin-left': '700px',
        display: 'block',
        padding: '40px 60px',
        'border-radius': '10px',
        'box-shadow': '0 2px 6px rgba(0, 0, 0, .1)',
        border: '1px solid rgba(0, 0, 0, .3)',
        color: 'rgb(102, 102, 102)',
        'text-shadow': '0 2px 2px rgba(0, 0, 0, .1)',
        'letter-spacing': '-1px',
        '-webkit-box-sizing': 'border-box',
        '-moz-box-sizing': 'border-box',
        '-ms-box-sizing': 'border-box',
        '-o-box-sizing': 'border-box',
        'box-sizing': 'border-box',
        '-webkit-transition': 'opacity 1s',
        '-moz-transition': 'opacity 1s',
        '-ms-transition': 'opacity 1s',
        '-o-transition': 'opacity 1s',
        transition: 'opacity 1s'
})
$('.hint').css({
        background: '#333',
        color: '#fff',
        'text-align': 'right',
        padding: '10px',
        'z-index': '100',
        '-webkit-transform': 'translateY(400px)',
        '-moz-transform':    'translateY(400px)',
        '-ms-transform':     'translateY(400px)',
        '-o-transform':      'translateY(400px)',
        transform:         'translateY(400px)',
        '-webkit-transition': 'opacity 1s, -webkit-transform 0.5s 1s',
        '-moz-transition':    'opacity 1s,    -moz-transform 0.5s 1s',
        '-ms-transition':     'opacity 1s,     -ms-transform 0.5s 1s',
        '-o-transition':      'opacity 1s,      -o-transform 0.5s 1s',
        transition:         'opacity 1s,         transform 0.5s 1s'
})
$('.not-supported .step').css({
        position: 'relative',
        opacity: 1,
        margin: '20px auto'
})
      $('div.content').css({ "margin-top": "-40px"});
      $('#article').jmpress();
//$('.step:not(.active)').css({opacity: '0.3'});
};
$('#enableslideshow').bind('click',slideshow)
})
</script>

<div id="home" class="step row-fluid">

<div class="span6">

<div class="hero-unit">
<h1>Case study</h1>
<h2><br>Artemis Intelligent Power</h2>
</div>

<p>This case study also presents an experiment of displaying our content well on web pages whilst secondarily supporting other methods of using it - for example, as a slideshow or downloading as a nice PDF (in development).</p>
<p><a id="enableslideshow" class="btn" href="">experimental - view as slideshow</a></p>
<!--
<p>If this case study interests you, then <a href="#contactinline">get in touch</a> with some info about yourselves, and we will help you discover how Cottage Labs can help your business</p>
-->

</div>

<div class="span6">

<a class="span12 img thumbnail" href="http://cottagelabs.com/media/artemisgroup.jpg"><img src="http://cottagelabs.com/media/artemisgroup.jpg" /></a>

</div>

</div>


<hr></hr>


<div class="step row-fluid" data-x="1000">

<div class="span6">
<div class="hero-unit">
<h1>Overview</h1>
</div>

<h2>About Artemis</h2>
<p><br>Part of Mitsubishi Power Systems Europe, <a href="http://www.artemisip.com/">Artemis Intelligent Power</a> carries out research, development and technology licensing associated with its trademark Digital Displacement hydraulic power technology; along with other innovations in the control and transmission of fluid power.  Through its long term development projects with market-leading industrial partners, the company has continued to grow and as a result needed to update its manufacturing process to meet global demand. The company  had a purpose built manufacturing facility adjacent to its R&amp;D headquarters, however its existing parts database was inadequate for external facing production. </p>



</div>

<div class="span6">
<h2>The challenge</h2>
<p>Cottage Labs was commissioned to create a custom parts database to meet the organisation's changing manufacturing and R&amp;D needs. Existing products were priced for large scale manufacturers and lacked the required functionality and flexibility. <p>

<h2>Our solution</h2>
<p>Working closely with the team at Artemis, Cottage Labs created a bespoke relation-less database to track and manage parts within the company's workflow. The new database was designed to cope with complex history, assembly, testing and component data, and to give Artemis better control of their inventory. The database was built on entirely open source software components, which had been tried and tested by the wider developer community and are not subject to restrictions on future development or expensive proprietary license fees. Phase 1 was deployed within one month of initial requirement sign off. </p>

</div>

</div>



<hr></hr>



<div class="step row-fluid" data-x="2000">

<div class="span6">

<div class="hero-unit">
<h1>Details</h1>
</div>

<h2>Project Outline</h2>

<p>Artemis required </p>
<p>Cottage Labs identified a series of steps to complete to achieve the project aims.</p>
<ul>
<li>Creating new part record and assigning an ID.</li>
<li>Creating new assembly record.</li>
<li>Editing part and assembly record with further details at any time</li>
<li>Identifying which assembly a part belonged to</li>
<li>Search for part or assembly, by location, status, any value in a document.</li>
<li>Automated local backup script.</li>
<li>Operator and technical manual.</li>
<li>Import data from old system.</li>
</ul>


<h3>What was required for success?</h3>

<p>The ability to accurately detail changes and account for the movement of items was limited in the existing database. Likewise the process for commercial production demanded the ability for greater granularity in tracking test data, part and assembly changes.</p>
<p>Cottage Labs worked with Artemis to map out their production workflow and created a tailored solution that improved efficiency and matched the companyâs forward-looking goals.</p>

</div>

</div>



<hr></hr>



<div class="step row-fluid" data-x="3000">

<div class="span6">

<div class="hero-unit">
<h1>Benefits</h1>
</div>

<h2>Business Advantages</h2>

<table class="table table-striped table-bordered"> 
<tr><td>The implementation of the new bespoke database provides a number of advantages in terms of speed, flexibility, efficiency and scale.</td></tr>
<tr><td>The ability to search and track parts and assemblies at a much finer level of detail has meant that the entire production workflow can be more streamlined and robust.</td></tr>
<tr><td>As new assemblies are created and tested a full record of all interactions is stored, paving the way for Artemis to move towards ISO 9000 accreditation. This will allow the business to seek larger contracts and grow into international markets.</td></tr>
<tr><td>The Cottage Labs Facetview powered solution also creates an open environment that allows a company to easily support future technological developments. Artemis have the potential to move to automated tracking via bar code scanning on all parts and the open design of this solution allows support to be built in from the ground up.</td></tr>
</table>

</div>

<div class="span6">

<h2>Technical advantages</h2>

<p>Cottage Labs has created a unique software stack, employing cutting edge Open Source code for data management. The key to the success of this software is based around two main components â Facetview and Bibserver â which provide unparalleled search, storage, and recovery of documents. </p>

<p>Typically websites, CMS or databases are limited in teh ways that they can search and present information but by combining the latest software tools Cottage Labs has been able able to deliver a faster search experience.</p>

<p>The front end of this software is based around the FacetView code. This tool is a <a href="http://jquery.com/">jQuery</a> plugin that lets you easily embed a faceted browse front end into any web page. This means that results can be filtered (faceted) to easily find the documents or records you need. It can interoperate with a variety of back-end search tools such as <a href="http://lucene.apache.org/solr/">SOLR</a> or <a href="http://elasticsearch.org/">ElasticSearch</a> (both of which are based on <a href="http://lucene.apache.org/">Lucene</a>).</p>

<p>BibServer is an open-source RESTful bibliographic data server. Cottage Labs has built on extensive experience designing and building software for library data management to repurpose this tool. In this software stack elements of bibserver code have been used to create a powerful tool to create and manage collections of records.</p>

<table class="table table-striped table-bordered">
<tr><td>
<h4>Reliability</h4>
<p>Building on a range of well tested Open Source tools Cottage Labs created a bespoke solution that included components that were tried and tested. Building on community efforts such as bibserver and facetview helped to ensure that software bugs were non-critical and that data security was maintained.</p>
</td></tr>


<tr><td>
<h4>Stability</h4>
<p>With an existing database that was nearing capacity the liability of failure was high. By moving to new, scalable technology Artemis were able to provide for growth with a a stable data environment.</p>
</td></tr>

<tr><td>
<h4>Accountability</h4>
<p>In comparison to proprietary or closed-source software the tools provided by Cottage Labs are completely open and auditable. The entire code base is examinable for qualities such as security, freedom from backdoors, adherence to standards and flexibility in the face of future changes. </p>
</td></tr>
</table>

</div>

</div>



<hr></hr>



<div class="step row-fluid" data-x="4000">

<div class="span6">

<div class="hero-unit">
<h1>Results</h1>
<blockquote><br>Cottage Labs delivered a solution that made it easy for us to store, manage, search and retrieve our data</blockquote>
</div>

</div>

<div class="span6">

<a class="img thumbnail" href="http://cottagelabs.com/media/screen.jpg"><img src="http://cottagelabs.com/media/screen.jpg" /></a>
<p>Screengrab: Artemis Parts Tracking Database frontpage</p>

<a class="img thumbnail" href="http://cottagelabs.com/media/screen2.jpg"><img src="http://cottagelabs.com/media/screen2.jpg" /></a>
<p>Screengrab2: New Part interface screen</p>

</div>

</div>



<a name="contactinline"></a>
<hr></hr>



<div class="step row-fluid" style="background-color:#c9d2d4;" data-x="5000">

<div class="span6" style="padding:10px;">
<h2>Cottage Labs Solutions</h2>

 <p><br>Cottage Labs builds customized solutions to help businesses of all sizes manage their data more effectively. </p>

 <p>We use open source software on all of our projects so you own all the code and will never need to pay for proprietary upgrades or addons again. This means we use robust, freely available software that has been thoroughly tested and never relies on the commercial interest of any one company. </p>
 
<p> As a result you can save on expensive and restrictive licensing fees and never need to be tied to one supplier.</p>

<p>To find out what Cottage Labs can do for your company - get in touch now</p>

</div>

<div class="span6" style="padding:10px;">

<form id="contactinline" action="/contact" method="post" class="clearfix">
<p><textarea class="span12" style="min-width:200px;height:180px;" placeholder="Introduce yourselves, provide some contact details for us to get back to you, and we will talk soon" name="message"></textarea></p>
<p><input class="span12" placeholder="your email address" name="email" /></p>
<p><input class="span12" id="submit_contact" class="btn" name="submit" type="submit" value="submit" /></p>
<input style="display:none;" name="not" type="text" />
</form>

</div>

</div>



Original Title: parts-tracking-database
Original Author: malcolm
Created: 2012-09-05 1707
Last Modified: 2013-02-26 1148
