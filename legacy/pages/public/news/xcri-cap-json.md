#XCRI-CAP JSON

This post introduces a JSON serialisation of the [XCRI CAP 1.2 specification](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2) which acts as a counterpoint to the standard XML formulation.

This is valuable for a number of reasons:

* Constructing web user interfaces with JavaScript is easy when source data is JSON formatted
* The indexing technology we are using in our [XCRI demonstrator](http://cottagelabs.com/projects/xcri) uses JSON as its data format
* JSON is generally more terse than XML, and is thus easier to look at and to transmit

It is not intended that this serialisation is in any way a *standard* only that it is quite a useful way to serialise the data for certain purposes.

##Some principles

Before we begin, some basic principles of the serialisation:

1. We want to be able to model the full XCRI structure, as per the specification
2. We don't care too much about formal namespaces for elements or attributes.  We'll prefix elements with short versions of namespaces for everything not in the standard XCRI namespace, and we'll basically ignore them for attributes
3. We want each output document to be consistently structured, so we can reliably work with the data.  For example, if an element can have multiple values, it should *always* be a list even if there is only one value
4. We're only going to support XCRI 1.2.  If we want to use this on 1.1 formatted data, then we'll have to apply a transform to the data first.

With those in mind, here is an outline of the serialisation:

##Catalog and Provider

Catalog: *The default root element for an XCRI-CAP feed* [[1](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#the_.3Ccatalog.3E_element)]

Provider: *Providers are organisations that offer one or more courses.* [[2](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#the_.3Cprovider.3E_element)]

<pre>
{
    "catalog" : {
        "provider" : [
            {
                "dc:contributor" : ["contributor"],
                "dc:description" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
                "dc:identifier" : [{"type" : "type", "value" : "value"}],
                "image" : {"src" : "src", "title" : "title", "alt" : "alt"},
                "dc:subject" : [{"type" : "type", "identifier" : "identifier", "lang" : "lang", "value" : "value"}],
                "dc:title" : [{"lang" : "lang", "value" : "value"}],
                "dc:type" : "type",
                "mlo:url" : "url",
                "mlo:location" : {
                    "mlo:street" : "street",
                    "mlo:town" : "town",
                    "mlo:postcode" : "postcode",
                    "mlo:phone" : "phone",
                    "mlo:fax" : "fax",
                    "mlo:email" : "email",
                    "mlo:url" : "url",
                    "mlo:address" : [{"type" : "type", "value" : "value"}]
                }
                "course" : [ {} ]
            }
        ]
    }
}
</pre>

The root element "catalog" has only one child element, "provider", which contains the **Common Elements** (see below) and an "mlo:location" element, with the address and other contact details for the provider, and also - importantly - the "course" information.  Notice that each catalog can contain more than one provider, and the provider can contain more than one course.

##Common Elements

There are 8 common elements in XCRI which can be re-used in a variety of different locations, and which provide some basic metadata associated with, for example, providers, courses, and presentations.  These are:

<pre>
{
    "dc:contributor" : ["contributor"],
    "dc:description" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
    "dc:identifier" : [{"type" : "type", "value" : "value"}],
    "image" : {"src" : "src", "title" : "title", "alt" : "alt"},
    "dc:subject" : [{"type" : "type", "identifier" : "identifier", "lang" : "lang", "value" : "value"}],
    "dc:title" : [{"lang" : "lang", "value" : "value"}],
    "dc:type" : "type",
    "mlo:url" : "url",
}
</pre>

The XCRI specification defines XML elements and attributes to handle the parts of each field.  For example, dc:description could be ([notwithstanding limitations defined in the spec](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#Descriptive_Text_Elements)):

<pre>
&lt;dc:description xsi:lang="en" href="http://cottagelabs.com"&gt;A Course from Cottage Labs&lt;dc:description&gt;
</pre>

We have placed all the attributes and the actual text value of the element all as attributes in a JSON object.  We have also set the convention that in cases such as these - where an element may contain both attributes and textual content - the textual content will live in a sub-element keyed with "value"; thus the above example would become:

<pre>
"dc:description" : [{"lang" : "en", "href" : "http://cottagelabs.com", "value" : "A Course from Cottage Labs"}]
</pre>

##Course

*A course provides details of a learning opportunity offered by a learning provider.* [[3](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#the_.3Ccourse.3E_element)]

<pre>
"course" : [
    {
        "mlo:level" : "level",
        "mlo:qualification" : [
            {
                "dc:identifier" : [{"type" : "type", "value" : "value"}],
                "dc:title" : [{"lang" : "lang", "value" : "value"}],
                "abbr" : "abbr",
                "dc:description" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
                "dcterms:educationLevel" : ["education level"],
                "dc:type" : "type",
                "mlo:url" : "url",
                "awardedBy" : "awarded by",
                "accreditedBy" : "accredited by"
            }
        ],
        "presentation" : [ { } ],
        "mlo:credit" : [{"credit:scheme" : "scheme", "credit:level" : "level", "credit:value" : "value"}],
        "dc:contributor" : ["contributor"],
        "dc:description" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "dc:identifier" : [{"type" : "type", "value" : "value"}],
        "image" : {"src" : "src", "title" : "title", "alt" : "alt"},
        "dc:subject" : [{"type" : "type", "identifier" : "identifier", "lang" : "lang", "value" : "value"}],
        "dc:title" : [{"lang" : "lang", "value" : "value"}],
        "dc:type" : "type",
        "mlo:url" : "url",
        "abstract" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "applicationProcedure" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:assessment" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "learningOutcome" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:objective" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:prerequisite" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "regulations" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
    }
]
</pre>

This is where the main body of all the information in any XCRI feed actually is.  You can see within the root "course" element there are the **Common Elements** as described above.  There is also a nested "qualification" element (of which there can be more than one), and a "presentation" element, which describes ways in which the course can be accessed (or, presented!), and which is also repeatable.  The remaining elements at the bottom of the example above form the **[Common Descriptive Elements](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#Common_Descriptive_Elements)** (see below).

##Common Descriptive Elements

The common descriptive elements in XCRI are:

* abstract
* applicationProcedure
* mlo:assessment
* learningOutcome
* mlo:objective
* mlo:prerequisite
* regulations

Each of these elements is structured in the same way, so they are easy to specify.  Each is repeatable, and each can contain a "lang" attribute, an "href" or a "value".  This is the same as we saw with dc:description earlier.

##Presentation

*A presentation is a particular instance of the course offered at a specific time and place or through specified media. It is the entity to which learners apply. Alternative names for this type of structure include course offering and course instance.* [[4](http://www.xcri.org/wiki/index.php/XCRI_CAP_1.2#the_.3Cpresentation.3E_element)]

<pre>
"presentation" : [
    {
        "dc:contributor" : ["contributor"],
        "dc:description" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
        "dc:identifier" : [{"type" : "type", "value" : "value"}],
        "image" : {"src" : "src", "title" : "title", "alt" : "alt"},
        "dc:subject" : [{"type" : "type", "identifier" : "identifier", "lang" : "lang", "value" : "value"}],
        "dc:title" : [{"lang" : "lang", "value" : "value"}],
        "dc:type" : "type",
        "mlo:url" : "url",
        "abstract" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "applicationProcedure" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:assessment" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "learningOutcome" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:objective" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:prerequisite" : [{"lang" : "lang", "href" : "href", "value" : "value"}],
        "regulations" :[{"lang" : "lang", "href" : "href", "value" : "value"}],
        "mlo:start" : {"dtf" : "datetime", "value" : "value"},
        "mlo:end" : {"dtf" : "datetime", "value" : "value"},
        "mlo:duration" : {"interval" : "interval", "value" : "value"},
        "applyFrom" : {"dtf" : "datetime", "value" : "value"},
        "applyUntil" : {"dtf" : "datetime", "value" : "value"},
        "applyTo" : "apply to",
        "mlo:engagement" : [{}],
        "studyMode" : {"identifier" : "identifier", "value" : "value"},
        "attendanceMode" : {"identifier" : "identifier", "value" : "value"},
        "attendancePattern" : {"identifier" : "identifier", "value" : "value"},
        "mlo:languageOfInstruction" : ["lang"],
        "languageOfAssessment" : ["lang"],
        "mlo:places" : "places",
        "mlo:cost" : "cost",
        "age" : "age",
        "venue" : [ { "provider" : { } } ]
    }
]
</pre>

As you can see, this is quite a substantial element, and consists first of the **Common Elements** and then of the **Common Descriptive Elements**, then a range of elements dealing with the actual presentation itself.  Finally, there is a repeatable "venue" element,  which contains a "provider" element as described above.

##Conclusions

You can see a full expression of an XCRI JSON document [here](https://github.com/CottageLabs/xcri/blob/master/xcri.json), and the software which produces and utilises it [here](https://github.com/CottageLabs/xcri).

We are using this serialisation within our demonstrator project, and aren't suggesting that this be a standard, at least not formally.  But we would be interested in your feedback on the value of this, or to hear from you if you find this useful.



Original Title: XCRI CAP JSON
Original Author: richard
Tags: xcri, json, news, richard
Created: 2013-01-02 0000
Last Modified: 2013-03-02 1924
