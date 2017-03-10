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
            <h1><br>XCRI Lightning</h1>
        </div>
    </div>

    <div class="span6">
        <p style="font-size:1.6em;">Over the last few months we have been experimenting with XCRI-CAP course feed demonstrators, to find out 
        what sorts of thing can be achieved with them as they currently stand, from the perspective of someone external 
        to a provider organisation and external to other XCRI feed development projects.</p>
        <p style="font-size:1.6em;">This is a short review of how we have done so far.</p>
        <p style="font-size:1.6em;"><a id="enableslideshow" class="btn" href="">experimental - view as slideshow</a></p>
        <h3>Mark MacGillivray, Richard Jones. Cottage Labs</h3>
        <p style="font-size:1.6em;">Project page - <a href="http://cottagelabs.com/projects/xcri">http://cottagelabs.com/projects/xcri</a></p>
    </div>

</div>


<hr></hr>


<div class="step row-fluid" data-x="1000">
    <div class="span12">
        <h2>Our experiences</h2>
        <p>
        <ul style="font-size:1.6em;">
        <li style="padding-bottom:15px;">Looked for a spec and a place where we could extract data from<br>
        More details of this at <a href="http://cottagelabs.com/news/seeking-xcri">Seeking XCRI</a></li>
        <li style="padding-bottom:15px;">We had a look to see what sorts of feeds we could access<br>
        More details of this at <a href="http://cottagelabs.com/news/experiences-extracting-xcri">Experiences Extracting XCRI</a></li>
        <li style="padding-bottom:15px;">Next, we had a look at what we had managed to collect. In total we got 7605 course records after overcoming a few issues.<br>
        More details of this at <a href="http://cottagelabs.com/news/from-directory-to-course-data">From directory to course data</a></li>
        <li style="padding-bottom:15px;">Next step was to convert the XCRI into a format we would easily use on the web - XCRI-CAP JSON.<br>
        More details of this at <a href="http://cottagelabs.com/news/xcri-cap-json">XCRI-CAP JSON</a></li>
        <li style="padding-bottom:15px;">Then we combined up our aggregation scripts with some code to produce data conformant to our desired XCRI-CAP JSON structure.<br>
        More details of this at <a href="http://cottagelabs.com/news/xcri-xml-to-json">XCRI XML to JSON</a></li>
        <li style="padding-bottom:15px;">Finally we ran the whole pipeline and got an aggregate collection of records together from the various 
        endpoints we were able to hit - with a few issues.<br>
        More details of this at <a href="http://cottagelabs.com/news/xcri-in-the-wild">XCRI in the wild</a></li>
        </ul>
        </p>
    </div>
</div>


<hr></hr>


<hr></hr>


<div class="step row-fluid" data-x="2000">
    <div class="span12">

        <p style="font-size:1.6em;">Our demonstrator-so-far is here: <a href="http://test.cottagelabs.com/xcri">http://test.cottagelabs.com/xcri</a></p>
        <p style="font-size:1.6em;">The code is all available here: <a href="http://github.com/cottagelabs/xcri">http://github.com/cottagelabs/xcri</a><br></p>

        <h2>What next - things we want to do</h2>
        <p style="font-size:1.6em;">We need more quality data sources - k-int? Direct? Who else has feeds we could pull now?</p>
        <p style="font-size:1.6em;">Combine with KIS data. Has anyone else finished this yet? Turns out the unistats API is borked.</p>
        <p style="font-size:1.6em;">Demonstrate an embedded widget on a site beyond our control - anyone interested in being test subjects?</p>
        
        <h2><br>What next - things the XCRI project community must do</h2>
        <p style="font-size:1.6em;">Keep making more feeds available</p>
        <p style="font-size:1.6em;">Make the available feeds easier to find - where is the definitive listing, where can they be advertised?</p>
        <p style="font-size:1.6em;">Work together to agree how to better implement the spec.</p>
        <p style="font-size:1.6em;">Define a clear use case for the feeds in the context of aggregation, rather than trying to tell aggregators what to do</p>
    </div>
</div>





Original Title: XCRI Lightning Talk
Original Author: mark
Tags: xcri, news, mark, richard, presentation
Created: 2013-01-29 0823
Last Modified: 2013-03-02 1924
