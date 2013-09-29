'''
An endpoint for crawling a website and getting back the pages
'''

import json, requests

from flask import Blueprint, request, abort, make_response

from portality.core import app
import portality.models as models


blueprint = Blueprint('crawler', __name__)

# pass in a URL or a string and it will be parsed for keywords and they will 
# be handed back.

@blueprint.route('/')
@blueprint.route('/<url>')
def stream(url=False, depth=0):

    if not url: url = request.values.get('url',False)
    if url and not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    depth = request.values.get('depth',depth)
    
    res = {}
    
    if url:
        # TODO: add a check to pull the root and look for a sitemap
        # if found, get the sitemap and pull the content at the level
        res = _link_exrtactor(url, depth)

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





