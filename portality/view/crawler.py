'''
An endpoint for crawling a website and getting back the pages
'''

import json, requests

from flask import Blueprint, request, abort, make_response

from portality.core import app
import portality.models as models


blueprint = Blueprint('crawler', __name__)


# take a start url. Get the content at that url and extract every web link from it
# add every local link as a key to the return object, pointing to a list
# for every local link, get the content of the link and add any new local links to the keys
# whilst doing these processes, add any new external links found into the lists the keys point to
# return the complete object list
# track which local pages link to which other local pages? 

@blueprint.route('/')
@blueprint.route('/<url>')
def crawler(url=False, depth=0, raw=False):

    if not url: url = request.values.get('url',False)
    if url and not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    depth = request.values.get('depth',depth)
    
    res = {}
    
    if url:
        # TODO: add a check to pull the root and look for a sitemap
        # if found, get the sitemap and pull the content at the level
        res = _link_exrtactor(url, depth)

    if raw:
        return res
    else:
        resp = make_response( json.dumps(res) )
        resp.mimetype = "application/json"
        return resp



def _link_extractor(url,depth,links={}):
    c = requests.get(url)
    links = _extract_links(c.text())
    # TODO: if depth permits, iterate the links 
    return links


def _extract_links(content):
    # TODO: extract the links from this content and return them
    return {}





