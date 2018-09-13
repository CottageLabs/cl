# Elasticsearch Questions, Answers and Tips

##PROBLEM: loading objects into the index sometimes fails and sometimes succeeds.  If the error is reproducible with the objects in the same order, the problem could be:

### Possible causes

* an index mapping mis-match; some objects have different datatypes in the same field, so the later ones which don't match get ignored

* this is often caused by date fields. If your data contains dates, elasticsearch will guess that e.g. the "created_date" field contains a date value. Then along comes a record with an improperly formatted date (or one that ES does not understand by default). It fails the mapping and is thus not accepted into the index.

### Dealing with it

1. Look at what the error is. The logs will have details. The logs will be in /var/log/elasticsearch if you have installed it properly from the .deb file, or in your ES install directory if you just unzipped it.
* the logs may not have anything about index mapping problems
1. If you're using the Bulk API and can't find the errors, stop using the Bulk API - send the records in 1-by1. That way, you will have the opportunity to get the errors from the responses ES gives you.


##PROBLEM: loading a lot of data into ES (while also, optionally, querying it) causes it do totally die

### Possible causes

- a memory issue perhaps?  It is probably related to the following problem (unaccounted for shard failure)

### Dealing with it

1. A restart seems to be the only way to recover.  This does not guarantee that the issue won't arise again.  To fix memory issues, see the next problem (unaccounted for shard failure)


##PROBLEM: unaccounted for shard failure.  In a search response, occasionally the total number of shards and the successful shards differ, but there are no failed shards

	{
		took: 3,
		timed_out: false,
		_shards: {
			total: 5,
			successful: 4,
			failed: 0
		}
		...
	}

### Possible causes

* There is insufficient memory on the machine
* There is insufficient memory allocated to the ES process,
* There are insufficient file descriptors allocated to the user ES runs as

### Dealing with it

You need to allocate more memory to ES, and to raise the number of file descriptors

The following steps are required (it also assumes that you have installed the ES service manager, which you can do from git clone git://github.com/elasticsearch/elasticsearch-servicewrapper.git)

vim config/elasticsearch.yml and uncomment bootstrap.mlockall: true
and uncomment cluster.name: elasticsearch (and change cluster name if necessary)
vim bin/service/elasticsearch.conf and set.default.ES_HEAP_SIZE=4096 or whatever value works for the machine
then vim /etc/security/limits.conf and put this in:

	root  hard  nofile  1024000
	root  soft  nofile  1024000
	root  hard  memlock unlimited
	root  soft  memlock unlimited
	* hard  nofile  1024000
	* soft  nofile  1024000
	* hard  memlock unlimited
	* soft  memlock unlimited

and then vim /etc/pam.d/common-session and /etc/pamd.d/common-session-noninteractive
and put the following in it:

	session required      pam_limits.so

Then you MUST log out and log back in as the user ES will run as, so that the file descriptor changes take effect






Original Title: Elasticsearch Q&A
Original Author: emanuil
Tags: elasticsearch
Created: 2013-12-05 1119
Last Modified: 2014-05-16 1253
