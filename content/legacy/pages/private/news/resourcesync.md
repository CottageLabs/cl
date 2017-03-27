# ResourceSync
<br>

It may surprise you to know that for the wealth and breadth of technology on the internet, there is no formal process for synchronising web content between two systems.  Certainly that technology has existed on the desktop for years, with utilities like <a href="http://en.wikipedia.org/wiki/Rsync">rsync</a> and other backup technology like <a href="http://en.wikipedia.org/wiki/Time_Machine_(Mac_OS)">Apple's Time Machine for OS X</a>; but no equivalent techniques exist for resources that are on the web.

Enter <a href="http://cottagelabs.com/projects/resourcesync/" title="ResourceSync">ResourceSync</a>.

In the last few months we've been excited to be involved in this project which is joint funded by the <a href="http://www.sloan.org/">Sloan foundation</a> in the US and the <a href="http://www.jisc.ac.uk/">JISC</a> in the UK, and is led by the folks who brought you <a href="http://www.openarchives.org/pmh/">OAI-PMH</a>, <a href="http://www.openarchives.org/ore/">OAI-ORE</a> and <a href="http://mementoweb.org/">Memento</a> to name just a couple of things: <a href="http://public.lanl.gov/herbertv/home/">Herbert van de Sompel</a>'s team at the <a href="http://lanl.gov/">Los Alamos National Laboratory</a> and <a href="http://www.cs.cornell.edu/lagoze/">Carl Lagoze</a>'s team at <a href="http://www.cornell.edu/">Cornell</a>.  It is being coordinated by <a href="http://www.niso.org/home/">NISO</a>, a standards body who produce the standards numbered z39.xx (you might know, for example, <a href="http://www.niso.org/standards/resources/Z39.50_Resources">z39.50</a>?), so ResourceSync should become z39.99 in the fullness of time!

The problem at the core of the ResourceSync effort is that there are services on the web which provide resources for its end-users, but there is no clean way for another service to discover all of those resources and create an always up-to-date mirror of them.  Sure, you can trawl a site and find all the resources and take copies of them, but:

<ol>
<li>are you really going to do that continuously just to monitor for when resources change?</li>
<li>how can you be absolutely sure that you've got all the resources?  What about those that aren't linked?</li>
<li>what about sources of non-traditional web content, like data archives, repositories, etc, which can't necessarily be crawled like a website at all</li>
</ol>

We have got involved in this project through JISC and via the <a href="http://cottagelabs.com/projects/sword2/" title="SWORD 2.0">SWORDv2</a> project.  SWORDv2 is a deposit protocol based on <a href="http://atompub.org/">AtomPub</a> which provides ways for scholarly content to be deposited between client and server environments.  In the repository world where SWORDv2 originated, ResourceSync looks like it might provide the discovery and dissemination pieces where SWORDv2 has provided the deposit pieces, so there's a natural synergy between the two (even if the technology is totally separate).

There's a lot going on in the project; Cornell have been working on <a href="https://github.com/resync/simulator">software which simulates change events</a>, some initial internal drafts of the proposed standard have been made, and we have been working on a detailed set of use cases to define the scope of the work.  The aim is to have a draft/beta version of the standard out soon after the summer.

The basic model that we are working to is a 3 tier synchronisation process:

<ol>
<li><strong>Initial synchronisation</strong> - some kind of data dump which will allow any system to synchronise all of the content from the source, to become equivalent to it at the current time.</li>

<li><strong>Incremental synchronisation via change communication</strong> - be to able to listen for changes to the resources in the source, and thus keep up-to-date via incremental updates.</li>

<li><strong>Audit</strong>- a mechanism where one system can confirm that it is up-to-date with another at any given point.</li>
</ol>

The exact way in which this will happen is still uncertain, although <a href="http://en.wikipedia.org/wiki/Sitemaps">Sitemap</a> is looking like a good technology to bootstrap off.  We are also interested in the model of the incremental synchronisation, to ensure that it is efficient and reliable; this may be through some Pub-Sub-Hub like notification mechanism or some form of persistent HTTP or XMPP connection.  Also, the synchronisation itself is not required to be HTTP, although that is a likely candidate, but could fall back to FTP, BitTorrent, etc.

So, watch this space, and there will be more coming from this project very soon.



Original Title: ResourceSync
Original Author: richard
Tags: atom, cornell, featured, jisc, lanl, niso, resourcesync, richard, sloanfoundation, swordv2, news
Created: 2012-07-05 1413
Last Modified: 2013-09-22 1652
