# ========================
# MAIN SETTINGS

# make this something secret in your overriding app.cfg
SECRET_KEY = "default-key"

# contact info
ADMIN_NAME = "Cottage Labs"
ADMIN_EMAIL = "us@cottagelabs.com"

# service info
SERVICE_NAME = "Cottage Labs"
SERVICE_TAGLINE = "We don't sell products, we trade our skills"
HOST = "0.0.0.0"
DEBUG = True
PORT = 5004

# elasticsearch settings
ELASTIC_SEARCH_HOST = "http://127.0.0.1:9200" # remember the http:// or https://
ELASTIC_SEARCH_DB = "cl"
INITIALISE_INDEX = True # whether or not to try creating the index and required index types on startup

# list of superuser account names
SUPER_USER = ["test"]

# Can people register publicly? If false, only the superuser can create new accounts
PUBLIC_REGISTER = False


# ========================
# MAPPING SETTINGS

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
            ],
            "properties":{
                "datefrom":{
                    "type": "date",
                    "index": "not_analyzed",
                    "format": "dd/MM/yyyy"
                },
                "dateto":{
                    "type": "date",
                    "index": "not_analyzed",
                    "format": "dd/MM/yyyy"
                },
                "duedate":{
                    "type": "date",
                    "index": "not_analyzed",
                    "format": "dd/MM/yyyy"
                },
                "datepaid":{
                    "type": "date",
                    "index": "not_analyzed",
                    "format": "dd/MM/yyyy"
                }
            }
        }
    }
}
MAPPINGS['account'] = {'account':MAPPINGS['record']['record']}
MAPPINGS['project'] = {'project':MAPPINGS['record']['record']}
MAPPINGS['pages'] = {'pages':MAPPINGS['record']['record']}


# ========================
# QUERY SETTINGS

# list index types that should not be queryable via the query endpoint
NO_QUERY = ['account']

# can anonymous users get raw JSON records via the query endpoint?
PUBLIC_ACCESSIBLE_JSON = True 

# list additional terms to impose on anonymous users of query endpoint
# for each index type that you wish to have some
# must be a list of objects that can be appended to an ES query.bool.must
# for example [{'term':{'visible':True}},{'term':{'accessible':True}}]
ANONYMOUS_SEARCH_TERMS = {
    "pages": [{'term':{'visible':True}},{'term':{'accessible':True}}]
}

# a default sort to apply to query endpoint searches
# for each index type that you wish to have one
# for example {'created_date' + FACET_FIELD : {"order":"desc"}}
DEFAULT_SORT = {
    "pages": {'created_date' + FACET_FIELD : {"order":"desc"}}
}


# ========================
# MEDIA SETTINGS

# location of media storage folder
MEDIA_FOLDER = "media"


# ========================
# PAGEMANAGER SETTINGS

# folder name for storing page content
# will be added under the templates/pagemanager route
CONTENT_FOLDER = False

# etherpad endpoint if available for collaborative editing
COLLABORATIVE = 'http://pads.cottagelabs.com'

# when a page is deleted from the index should it also be removed from 
# filesystem and etherpad (if they are available in the first place)
DELETE_REMOVES_FS = False # True / False
DELETE_REMOVES_EP = False # MUST BE THE ETHERPAD API-KEY OR DELETES WILL FAIL

# disqus account shortname if available for page comments
COMMENTS = 'cottagelabs'


# ========================
# HOOK SETTINGS

REPOS = {
    "portality": {
        "path": "/opt/portality/src/portality"
    },
    "content": {
        "path": "/opt/portality/src/portality/portality/templates/pagemanager/content"
    }
}

# ========================
# FEED SETTINGS

BASE_URL = "http://cottagelabs.com"

# Maximum number of feed entries to be given in a single response.  If this is omitted, it will
# default to 20
MAX_FEED_ENTRIES = 20

# Maximum age of feed entries (in seconds) (default value here is 3 months).  If this is omitted
# then we will always supply up to the MAX_FEED_ENTRIES above
MAX_FEED_ENTRY_AGE = 7776000

# Licensing terms for feed content
FEED_LICENCE = "(c) Cottage Labs LLP 2012.  All content Copyheart: http://copyheart.org"

# name of the feed generator (goes in the atom:generator element)
FEED_GENERATOR = "CottageLabs feed generator"

# Larger image to use as the logo for all of the feeds
FEED_LOGO = "http://cottagelabs.com/media/cottage_hill_bubble_small.jpg"




# ========================
# CL SETTINGS

# Facetview displays, need to be moved somewhere else, perhaps into pagemanager
FACETVIEW_DISPLAYS = {
    "compact" : {
        'result_display':  [
            [
                {
                    "pre": '<a class="cl_red_leader" href="',
                    "field": "url"
                },
                {
                    "pre": '">',
                    "field": "title",
                    "post": "</a>&nbsp;"
                },
                {
                    "field" : "excerpt"
                }
            ]
        ],
        'searchwrap_start': '<div class="row-fluid"><div id="facetview_results" class="clearfix">',
        'searchwrap_end': '</div></div>',
        'resultwrap_start': '<span>',
        'resultwrap_end': '</span>',
        "paging":{
            "from":0,
            "size":4
        }
    },
    "stories" : {
        'result_display':   [
            [
                {
                    "pre": '<div class="row-fluid"><div class="span9"><strong><a class="cl_black_leader" href="',
                    "field": "url"
                },
                {
                    "pre": '">',
                    "field": "title",
                    "post": "</a></strong></div>"
                },
                {
                    "pre" : '<div class="span3"><em>',
                    "field" : "last_updated",
                    "post" : "</em></div>"
                },
                {
                    "field" : "excerpt"
                }
            ]
        ],
        'searchwrap_start': '<div class="row-fluid"><div id="facetview_results" class="clearfix">',
        'searchwrap_end': '</div></div>',
        'resultwrap_start': '<div class="cl_news_line">',
        'resultwrap_end': '</div>',
        "paging":{
            "from":0,
            "size":20
        }
    },
    "features": {
        'result_display': [
            [
                {
                    "pre": '<div class="cl_feature_box"><a class="cl_feature_title" href="',
                    "field": "url"
                },
                {
                    "pre": '">',
                    "field": "title",
                    "post": "</a></div>"
                }
            ],
            [
                {
                    "pre": '<div class="cl_feature_text"><a class="cl_feature_content" style="color:#333;" href="',
                    "field": "url"
                },
                {
                    "pre": '">',
                    "field": "excerpt",
                    "post": '</a></div>'
                }
            ]
        ],
        'searchwrap_start': '<div class="row-fluid"><div class="well" style="margin-top:20px;margin-bottom:0px;"><div id="facetview_results" class="clearfix">',
        'searchwrap_end': '</div></div></div>',
        'resultwrap_start': '<div class="span3 feature_span">',
        'resultwrap_end': '</div>',
        "paging":{
            "from":0,
            "size":4
        }
    },
    "panels": {
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
    "list": {
        'result_display': [
            [
                {
                    "pre": '<div class="cl_feature_box"><span class="cl_feature_title">',
                    "field": "title",
                    "post": "</span></div>"
                }
            ],
            [
                {
                    "pre": '<div class="cl_feature_text"><span class="cl_feature_content">',
                    "field": "excerpt",
                    "post": '</span></div>'
                }
            ],
            [
                {
                    "pre": '<div class="cl_feature_link"><a href="',
                    "field": "url",
                    "post": '">read more &raquo;</a></div>'
                }
            ]
        ],
        'searchwrap_start': '<table id="facetview_results" class="table table-bordered table-striped table-condensed">',
        'searchwrap_end': '</table>',
        'resultwrap_start': '<tr><td>',
        'resultwrap_end': '</td></tr>',
        "paging":{
            "from":0,
            "size":10
        }
    },
    "titles": {
        'result_display': [
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
            ]
        ],
        'searchwrap_start': '<table id="facetview_results" class="table table-bordered table-striped table-condensed">',
        'searchwrap_end': '</table>',
        'resultwrap_start': '<tr><td>',
        'resultwrap_end': '</td></tr>',
        "paging":{
            "from":0,
            "size":10
        }
    }
}


