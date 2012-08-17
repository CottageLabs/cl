SECRET_KEY = "default-key"

# contact info
ADMIN_NAME = "us"
ADMIN_EMAIL = "us@cottagelabs.com"

# service info
SERVICE_NAME = "Cottage Labs"
SERVICE_TAGLINE = ""
HOST = "0.0.0.0"
DEBUG = True
PORT = 5004

# list of superuser account names
SUPER_USER = ["test"]

# elasticsearch settings
ELASTIC_SEARCH_HOST = "127.0.0.1:9200"
ELASTIC_SEARCH_DB = "cl"

# location of media storage folder
MEDIA_FOLDER = "media"

# if search filter is true, anonymous users only see visible and accessible pages in query results
# if search sort and order are set, all queries from /query will return with default search unless one is provided
ANONYMOUS_SEARCH_FILTER = True
SEARCH_SORT = ''
SEARCH_SORT_ORDER = ''

# jsite settings
JSITE_OPTIONS = {
    "searchurl": "/query/record/_search?",
    "recordurl": "/query/record/",
    "savetourl": "",
    "datatype": "json",
    "collaborative": True,
    "facetview": {
        "search_url": "/query/record/_search?",
        "datatype": "json",
        "search_index": 'elasticsearch',
        "searchbox_class": '.facetview_searchbox',
        "embedded_search": False,
        "initialsearch": True,
        "result_display": [
            [
                {
                    "pre": '<h4><a href="',
                    "field": "url",
                    "post": '">'
                },
                {
                    "field": "title",
                    "post": "</a></h4>"
                }
            ],
            [
                {
                    "field": "excerpt"
                }
            ],
            [
                {
                    "pre": "by ",
                    "field": "author"
                },
                {
                    "pre": " on ",
                    "field": "created_date"
                }
            ]
        ],
        "searchwrap_start": '<div id="facetview_results" class="clearfix">',
        "searchwrap_end":"</div>",
        "resultwrap_start":'<div class="result_box"><div class="result_info">',
        "resultwrap_end":"</div></div>",
        "result_box_colours":['#e7ffdf','#f7f9d0','#cacaff','#caffd8','#ffdfff','#eeeeee','#c9d2d4'],
        "paging":{
            "from":0,
            "size":9
        }
    },
    "tagkey": "tags",
    "comments": "cottagelabs",
    "twitter": "cottagelabs",
    "bannerheight": "245px",
    "editable": True,
    "richtextedit": False,
    "jspagecontent": False
}

# a dict of the ES mappings. identify by name, and include name as first object name
# and identifier for how non-analyzed fields for faceting are differentiated in the mappings
FACET_FIELD = ".exact"
MAPPINGS = {
    "record" : {
        "record" : {
            "dynamic_templates" : [
                {
                    "default" : {
                        "match" : "*",
                        "match_mapping_type": "string",
                        "mapping" : {
                            "type" : "multi_field",
                            "fields" : {
                                "{name}" : {"type" : "{dynamic_type}", "index" : "analyzed", "store" : "no"},
                                "exact" : {"type" : "{dynamic_type}", "index" : "not_analyzed", "store" : "yes"}
                            }
                        }
                    }
                }
            ]
        }
    }
}
