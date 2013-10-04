'''
An endpoint for crawling a website and getting back the pages
'''

import json, requests

from flask import Blueprint, request, abort, make_response

from portality.core import app
import portality.models as models


blueprint = Blueprint('sixdegrees', __name__)


# from a starting url, use the crawler and the parser to build up a six 
# degrees map from that url


@blueprint.route('/')
@blueprint.route('/<start>')
def sixdegrees(start=False, depth=6, delayfish=0, internal=True, external=True, raw=False):

    if not start: start = request.values.get('start',False)
    if start and not start.startswith('http://') and not start.startswith('https://'):
        start = 'http://' + start
    
    depth = request.values.get('depth',depth)
    delayfish = request.values.get('depth',delayfish)
    internal = request.values.get('depth',internal)
    external = request.values.get('depth',external)
    
    res = {}
    
    if start:
        pass
        # pass the starting url to the crawler to get a listing of all its links
        # for every external url, pass it to the crawler
        # build all the sets of results back up into a result object
        # maybe run each link through the parser too, to guess what the page is about?
        # save them into an index?

    if raw:
        return res
    else:
        resp = make_response( json.dumps(res) )
        resp.mimetype = "application/json"
        return resp






