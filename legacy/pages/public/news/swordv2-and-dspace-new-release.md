#SWORDv2 and DSpace: New Release

We're pleased to be able to say that in the last month we've been working hard to get the new version of the [SWORDv2](http://swordapp.org) [java library](https://github.com/swordapp/JavaServer2.0) and the related [DSpace](http://dspace.org) module which uses it up to release quality, in time for the [DSpace 4.0 release](https://wiki.duraspace.org/display/DSPACE/DSpace+Release+4.0+Notes) which will be very soon.

For DSpace, this means we've achieved the following:

* Some enhancements to the authentication/authorisation process, and more configurability
* Proper support for the standard DSpace METS package, which had been omitted in the first version of SWORDv2 for various complicated reasons
* Lots more configuration options, giving administrators the ability to fine tune their SWORDv2 endpoint
* Improvements to how metadata is created, added and replaced and how those changes affect items in different parts of the workflow
* Some general bug fixing and refactoring for better code

If you're not a DSpace user, though, you can still benefit from the common java library; we've now released this properly through the maven central repository, and if you want to build your server environment from it, you can include it in your project as easily as:

<pre>
    &lt;dependency&gt;
        &lt;groupId&gt;org.swordapp&lt;/groupId&gt;
        &lt;artifactId&gt;sword2-server&lt;/artifactId&gt;
        &lt;version&gt;1.0&lt;/version&gt;
        &lt;type&gt;jar&lt;/type&gt;
        &lt;classifier&gt;classes&lt;/classifier&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.swordapp&lt;/groupId&gt;
        &lt;artifactId&gt;sword2-server&lt;/artifactId&gt;
        &lt;version&gt;1.0&lt;/version&gt;
        &lt;type&gt;war&lt;/type&gt;
    &lt;/dependency&gt;
</pre>

We hope you have fun with the new software.  In the mean time, don't forget that there's lots of SWORD expertise hanging out on the [sword-app-tech mailing list](https://lists.sourceforge.net/lists/listinfo/sword-app-tech).

<em><a href="/people/richard">Richard Jones</a>, 15th November 2013</em>



Original Title: SWORDv2 and DSpace: New Release
Original Author: richard
Tags: richard, swordv2, news, featured, java, dspace
Created: 2013-11-15 1218
Last Modified: 2013-11-15 1236
