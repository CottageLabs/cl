# Managing CL domain name settings

Our CL domains are handled via Godaddy - any domain names or SSL certificates or similar services that are required for a CL project and that should continue to be paid via the CL bank account should be purchased via Godaddy.

To get access to this, ask the CL sysadmin team.


## Domain names

cottagelabs.com points to our main production server where our website and etherpads run. This server should only be used for central CL stuff that we require to run our own business - NOT for running client services. Any subdomains of cottagelabs.com automatically forward to this server too, until an alternative DNS setting is registered for them.

test.cottagelabs.com targets our main test server - note that this test server is not actually a provision by CL but is paid for by Mark or by projects he allocates to it. Any subdomain of test.cottagelabs.com automatically forward to this server.


## Pointing subdomains

If you want to run a service at a CL subdomain you should edit the DNS zone file for cottagelabs.com. Create an A record that points the subdomain to the server you want to run the service on.

Note however that if you are just running a temporary service on the test server and you just want to make a simple domain name for it, you can configure nginx directly on the test server to use a thing.test.cottagelabs.com subdomain without having to mess with the settings.

Also if you are setting up a service on the main CL production server (which should of course be a CL internal service, NOT a client service) then you can configure nginx to capture anything under cottagelabs.com anyway, without bothering to alter the DNS settings.


## Pointing other domains

If you need to buy a domain name to point at a service you are running, you can buy it via the CL Godaddy account. NOTE that you must take account of this cost via the CL accounting processes, and ensure money is available to cover this cost, and add it to the sysadmin ongoing costs spreadsheet.


## SSL certificates

We have one multi-domain SSL certificate so far. Others can be purchased via the CL godaddy account and used as necessary to secure https access to services that require it. Nginx can easily be configured to use these certificates. Ask sysadmin team for help if necessary.





Original Title: Manage CL domains
Original Author: mark
Tags: howto
Created: 2013-09-01 1949
Last Modified: 2013-09-01 1957
