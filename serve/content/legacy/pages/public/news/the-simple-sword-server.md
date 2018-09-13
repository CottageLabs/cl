# The Simple Sword Server
<br>

The <a href="https://github.com/swordapp/Simple-Sword-Server">Simple Sword Server (SSS)</a> is a python implementation of the server-side responsibilities of the <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html">SWORDv2 specification</a> that we've been building throughout the <a href="http://cottagelabs.com/projects/sword2/" title="SWORD 2.0">SWORD2.0</a> and <a href="http://cottagelabs.com/projects/sword-2-plusplus/" title="SWORD 2++">SWORD2++</a> projects.  Its main purpose was initially to provide developers with a reference implementation server which they can use to develop clients against (like we did with the <a href="http://cottagelabs.com/projects/duo/" title="Duo">DUO project</a>).  But since then it has grown so that it is now a fully functional server library for providing SWORDv2 support.

So, you can talk to SSS as-is, as if it were a real server, and it will behave exactly as if it were one.  In fact, under-the-hood, it provides a very simple file-system repository, so it almost <em>is</em> a real server.  In this post we're going to talk mostly about its use as a development tool, but there's a bit more information further down about how to use it as a server library too.

<h3>API</h3>

The API provides the full range of features specified by SWORDv2.  Every object is given a <a href="http://en.wikipedia.org/wiki/Universally_unique_identifier">UUID</a> when it is created; both Collections and Items are identified in this way.  Items always live in a collection, so an Item's identifier is always 

    [collection uuid]/[item uuid]

The SSS URL space is very straightforward; each URL type is named in the same way as it is <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#terminology">named in the SWORDv2 specification</a>, so it's easy to compare the two, and Collection/Item identifiers are simply appended.  So we have:

<ul>
<li>Service document: /sd-uri</li>
<li>Collection: /col-uri/[collection uuid]</li>
<li>Repository Item (aka Container): /edit-uri/[collection uuid]/[item uuid]</li>
<li>Media Resource: /em-uri/[collection uuid]/[item uuid]</li>
<li>Media Resource Content: /cont-uri/[collection uuid]/[item uuid]</li>
<li>Statement: /state-uri/[collection uuid]/[item uuid]</li>
<li>Collection's Web Page: /html/[collection uuid]</li>
<li>Item's Web Page (aka Alternate): /html/[collection uuid]/[item uuid]</li>
</ul>

Notice as well that the last 2 URLs are for web pages.  This means that you can look at what a Collection or an Item looks like in the repository via a web browser; it's not pretty, but it IS useful!  Also, you can visit the base URL (e.g. http://localhost:8080), and you will get a nice home page for the repository.

<div class="row-fluid">
<div class="span4"></div>
<div class="span4">
<a href="http://cottagelabs.com/media/SSSHomePage.png"><img src="http://cottagelabs.com/media/SSSHomePage.png" alt="" title="SSSHomePage" class="img thumbnail span12" /></a>
</div>
</div>

The HTML interface also supports the <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#autodiscovery">auto-discovery features in Section 13 of the SWORDv2 spec</a>.

<h3>The Repository</h3>

When you start SSS, it will create a directory called "store" in your current working directory, and automatically create 10 Collections as directories (if there's already a store directory, it will just start itself up over that).  When you create Items via the API, the Item will be created in the Collection directory as a sub-directory; all the directories are named by their UUID.

So the main hierarchy looks like this:

    store
      |- Collection 1
      |- Collection 2
      \  Collection 3
              |- Item 1
              |- Item 2
              \  Item 3

When an item is created/updated, all of the resources which are relevant to the SWORDv2 API are created/updated.  That makes it extremely useful for developers who can create objects via the API and then investigate them via a file browser/text editor during development/debugging.  The structure of an Item looks like this:

    Item
      |- 2012-04-16T14:18:37Z_example.zip
      |- atom.xml
      |- sss_deposit-receipt.xml
      |- sss_metadata.xml
      |- sss_statement.xml
      \  sss_statement.atom.xml

The <strong>zip file</strong> is the package which was deposited (note that SSS doesn't bother to unpack it - it wouldn't know what to do with the content, after all); it is prefixed by the timestamp of when it was deposited (which avoids name clashes if you add more packages, and makes it easier for you to identify which package you just deposited).

The <strong>atom.xml</strong> file is the atom entry document which was deposited (at least, in cases where it was deposited in the first place - see the SWORDv2 spec for the various modes of deposit available).  SSS will extract any embedded <a href="http://www.dublincore.org/documents/dcmi-terms/">Dublin Core</a> into <strong>sss_metadata.xml</strong>.

The <strong>sss_deposit-receipt.xml</strong> is a transcript of the most recently returned <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#depositreceipt">Deposit Receipt</a>, while <strong>sss_statement.xml</strong> and <strong>sss_statement.atom.xml</strong> are the two different variations on the <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#statement">Statement</a> format (RDF/XML and Atom respectively).  These are prepared in advance of any request for them, and are updated each time an update to the item comes in.

You'll find that when you're working with the server, it's really convenient to be able to go and see what it's done with your content, and what the Statement and Deposit Receipt look like, without having to go through the API each time.  After all, you might not have written the bit to retrieve the Statement yet!

<h3>Configurability</h3>

SSS uses a novel approach to configuration.  It uses a file in the current working directory named <strong>sss.conf.json</strong>, which is an augmented JSON formatted file containing a configuration object.  If the file does not already exist at startup (which it won't when you first run SSS), it will be created.

The key difference between this JSON format and normal JSON is that this format allows line comments.  Any line prefixed with a # is automatically stripped prior to parsing as JSON, but the whitespace is preserved so that any errors with your JSON will still be flagged up on the correct line of the file.  So your file can look like:

    {
        # First config option
        "first" : "value",

        # Next config option
        "next" : "config"
    }

There are a large number of configuration options, and we won't look at all of them, but here are some highlights (go and have a look at the file yourself when you are using SSS - all the options are documented in-line - or take a look at the <a href="https://github.com/swordapp/Simple-Sword-Server/blob/master/sss/config.py">config.py source</a>).

<strong>num_collections</strong>: Defaults to 10; this is the number of collections that SSS will maintain automatically for you.  If there are fewer than 10 collections on start-up it will create the deficit (it doesn't delete collections if there is an excess, though, so it might help to think of this as a lower limit)

<strong>authenticate, user, password, mediation, obo</strong>: this set of options control authentication.  If <strong>authenticate</strong> is false, then all operations can be carried out without credentials.  If it is true, then a successful authentication would use the <strong>user</strong> and <strong>password</strong> specified here (this is not high security, as you might have noticed).  If <strong>mediation</strong> is set to false, then <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#authenticationmediateddeposit">On-Behalf-Of</a> deposits will cause an error, and if set to true On-Behalf-Of deposits will only be accepted from the user identified by <strong>obo</strong>.

<strong>app_accept</strong>: the list of mimetypes which are acceptable content types.  SSS does proper content negotiation (using <a href="http://pypi.python.org/pypi/negotiator/1.0.0">The Negotiator</a>) on GET requests and will only accept correct content types on deposit (PUT, POST).  You can also specify <strong>multipart_accept</strong>, or even specify <strong>accept_nothing</strong>.  All of these options will be reflected in the <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#protocoloperations_retreivingservicedocument">Service Document</a>.  If <strong>accept_nothing</strong> is specified, the Collection will not provide any information to the client regarding acceptable content types, which the client should take as a hint to not try to deposit anything.  This may be best used in concert with <strong>use_sub</strong>...

<strong>use_sub</strong>: Service Documents can nest.  SSS fakes this by allowing each Collection to contain every other Collection if this option is set to true.  There isn't a real collection hierarchy in SSS, this is just for show for the client.

Here's a snippet from the config file showing us setting up the acceptable content type to be anything (*/*), and telling the server to pretend like it has a hierarchy of Collections:

    # What media ranges should the app:accept element in the Service Document support
    "app_accept" : [ "*/*" ],
    "multipart_accept" : [ "*/*" ],
    "accept_nothing" : false,
    
    # should we provide sub-service urls
    "use_sub" : true,

<strong>package_ingesters</strong>: this is a dictionary of URIs identifying package formats with software implementations which understand that format which SSS should use if it sees a package for that format.  There is a <strong>sword_accept_package</strong> config option which tells the client what formats you accept, and this option then tells SSS what to do when it gets one of those formats.  In our case we provide a couple of basic ones, none of which do anything particularly interesting, but if the urge comes upon you to write something to unpack your particular zip file, you can do it and plug it in here.

Here's a basic config for the <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#iris">standard SWORDv2 package types</a>, and the SSS ingester plugins which handle them:

    "sword_accept_package" : [
            "http://purl.org/net/sword/package/SimpleZip",
            "http://purl.org/net/sword/package/Binary"
     ],

    "package_ingesters" : {
            "http://purl.org/net/sword/package/Binary" : 
                                 "sss.ingesters_disseminators.BinaryIngester",
            "http://purl.org/net/sword/package/SimpleZip" : 
                                 "sss.ingesters_disseminators.SimpleZipIngester"
    },

<strong>allow_update, allow_delete</strong>: real-world servers are at-liberty to refuse any of your SWORDv2 requests at any point if they choose, and these options allow you to simulate that in SSS.  You can turn off updates and deletes here, so repeat requests to carry out such operations will <a href="http://swordapp.github.com/SWORDv2-Profile/SWORDProfile.html#errordocuments">fail in the appropriate way</a>.

The other good thing about this config file is that it's arbitrarily extensible with your own JSON.  If you feel like writing a plugin for SSS you can enter the config here, and it will not interfere with any other config, and you can load it and use it as you like in your plugin.  

In fact, this is how SSS can be used as a server library - the repository back-end is simply a plugin, and can be replaced by any other back-end (such as your properly written, actually secure, server!); you can just update the configuration:

    "sword_server" : "sss.repository.SSS",
    "authenticator" : "sss.repository.SSSAuthenticator",

Which brings us nicely on to ...

<h3>SSS as a server library</h3>

After we'd been working on SSS as a reference implementation for a while, we got involved with the <a href="http://cottagelabs.com/projects/dataflow/" title="DataFlow">DataFlow project</a>, which uses SWORDv2 to transfer research data between its academic client environment (<a href="http://www.dataflow.ox.ac.uk/index.php/about/about-datastage">DataStage</a>) and its archiving system (<a href="http://www.dataflow.ox.ac.uk/index.php/about/about-databank">DataBank</a>).  The whole stack is written in python, so it made sense to bootstrap off the SSS application, so we set about converting it from just a reference implementation for developers into a well decoupled server library and repository implementation.

The server library part supports <a href="http://webpy.org/">web.py</a> and <a href="http://www.pylonsproject.org/">pylons</a>, and deals with receiving HTTP requests and turning them into an  object model which is passed to the repository implementation.  It then gets back response objects and serialises them back onto the wire for the client.  This saves a lot of work for the server developer, because lots of the fiddly things like handling HTTP headers, setting content types and other response parameters, as well as dealing with scalability issues, not to mention conformance to the spec are all dealt with by the library.

Once we did that, we could replace the standard SSS repository with an implementation which is integrated with DataBank.

If you are a python developer and you want to work with SWORDv2, SSS is a good place to start.  All you need to do is implement the repository interface defined in the <a href="https://github.com/swordapp/Simple-Sword-Server/blob/48cded9832434a7e2f962680c6820174bd614497/sss/core.py#L10">SwordServer</a> class and plug it in in the configuration file, and away you go!

<h3>Where next?</h3>

First you need to check out the <a href="https://github.com/swordapp">swordapp github page</a>, which has all the software that's been produced by the project and other SWORDv2 related projects.

The three client libraries we have worked on (The <a href="https://github.com/swordapp/python-client-sword2">Python Client</a>, the <a href="https://github.com/swordapp/JavaClient2.0">Java Client</a> and the <a href="https://github.com/swordapp/sword2ruby">Ruby Client</a>) were both developed and tested against the Simple Sword Server, so if you are looking to build a client environment or test your own server environment, they are a good place to begin.


<h3>Installation</h3>

Ok, to finish up, here are some details on installation.  You can stop reading now if you aren't trying to install SSS...

Running the Simple Sword Server is really easy.  It depends on web.py and lxml, so you need to install them with something like

    sudo easy_install web.py
    sudo easy_install lxml

Then you can check SSS out with 

    git clone git://github.com/swordapp/Simple-Sword-Server.git

There's no need to actually install the application, you can just:

    cd Simple-Sword-Server/sss
    python webpy.py

This will bring up SSS at

    http://localhost:8080/



Original Title: The Simple Sword Server
Original Author: richard
Tags: dataflow, deposit, duo, opensource, python, repositories, richard, sss, swordv2, news
Created: 2012-06-07 1152
Last Modified: 2013-03-02 1909
