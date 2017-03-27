CL has various servers and domain names pointed at them, managed by the Sysadmin project. Mark is currently the Sysadmin project leader.

If something is wrong with one of our servers, contact the CL Sysadmin team.

# Sysadmin team contact

sysadmin@cottagelabs.com . You'll see a lot of "contact the sysadmin team" on this page.


# Preferences

Our preferred OS is Ubuntu, version 14.04 LTS. Recommend sticking with LTS (long-term support) versions until a new one comes out.

Our preferred web server is nginx, our preferred index is elasticsearch. Preferred python application server is gunicorn.


# Domain pointing

If you need a domain name - or subdomain - pointed, ask the Sysadmin team. Anything under .cottagelabs.com goes to our production server by default, then particular subdomains can be routed to the dev server - e.g. test.cottagelabs.com and *.test.cottagelabs.com go there.

# Access

Access is by public key authentication. Talk to the sysadmin team if you need access to one of our servers. You are unlikely to get access to the production server if you are not in the sysadmin team. 

Anyone can get access to dev servers upon request and proof of competence. You have to pass a very hard test... stage one of which is knowing how to make a public key.


# Production servers

We have multiple production servers. Our provider of choice is [Digital Ocean](http://digitalocean.com). Contact the sysadmin team if you would like a new development or production server.

Below is a diagram of what services and software we use to:
    a/ get servers
    b/ send email and do other things from our applications
    c/ run our apps on our servers
    
<img src="https://docs.google.com/a/cottagelabs.com/drawings/d/1M6sqghwISzBFkxxN7vFsLTylbhvQIr_bjiaI1c9ejII/pub?w=960&amp;h=769">



# Alternatives

We have an Amazon AWS account but it is expensive to run machines long term - use it for short bursts or where you need a lot of power quick. Otherwise use the machines above. We currently have nothing running on Amazon though.

We have a heroku account - just sign up and you can run small things for free. Ownership can be transferred to CL if necessary. We currently have nothing running on Heroku though.





Original Title: Manage CL servers
Original Author: mark
Tags: howto, server, sysadmin
Created: 2013-03-05 1812
Last Modified: 2014-08-12 1211
