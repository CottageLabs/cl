SECRET_KEY = 'default-key'

# service and super user account
SERVICE_NAME = "Cottage Labs"
SUPER_USER = ["test"]
HOST = "0.0.0.0"
DEBUG = True
PORT = 5004

# elasticsearch settings
ELASTIC_SEARCH_HOST = "127.0.0.1:9200"
ELASTIC_SEARCH_DB = "cl"

# location of media storage folder
MEDIA_FOLDER = 'media'

# jsite settings
JSITE_OPTIONS = {
    "searchurl": "/query/record/_search?",
    "recordurl": "/query/record/",
    "savetourl": "",
    "datatype": "json",
    "collaborative": False,
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
                    "field": "url",
                    "post": "</a></h4>"
                }
            ],
            [
                {
                    "field": "excerpt"
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
            "date_detection" : False,
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
    },
    "collection" : {
        "collection" : {
            "date_detection" : False,
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
