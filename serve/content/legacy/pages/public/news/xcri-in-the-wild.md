#XCRI in the Wild
<br>

After working with data from a variety of XCRI feeds, we've identified a number of issues which commonly arise either with specific implementations of the standard, or even with the standard itself.  This post outlines these issues, and the steps that have been necessary in attempting to prove the value of XCRI feeds.

##Issues with implementations
<br>

**Technically incorrect XML** - it is occasionally seen that XML is technically incorrect, incorporating invalid escape characters (e.g. HTML escape characters incorrectly used in XML), or special (non unicode) characters copy and pasted directly from Word documents.  This means automated parsing of that XML can be impossible, and manual intervention is required.

**Schema invalid XML** - It is occasionally seen that XML documents are not valid implementations of the schema.  Notwithstanding the deeper details, such as date formats, we have also seen, for example, <code>course</code> elements nested directly inside <code>catalog</code> elements, rather than inside the correct <code>provider</code> element (as described [here](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#the_.3Ccatalog.3E_element))

**Mis-use of fields** - There is extensive mis-use of fields in the schema across the sector.  In some cases semantics are shoe-horned in to more generic fields (in particular <code>dc:description</code>), in other cases data is placed into the wrong fields, and we have also seen default text from course data environments included in the data (e.g. *"This field should contain a short description of the course"*)

**Variable commitment to fields** - Some organisations are good at populating certain fields, and not others, and there is not much consistency across the sector as to who is populating what.  From an aggregator point of view, this is difficult because it's hard to provide a view over the entire dataset of certain properties.

**Dud links** - a random spot check of some of the URLs provided in the data from the sources we harvested indicates a high proportion of dud links.

**Useful data defined only in human readable content** - It is extremely common for useful data (such as age ranges) to be included in textual descriptions of courses, but not in their explicit data fields.  For example, *"Tennyson High School (14-19)"* does not indicate in the <code>age</code> field that it is for 14 - 19 year olds.  This is a ubiquitous problem throughout all XCRI data that we have examined, and is particularly notable in age and cost data, and limits the usability of this data in high quality user interfaces.

**Obviously missing data** - There are cases where we can clearly locate some information (e.g. the cost of a course) on an institution's web page, but not find the equivalent data in their XCRI feed.  This is concerning because it makes us wonder what else we are missing, what the institutional commitment to their XCRI feed is, and whether the source of the data for their website and their XCRI feed is even the same (which would indicate undue duplication of effort, as well as increasing the risk of error). The concept of exposing course data via XCRI feeds is a good one, but in order to succeed it requires full commitment to making such feeds first-class sources of such data; if they do not appear to be so, then they are less likely to be relied upon by external aggregators.

**Semantics embedded in fields** - in some cases we see semantics of the content of a field embedded in the field itself.  For example, we may see:

    <dc:description>aim: to do X, Y and Z</dc:description>

In some cases (such as the previous example) this is actually XCRI 1.1 description type semantics shoe-horned into XCRI 1.2, even though both versions of the spec have formal ways of representing that data.  The above would be, in XCRI 1.1:

    <dc:description xsi:type="aim">to do X, Y and Z</dc:description>

And in XCRI 1.2:

    <mlo:objective>to do X, Y and Z</mlo:objective>
    
In other cases, the semantics are of unknown origin, and it is not at all clear how to interpret them (see next point)

**Semantics for communities of practice** - Nearly 50% of our harvested XCRI data at time of writing contains the following <code>dc:description field</code>:

    <dc:description>support: Yes</dc:description>

This is not an XCRI 1.1 semantic as in our earlier example, and there is no obvious attribute or other documentation to expand on the meaning of this.


##Issues with the specification
<br>

**Embedded XHTML** - The specification permits for XHTML to be included inside any of the [Descriptive Text Elements](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#Descriptive_Text_Elements).  While the reason for this is clear - to allow formatted descriptions of course elements to be incorporated - it causes problems in a number of ways: 

* Firstly, it means that when the XML is machine-read the XHTML will get parsed along with the enclosing XML document, meaning that displaying it involves some to-and-fro with parsing and serialising XML fragments.  
* Secondly - and more seriously - it means that the descriptive text is only suitable for certain kinds of environment; in particular it is only suited to the web, but in fact only a sub-set of web environments, since it is problematic to work with in some JavaScript contexts.

A far better approach would be to disallow XHTML content within the XCRI specification and strive, instead, for a more pure and machine readable description of courses, and leave it to client environments to determine what the appropriate display template is.

**Constraints on repeated fields** - The specification allows for most fields to be repeated, but for certain fields this makes it difficult to build a clear user interface.  For example, repeated <code>dc:description</code> fields with different kinds of descriptions make it hard to automatically select the most appropriate content to present to the user.  Typically, a specification would place further constraints on the use of such fields, such as that they all have different <code>xml:lang</code> elements, and the XCRI spec could benefit from a degree of tightening up around such conditions.  For example, the desired output would be:

    <dc:description>This is the default description</dc:description>
    <dc:description xml:lang="fr">c'est la description en franÃ§ais</dc:description>
    <dc:description xml:lang="de">dies ist der Deutsch Beschreibung</dc:description>

The specification could then include a constraint such as:

<blockquote>
Descriptive Text Elements MAY be repeated, but there MUST NOT be two or more elements which either omit the xml:lang attribute or have the same value for the xml:lang attribute
</blockquote>

**Insufficiently open** - The XCRI specification, while ostensibly open, is based upon other standards which are not.  In particular *"[EN 15982] EN 15982: Metadata For Learning Opportunities (Advertising)"*, which we have only been able to find paid-for versions of (for example, [here](http://shop.bsigroup.com/ProductDetail/?pid=000000000030204827)).  This is a problem for a number of reasons: 

* firstly, we were not able to examine all parts of the XCRI specification, since it defers to EN 15982 on a number of occasions, and this has necessarily limited our implemetation
* secondly, as a publicly-funded endeavour, it should be using open standards/technologies from a philosophical standpoint

Note also, that the old version of the MLO specification (EN 15903 *is* available freely online [here](http://www.cen-ltso.net/main.aspx?put=1042))

**Freedom of representation** - There are some fields where there are different approaches an implementation could take for representing data, and no clear guidance as to which way is correct.  For example, we can readily find examples of multiple <code>presentation</code> elements each containing a single <code>venue</code> element, where the only difference between each <code>presentation</code> is the <code>venue</code> itself; this could equally well be modelled as a single <code>presentation</code> element with multiple <code>venue</code> elements, but the spec (by omission) allows both approaches, creating difficulties for aggregators in choosing an appropriate approach.  So, for example:

    <presentation>
        [generic presentation metadata]
        <venue>[venue 1 information]</venue>
    </presentation>
    <presentation>
        [generic presentation metadata]
        <venue>[venue 2 information]</venue>
    </presentation>
    <presentation>
        [generic presentation metadata]
        <venue>[venue 3 information]</venue>
    </presentation>
    ...

could also be represented as:

    <presentation>
        [generic presentation metadata]
        <venue>[venue 1 information]</venue>
        <venue>[venue 2 information]</venue>
        <venue>[venue 3 information]</venue>
    </presentation>

Both approaches are spec compliant.  Similar problems arise with the use of the various <code>url</code> and <code>identifier</code> fields available.  Most likely this diversity in implementations can best be fixed with accompanying recommendations and best practice guides.

**Instructions to Aggregator** - Often the specification will provide instructions *to* an Aggregator regarding what it MUST do ([for example](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#Common_Elements) an aggregator *"MUST be able to process the description, identifier, image, subject, title and url elements"*), which is an incorrect approach to spec writing.  The XCRI specification should be focussed on the format, and what it means to be format compliant.  The Aggregators will do whatever they want to do with the data, which is as it should be.

**Lack of use cases/good practice guides** - At time of writing there are no clearly described use cases or good practice guides for XCRI, and we feel that the lack of these is at least a contributing factor to the issues we have with specific implementations.  It would be highly valuable to document the use cases, and use those to driver further versions of the specification.  There is a [page on the wiki](http://www.xcri.org/wiki/index.php/XCRI_1.2_BP) which looks primed to include this information, but was empty when this post was written.

**Not enough m2m data** - the specification focusses heavily on human readable data (some of it with embedded XHTML), and not enough on machine readable data.  As such, it is very difficult for an aggregator to do intelligent or interesting things with the data as-is, and a lot of post processing may be necessary.  There would be tremendous value in enabling m2m comprehension of the course data.

**Relaxing existing specifications** - many aspects of the specification *relax* requirements of the specifications from which it borrows ([for example](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#Common_Elements) *hasPart/isPartOf: these elements are included for compatibility with the [EN 15982] standard. Producers SHOULD NOT use these elements*).  This is generally an unwise approach to standards development, since by relaxing constraints of a parent specification, the child specification is no longer compatible with the parent and any tool chains which are designed to work with the parent.  We'd recommend either breaking the dependency on the MLO specification (which may be desireable for its non-open status, but also difficult to achieve) or fully embracing its semantics.


##Issues with mapping from 1.1 to 1.2

As part of our demonstrator we are using the [XSLT transform from XCRI 1.1 to 1.2](http://www.xcri.co.uk/examples-a-code/149-mapping-11-to-12.html).  We have found this transformation to be lossy, and in particular it omits attributes from XML elements even if they are valid in XCRI 1.2.  This means that some custom extensions to any XCRI 1.1 data will be lost in translation, and useful attributes which are part of the spec are also lost.  A concrete example is that the <code>xsi:type="geo:lat"</code> or <code>"geo:long"</code> attributes are lost from the <code>mlo:address</code> elements of locations.


##Conclusions

Despite the stated focus on Aggregation, the extensive allowance for free-text within XCRI documents detracts from the value that machine-readable feed formats should provide.

The specification does not appear to have been designed with specific aggregation use cases in mind; rather, the overriding use case instead appears to be that of enabling data providers to easily drop existing textual descriptions into a seemingly interoperable machine-readable document. Whilst there is of course a benefit to lowering the difficulty of producing such feeds, there is a risk that taking this too far will result in feeds that are not fit for purpose. This risk must be avoided at all costs.

Whilst we are succeeding in demonstrating the value of XCRI course feeds as our project proceeds, it becomes increasingly clear that course data must be represented in a far more granular and technical fashion if it is to succeed in being useful in wider contexts. Further efforts to develop the spec in this direction, along with provision of some XCRI libraries and document validators, will help to increase adoption of and commitment to XCRI.








Original Title: XCRI in the Wild
Original Author: richard
Tags: xcri, data, news, richard
Created: 2013-01-03 2112
Last Modified: 2013-03-02 1924
