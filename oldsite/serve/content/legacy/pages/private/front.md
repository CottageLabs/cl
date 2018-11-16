
<div class="container" id ="blurb">
<div class="content">

<div class="row-fluid">

<div class="span4">

<h2>Hi!</h2>

<p><a href="#us">We are Cottage Labs</a>. We love doing projects with people to <a href="">collaboratively develop</a> and run software systems that support and enhance business and community practices.</p>

<div class="well" style="background-color:#333;">

<h2><a href="" style="color:#c9d2d4;">Find out more about who we are and who we work with</a></h2>

</div>

</div>

<div class="span4">

<h2>DEV</h2>

<p>Most of our work is on open source <a href="/software">software</a> development <a href="/projects">projects</a>, and it's usually <a href="#who">for research and higher education</a> organisations or communities ( but not always :)</p>

</div>

<div class="span4" style="background-color:#c9d2d4;">

<h2>OPS</h2>

<p>We also <a href="/operations/ours">run services</a>, usually for scholarly communities, and typically using code that we write (or contribute to) ourselves. But we do <a href="/operations/service">provide services</a> for <a href="/operations">other groups</a> too.</p>

</div>

</div>

</div>
</div>



<div id="logos" style="width:700px;">

<div class="clearfix">
<a style="float:left;max-width:200px;max-height:80px;" class="img thumbnail" href="/customers?q=jisc"><img src="http://cottagelabs.com/media/jisc-logo.jpg" style="height:55px;"></a>
<a style="float:left;max-width:200px;max-height:55px;" class="img thumbnail" href="/customers?q=universityofoxford"><img src="http://cottagelabs.com/media/oxford.gif" style="height:55px;"></a>
<img class="img thumbnail" src="http://cottagelabs.com/media/cambridge.jpg" style="float:left;max-width:200px;height:55px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/duo2.jpg" style="float:left;max-width:200px;height:55px;">
</div>

<div class="clearfix">
<img class="img thumbnail" src="http://cottagelabs.com/media/plos.jpg" style="float:left;max-width:260px;height:69px;">
<a style="float:left;height:69px;" class="img thumbnail" href="/customers?q=lanl"><img src="http://cottagelabs.com/media/LANL_logo.png" style="height:69px;"></a>
<img class="img thumbnail" src="http://cottagelabs.com/media/Cornell_logo.jpg" style="float:left;max-width:250px;height:69px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/Exeter_logo1.jpg" style="float:left;max-width:250px;height:69px;">
</div>

<div class="clearfix">
<img class="img thumbnail" src="/media/brunel.png" style="float:left;width:150px;max-height:55px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/mimas-logo-medium-300x59.gif" style="float:left;max-width:210px;height:55px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/okf.png" style="float:left;width:57px;height:55px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/lyrasislogo.jpg" style="float:left;width:200px;max-height:55px;">
</div>
                
<div class="clearfix">
<img class="img thumbnail" src="http://cottagelabs.com/media/KCL_box_red_pin_rgb.jpg" style="float:left;max-width:200px;max-height:69px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/NISO_LOGO-RGB-600dpi.jpeg" style="float:left;width:155px;height:69px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/British_Library1.jpg" style="float:left;width:40px;max-height:69px;">
<img class="img thumbnail" src="http://cottagelabs.com/media/webtitlelogo.png" style="float:left;width:240px;height:69px;">
<a style="float:left;width:70px;height:69px;" class="img thumbnail" href="/customers?q=universityofedinburgh"><img src="/media/edinburgh.png"></a>
</div>

</div>












<link href='http://fonts.googleapis.com/css?family=Roboto+Slab' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Special+Elite' rel='stylesheet' type='text/css'>

<style>
html, body{
    font-family:'Roboto Slab', serif;
    font-family: 'Special Elite', cursive;
    font-size:1em;
}
#topstrap {
    background-color: none;
    border-bottom:10px solid #333;
    margin: 0;
    background-image:url(/static/cottageblur.png);
    background-repeat:no-repeat;
    background-position:bottom;
    height:85px;
}
#blurb .content p{
    font-family: 'Special Elite', cursive;
}
</style>


<script type="text/javascript">
jQuery(document).ready(function () {

    $('#mainnav').insertAfter( $('#topstrap > .container') );
    $('#blurb').insertAfter( $('#mainnav') );
    
    // widen the topstrap for intro page
    var ht = $(window).height() - 10;
    $('#topstrap').css({'height':ht + 'px'});

    $('body').prepend('<div id="navbuttons" style="position:fixed;top:0;right:0;padding:5px;background-color:#c9d2d4;"><p style="font-size:0.8em;padding:0;margin:0;">CL | <span class="icon icon-list"></span> <span class="icon icon-cog"></span> <span class="icon icon-user"></span> <span class="icon icon-search"></span></p></div>')

    // animate anchor clicks
    var infomator = function(event) {
        event.preventDefault();
        if ( $(this).attr('href') == '#datavis' ) {
            $('#datavis').show();
            dograph();
        }
        $('body, html').animate({
            'scrollTop': $('[name="' + $(this).attr('href').replace('#','') + '"]').offset().top
        }, 700);
    }
    $('.infomator').bind('click',infomator);
    if ( window.location.hash == '#datavis' ) {
        $('#showdatavis').trigger('click');
    }

});
</script>



Original Title: untitled
Original Author: mark
Created: 2014-05-04 1731
Last Modified: 2014-05-06 1837
