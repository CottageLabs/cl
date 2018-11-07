#Experiences Extracting XCRI
<br>

In a [previous post](http://cottagelabs.com/news/seeking-xcri) we explored the web for XCRI resources.  From that investigation, the most useful thing that we found was [the XCRI directory](http://xxp.igsl.co.uk/app/xcridirectory), which lists 65 course data feeds.  The types of feed break down thus:

<div class="row-fluid">

<div class="span1"></div>

<div class="span3">
<div class="hero-unit">
<h1>40</h1>
SOAP web services
</div>
</div>

<div class="span3">
<div class="hero-unit">
<h1>8</h1>
Demo feeds
</div>
</div>

<div class="span3">
<div class="hero-unit">
<h1>17</h1>
HTTP/REST web services
</div>
</div>

</div>

We will ignore the demo feeds, and the HTTP/REST feeds are easy enough to access at their base URLs, with an ordinary HTTP request (e.g. from your web browser).  In this post we will focus on our experiences with the SOAP endpoints, to get an understanding of the challenges involved in constently harvesting data from them.

##Discovering the endpoints

Whether it is HTTP/REST or SOAP, the XCRI directory has some significant limitations in terms of accessing its listing.  There is a web user interface, but no machine readable API.  In order to extract the URLS from which the feeds can be obtained, it is necessary to manually click-through from the directory listing to a feed-specific page, to obtain the endpoint URL.  For example, [Wolds College](http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1048)

<div class="row-fluid">
<div class="span3"></div>
<div class="span6">
<img src="http://cottagelabs.com/media/xcri-directory-record.png"/>
</div>
</div>

As you can see from that page, we can then manually extract the following useful information:

* **Data Link**: [http://host.igsl.co.uk:7101/Lincs-webservice-context-root/xxpSoapHttpPort?WSDL](http://host.igsl.co.uk:7101/Lincs-webservice-context-root/xxpSoapHttpPort?WSDL)
* **A related website**: [http://www.xxp.org/getlincscourses.html](http://www.xxp.org/getlincscourses.html)
* **A description of the service**: The SOAP call accepts a single parameter specifying the UKPRN of the provider, in this case 10022722.

This is a painstaking way of obtaining the information, and as the directory grows the problem will become compounded.

##How to use the endpoints

One of the most significant issues for rapidly integrating the XCRI feeds is the heterogeneity in implementation of the SOAP APIs.  For example, let us consider two different organisations:

<div class="row-fluid">

<div class="span6" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<h3>The Open University</h3>
<p><strong>URL</strong>: <a href="http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1013">http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1013</a></p>
<p>"An enhanced version of the native Open University feed that includes additional meta data (specific coding schemes, classifications and controlled text fields) for the National Learning Directory and other third party data aggregators"</p>
<p><strong>SOAP service definition</strong>:</p>
<pre>
Service ( xxp ) tns="http://uk.co.igsl.asap/"
   Prefixes (1)
      ns0 = "http://uk.co.igsl.asap/"
   Ports (1):
      (xxpSoapHttpPort)
         Methods (1):
            getOUCourses(xs:string arg0, )
         Types (2):
            getOUCourses
            getOUCoursesResponse
</pre>

<p>As you can see, the <strong>getOUCourses</strong> method takes one argument, although there is no immediately available documentation as to what the argument is.  If we follow the link in the directory to the <a href="http://www.xxp.org/getoucourses.html">associated website</a> we find that we can pass in the arguments "ALL", "PG", or "UG".</p>

<p>Once we do that, we are presented with a full list of the related course data records.</p>

</div>

<div class="span6" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">

<h3>Tennyson High School</h3>
<p><strong>URL</strong>: <a href="http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046">http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046</a></p>
<p>"14-19 course feed (dormant)
The SOAP call accepts a single parameter specifying the UKPRN of the provider, in this case 10017033."</p>
<p><strong>SOAP service definition</strong>:</p>
<pre>
Service ( xxp ) tns="http://uk.co.igsl.asap/"
   Prefixes (1)
      ns0 = "http://uk.co.igsl.asap/"
   Ports (1):
      (xxpSoapHttpPort)
         Methods (1):
            getLincsCourses(xs:string arg0, )
         Types (2):
            getLincsCourses
            getLincsCoursesResponse
</pre>

<p>As you can see the <strong>getLincsCourses</strong> method takes one argument, and the description in this case tells us what that argument should be (10017033).  If we follow the link in the directory to the <a href="http://www.xxp.org/getlincscourses.html">associated website</a>, we see that the Lincolnshire Teenage Services SOAP endpoint covers a number of schools and FE colleges, and we can get the codes to pass to <strong>getLincsCourses</strong> from there.</p>

</div>

</div>

<br><br>

##Endpoint Comparisons

There are a number of striking things which affect the ease by which these services can be integrated into, for example, an aggregator:

1. Each service has a different SOAP method to be invoked to get the data.  The Open University uses **getOUCourses**, and Lincolnshire Teenage Services uses **getLincsCourses**.

2. Each service takes different arguments to its SOAP method in order to get the data.  The Open University uses **ALL**, **UG** or **PG**, and Lincolnshire Teenage Services uses college identifiers (there is no equivalent to an ALL)

3. Each service is documented differently

Together, these make a standardised approach to harvesting data from the services basically impossible, and therefore each service will need to be incorporated in its own custom way.  There would be a significant advantage in standardising to some degree the SOAP methods to be used.  Or better still to abandon SOAP altogether and insist on a REST API.

We are currently working on software which will ease the process of integrating XCRI sources from both SOAP and REST endpoints, and a future blog post will discuss that work.





Original Title: Experiences Extracting XCRI
Original Author: richard
Tags: xcri, soap, rest, richard
Created: 2012-11-26 2151
Last Modified: 2013-03-30 0957
