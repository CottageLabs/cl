#From Directory to Course Data

The main directory of XCRI feeds is The XCRI Directory ([http://xxp.igsl.co.uk/app/xcridirectory](http://xxp.igsl.co.uk/app/xcridirectory)).  Within the directory there are 67 registered endpoints, and we want to be able to extract the XCRI data from each one.

There are a number of challenges that we need to overcome in order to do this:

1. The XCRI directory doesn't provide an API, so if we want to extract all of the endpoint technical information we either need to do it manually, or scrape the web pages for the information
2. The XCRI directory doesn't contain enough technical information for us to obtain the course data from the SOAP endpoints without manually exploring them
3. Not all of the listed endpoints are operational, or straightforward to interact with

This post introduces [the software](https://github.com/CottageLabs/xcri) and processes that we've used to address these challenges and obtain a substantial amount of course data.

## Scraping the Directory

To obtain a list of all the records in the directory, we must first scrape the directory home page.  We can do this in two stages:

First we scrape all the records on the [http://xxp.igsl.co.uk/app/xcridirectory](http://xxp.igsl.co.uk/app/xcridirectory) page.  As a user in a web browser this page only presents 10 records at a time, but this is a javascript feature, and requesting the raw HTML from the URL gives you all of the records in one document.  From this we can extract an initial listing of the entries in the directory, with the following data:

* The URL of the directory page dedicated to that endpoint
* The version of XCRI supported
* The name of the endpoint

For example, we can extract the record for Tennyson High School, and make a [JSON](http://www.json.org/) object that represents it:

    {
        "url": "http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046", 
        "version": "1.1", 
        "name": "Tennyson High School (14-19)"
    }

Now we scrape more data from the individual record pages (under the "url" parameter).  We will look at each individual record, and produce an augmented record which contains almost enough detail to move on to extract the XCRI data itself.  This allows us to obtain the additional data:

* The website describing the endpoint
* The WSDL or REST web-service URL
* The type of endpoint (SOAP or REST)

So, our Tennyson High School example above becomes:

    {
        "website": "http://www.xxp.org/getlincscourses.html", 
        "name": "Tennyson High School (14-19)", 
        "url": "http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046", 
        "wsdl_url": "http://host.igsl.co.uk:7101/Lincs-webservice-context-root/xxpSoapHttpPort?WSDL", 
        "version": "1.1", 
        "type": "SOAP"
    }

This is everything that we can get automatically from the directory.  For REST web services, this is enough, but the SOAP web services need a bit more information.  Each web service has an operation that needs to be invoked (it might be called, for example **getCourses**), and each operation may need to take a parameter or argument to be properly invoked (for example, an organisation's [UKPRN](http://www.thedataservice.org.uk/datadictionary/glossary/ukprn0809.htm)).  That means that in order to go any further we need to get these details manually ...

##Manually adding endpoint information

We still need to populate some "arguments" and "operation" parameters correctly so that we can successfully interrogate each SOAP endpoint.  This is where we need some manual intervention.  Each record that we have scraped has a couple of useful bits of information to help us: the website, and the url of the directory page for that endpoint.  Let's consider Tennyson High School as an example; first let's look at the two pages that we have links to:

<div class="row-fluid">
<div class="span6">
<a href="http://cottagelabs.com/media/getlincscourses.png"><img src="http://cottagelabs.com/media/getlincscourses.png" class="img thumbnail"></a>
<a href="http://www.xxp.org/getlincscourses.html">http://www.xxp.org/getlincscourses.html</a>
</div>
<div class="span6">
<a href="http://cottagelabs.com/media/tennysonhighschool.png"><img src="http://cottagelabs.com/media/tennysonhighschool.png" class="img thumbnail"></a>
<a href="http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046">http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046</a>
</div>
</div>
<br>

In the first screen shot we can see that the web service is called **getLincsCourses**, and beneath it a list of UKPRN Codes for each of the colleges or schools that are supported by that service.  We can find Tennyson High School in this list if we scroll down, and we can also find this information in the XCRI directory page: *"The SOAP call accepts a single parameter specifying the UKPRN of the provider, in this case 10017033."*  Between them they give us enough information to finish populating the record for this endpoint:

    {
        "website": "http://www.xxp.org/getlincscourses.html", 
        "name": "Tennyson High School (14-19)", 
        "url": "http://xxp.igsl.co.uk/app/xcriinfo?fed_id=1046", 
        "wsdl_url": "http://host.igsl.co.uk:7101/Lincs-webservice-context-root/xxpSoapHttpPort?WSDL", 
        "version": "1.1", 
        "arguments": ["10017033"], 
        "operation": "getLincsCourses", 
        "type": "SOAP"
    }

We must go through each SOAP endpoint in this way, and add the arguments (if they are necessary) and the web service operation that we need to invoke, then we can move on to extracting the course data.


##Course Data Extraction

We now have a set of records that we scraped from the [XCRI Directory](http://xxp.igsl.co.uk/app/xcridirectory), and augmented with manual processes, for both REST and SOAP web services.  Now we can can pull down the course data from each type of endpoint, as follows:

<div class="row-fluid">

<div class="span6" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<h3>REST</h3>
Request the "resource_url", and save the output directly.  This is plain XCRI course data.
</div>

<div class="span6" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<h3>SOAP</h3>
Request the "wsdl_url", and use that to determine the URL of the web service (e.g. getLincsCourses), then pass the arguments to that web service in a SOAP wrapper, and get back the XCRI XML response.  We do this using a SOAP client software library to simplify this.
</div>

</div>
<br>

In the process of acquiring data from the endpoints, we pick up the following errors:

<div class="row-fluid">

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>8</h1></div><div class="span9">Have no URL in the directory</div></div>
</div>

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>6</h1></div><div class="span9">Return an error, an HTML page, or no data</div></div>
</div>

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>5</h1></div><div class="span9">Respond with <em>415 Unsupported Media Type</em></div></div>
</div>

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>3</h1></div><div class="span9">Return XCRI data but in incorrectly formatted XML</div></div>
</div>

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>1</h1></div><div class="span9">Unable to locate a list of valid UKPRNs to use against the web service</div></div>
</div>

<div class="span2" style="border: 1px solid #bbbbbb; background: #dddddd; padding: 10px">
<div class="row-fluid"><div class="span3"><h1>1</h1></div><div class="span9">Has a response document structure too complex for automated analysis</div></div>
</div>

</div>
<br>

Once we have remove the erroneous records, and manually fixed the XML where possible we can run the software over all of the remaining sources, which gives us:

<div class="hero-unit">
<h1>7605</h1>
XCRI formatted course data records upon which we can build our course data demonstrator
</div>


## Invoking the code

For developers, here is a quick-start on how to invoke the code, but you'll find full documentation over on the [github page for the software](https://github.com/CottageLabs/xcri)

Scrape the directory home page for all the endpoints:

    python scraper.py directory <directory scraper output file>

Augment the information obtained from the directory page, by scraping the individual record pages:

    python scraper.py sources <directory scraper output file> <output file>

Your outuput file now contains as much information as we can obtain from the directory.

Before moving on to the next step, you must manually add the details required for extracting data from the SOAP endpoints, before moving on to obtain the data itself.

Finally, then, to obtain the data, invoke the obtain.py script:

    python obtain.py -s <sources json file> -o <output dir>




Original Title: From Directory to Course Data
Original Author: richard
Tags: xcri, richard, course data, soap, rest, web services, news
Created: 2012-12-14 1402
Last Modified: 2013-03-02 1809
