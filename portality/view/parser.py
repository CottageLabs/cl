'''
An endpoint for parsing a page or a string for keywords.
'''

import json, requests, re, string

from flask import Blueprint, request, abort, make_response

from portality.core import app
import portality.models as models

from topia.termextract import extract


blueprint = Blueprint('parser', __name__)

# pass in a URL or a string and it will be parsed for keywords and they will 
# be handed back.

# create a term extractor and keep it in memory - they have quite a start-up
# overhead so don't want to create one each time
extractor = extract.TermExtractor()

@blueprint.route('/')
@blueprint.route('/<path:path>')
def parser(path='', blurb='', scale=3, minoccur=2, omitscores=False, boostphrases=False, size=0):
    size = int(request.values.get('size',size))
    minoccur = int(request.values.get('minoccur',minoccur))
    scale = int(request.values.get('scale',scale))
    if 'omitscores' in request.values and request.values['omitscores'].lower() not in ['false','0','no']:
        omitscores = True
    if 'boostphrases' in request.values and request.values['boostphrases'].lower() not in ['false','0','no']:
        boostphrases = True
    
    extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=minoccur)

    if path:
        url = path
    else:
        url = request.values.get('url','')

    if url and not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    if url:
        #try:
            # NOTE: GETTING THIS TO WORK PIP INSTALL SPYNNER WHICH REQUIRES 
            # A BUNCH OF OTHER STUFF (I AM NOT SURE EXACTLY WHICH YET): 
            # sudo apt-get install libx11 libx11-dev xvfb libxtst-dev libpng-dev
            # https://github.com/makinacorpus/spynner/#dependencies
            # still fails on importing PyQt4 which is on my system but can't
            # get it into my virtual env. Rely on non-js page content for now.
        #import spynner
        #browser = spynner.Browser()
        #browser.create_webview(True)
        #browser.load(url, load_timeout=60)
        #c = browser._get_html()
        #browser.close()
        #c = _html_text(c)
        #except:
        c = requests.get(url)
        c = _html_text(c.text)
    else:
        c = request.values.get('blurb',blurb)
        
    if c:
        # TODO: check for parameters to the extractor and pass them in 
        # from the method signature or from the request.values
        terms = extractor(c)
        result = {}
        for t, o, l in terms:
            if boostphrases:
                ct = o + l
            else:
                ct = o
            result[t.lower()] = ct * scale
        res = [ {"term":i[0],"score":i[1]} for i in sorted(result.items(), key=lambda x: x[1], reverse=True) if len(i[0].replace(' ','')) > 2 and i[0].replace(' ','') not in url and i[0][0] in string.lowercase + string.uppercase and i[0][len(i[0])-1] in string.lowercase + string.uppercase ]
        if omitscores:
            res = [i[0] for i in res]
        if size is not 0:
            res = res[:size]
    else:
        res = [] # nothing to report on

    resp = make_response( json.dumps(res) )
    resp.mimetype = "application/json"
    return resp


def _html_text(html):
    # first thing is to strip the style and script tags, with all their content
    processed = re.sub("(?i)<style[ ]{0,1}.*?>.*?</style>", "", html, re.DOTALL)
    processed = re.sub("(?i)<script[ ]{0,1}.*?>.*?</script>", "", processed, re.DOTALL)

    # get rid of links and noscripts and select lists too
    processed = re.sub("(?i)<a[ ]{0,1}.*?>.*?</a>", "", processed, re.DOTALL)
    processed = re.sub("(?i)<noscript[ ]{0,1}.*?>.*?</noscript>", "", processed, re.DOTALL)
    processed = re.sub("(?i)<select[ ]{0,1}.*?>.*?</select", "", processed, re.DOTALL)
    
    # now get rid of all of the other html tags, leaving their content behind
    processed = re.sub("<[/]{0,1}[!a-zA-Z]+[ ]{0,1}.*?>", "", processed, re.DOTALL)
    
    # finally tidy up by getting rid of all the newlines and tabs that will be all
    # over the place
    processed = processed.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    
    return processed

