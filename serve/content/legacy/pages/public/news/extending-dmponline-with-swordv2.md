# Extending DMPOnline with SWORDv2
<br>

<img src="http://cottagelabs.com/media/dmp_logo.png" alt="" title="dmp_logo" class="img thumbnail pull-right" />

Research funding bodies typically require researchers to implement data
management plans to safeguard the data and outputs of their research. The <a href="https://dmponline.dcc.ac.uk/">Data
Management Plan (DMP) Online</a> tool, developed by the <a href="http://www.dcc.ac.uk/">Digital Curation Centre</a> at
the <a href="http://www.ed.ac.uk/">University of Edinburgh</a>, is used by academics to do exactly this - define how they will manage the
data and outputs from their research.

Extending DMPOnline to communicate with institutional repositories using <a href="/projects/sword2">SWORDv2</a>, so
that data plans are archived and preserved, seemed a natural addition to the
functionality of this tool. With that aim, Cottage Labs attempted to integrate the
recently developed <a href="https://github.com/swordapp/sword2ruby">Sword2Ruby</a> library into the DMPOnline code base.

First of all, we forked the existing <a href="https://github.com/DigitalCurationCentre/DMPOnline">DMPOnline code</a>, so that we wouldn't break
anyone else's systems. Then once this was up and running locally (with the usual
Ruby/Gem installation palaver), we set about working out <a href="https://docs.google.com/document/d/1B_Zu_DL33Ddb44nk_xgdY1ZzlgtgVgLQ3Ovm3PIZzN0/edit">how the integration
would function</a> and what new buttons we might need. We realised that the
connection between DMPOnline and the Repository should be asynchronous,
to allow for servers going offline and networks going down. Thus a queue was
necessary: a request would be queued by DMPOnline, and then processed on a
regular schedule by a worker job. If the worker cannot process the request, e.g.
if the repository is offline, the request will get re-queued and tried again at the
next available opportunity.

Unfortunately, the asynchronous mechanism introduced additional complexities
- such as what happens when a plan is deleted from DMPOnline? How should
it be recorded in the queue if the associated plan record (storing the repository
identifiers) no longer exists? This problem was resolved by selectively caching
the repository URIs on which to perform the actions.

Some other issues cropped up because of the 'bleeding edge' nature of the
DMPOnline tool - for example, there is currently no facility to manage user
accounts, which makes the deployment of the system difficult.

Nevertheless, the integration is working well and we are looking to install the
system at a host university in the next couple of months.  You can see how it works with this handly video demo:

<iframe width="420" height="315" src="http://www.youtube.com/embed/O5FJlpTcqTM" frameborder="0" allowfullscreen></iframe>

The code for DMPOnline with Repository Integration is available from: <a href="https://github.com/CottageLabs/DMPOnline">
https://github.com/CottageLabs/DMPOnline</a>

Our project page for the project is <a href="/projects/oxforddmponline">here</a>


<em>Martyn Whitwell, Cottage Labs, August 2012</em>



Original Title: Extending DMPOnline with SWORDv2
Original Author: martyn
Tags: martyn, oxforddmponline, researchdatamanagement, dmp, dcc, videos, news, dmponline, swordv2
Created: 2012-08-05 1202
Last Modified: 2013-05-14 1932
