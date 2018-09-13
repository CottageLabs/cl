# Edinburgh International Science Festival
<br>

The [Edinburgh International Science Festival](http://sciencefestival.co.uk) is on now, 9th April to 22nd April. It has a nice website with lots of pictures, but seems a bit difficult to use (based solely on anecdotal evidence - don't get annoyed with me!)

My wife tried yesterday to search for some events, but found oddities such as not being able to filter for certain values, and sometimes getting pages back with [no times listed](http://www.sciencefestival.co.uk/whats-on/categories/talk/cystic-fibrosis-better-understanding-better-lives). What could I do to solve this, I thought?

Turns out, the [people that made the festival website](http://www.line.uk.com) are also [running an event](http://www.sciencefestival.co.uk/news/cutting-edge/calling-all-digital-creatives) as part of the festival, and it is supposed to be about doing cool visualisations with data. There are some [data collections and a brief](http://www.line.uk.com/underthehood/) of the event. Great! I could get the raw data and do something with it!

Unfortunately, the raw data has many errors, and is not very uniform. So it has taken me longer to do something useful with it than planned. The brief also has some amusing spelling errors in it! (The data also comes in .xls format, by the way...). Still, any open data is better than closed data - and with access to such open data, we could solve these errors and make the data admin process much less laborious. I should probably have used [Google Refine](http://code.google.com/p/google-refine/) to help me, but I was already wading through it before I really thought about that.

After spending a lot of time cleaning data, and a little time trying to do something sensible with it, I have built a tool to find out about the events that are on. It is plain and simple, in contrast with the original site.

After filtering, further details about an event are available by selecting the "more" option. This also has the nice feature of searching [Bibliographica](http://bnb.bibliographica.org) for relevant titles and listing them; in some cases, this gives a nice relevant reading list for each event, and can give a bit of insight into what the event might be like. In other cases, not much of use can be found.

[Festivals Lab have put up some APIs](http://projects.festivalslab.com/eisf/) onto this and other festival datasets - the data there is tidier than the stuff available from Line, although still not perfect - it appears to be a closer match to what is on the main site though. I may well grab a copy of the data from their API and update with that instead, but it does not include Venue maps or LatLongs, which I have already added (update - it will soon, cos I sent them the LatLongs).

I would quite like to do something with latlongs and [processing](http://processing.org/).

Of course, I have no control over buying tickets or anything like that; I have added a link from each event back to the official site search, and from there you are on your own...

I have done no browser checking or validation - I suggest running it in Firefox, it should be fine.

(not available any more...)



Original Title: Edinburgh International Science Festival
Original Author: mark
Tags: indexing, mark, news, search
Created: 2011-04-10 1941
Last Modified: 2012-12-07 0032
