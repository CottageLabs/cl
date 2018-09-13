<div class="row-fluid">
    <div class="span12">
        <div class="hero-unit">
            <h1>Using portality</h1>
        </div>
    </div>
</div>

Portality is a python software repo, based on <a href="http://flask.pocoo.org">Flask</a>, that has a bunch of useful things in it. It assumes an elasticsearch backend. To use it, you should create a new repo then add portality as an upstream source and merge it.

<pre>
git remote add upstream https://github.com/CottageLabs/portality.git
git fetch upstream
git merge upstream/master
</pre>

Portality also contains some submodules, so to initiate them use:

<pre>
git submodule init
git submodule update
</pre>

In Portality you will find a default_settings.py. Where you want to overwrite some of the values in there, create a file called app.cfg in the top level directory (above where default_settings.py is) and put your overwrites in there.

There is also a web.py file which is the example app. To run it just do <code>python portality/web.py</code>. However you should not edit web.py - instead, copy and paste it into a file called, say, app.py and customise that instead.

You will see that web.py imports a number of different functionalities from the view/ folder. These can be included or excluded as required from your own app.py.

Also, the access layer to elasticsearch is defined in dao.py and then models that use that access method are specified in models.py. There are some examples in there, and you can add your own as required.

The various views also rely on particular includes in the /static folder, and also on templates available in the /templates folder. Again, various of these can be used as examples to start from and customised as required.

Some work should probably be done on Portality here to put these statics and templates into default_ folders, which can then be used in the child app as required.

I will try to soon add a description of each of the views currently available in portality.



Original Title: using portality
Original Author: mark
Tags: mark, portality
Created: 2013-07-15 0215
Last Modified: 2013-07-15 0218
