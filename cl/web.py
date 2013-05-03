# -*- coding: utf-8 -*-

import re, json, requests, urllib, urllib2, markdown
from flask import Flask, jsonify, json, request, redirect, abort, make_response
from flask import render_template, flash
from flask.views import View, MethodView
from flask.ext.login import login_user, current_user
import cl.dao
import cl.util as util
from cl.core import app, login_manager
from cl.view.account import blueprint as account
from cl.view.sitemap import blueprint as sitemap
from cl.view.tagging import blueprint as tagging
from cl.view.media import blueprint as media
from cl.view.admin import blueprint as admin
from cl import auth
from copy import deepcopy


app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(sitemap, url_prefix='/sitemap')
app.register_blueprint(tagging, url_prefix='/tagging')
app.register_blueprint(media, url_prefix='/media')
app.register_blueprint(admin, url_prefix='/admin')


@login_manager.user_loader
def load_account_for_login_manager(userid):
    out = cl.dao.Account.pull(userid)
    return out

@app.context_processor
def set_current_user():
    """ Set some template context globals. """
    return dict(current_user=current_user, sharethis=app.config.get('JSITE_OPTIONS',[]).get('sharethis',False))

@app.before_request
def standard_authentication():
    """Check remote_user on a per-request basis."""
    remote_user = request.headers.get('REMOTE_USER', '')
    if remote_user:
        user = cl.dao.Account.pull(remote_user)
        if user:
            login_user(user, remember=False)
    # add a check for provision of api key
    elif 'api_key' in request.values:
        res = cl.dao.Account.query(q='api_key:"' + request.values['api_key'] + '"')['hits']['hits']
        if len(res) == 1:
            user = cl.dao.Account.pull(res[0]['_source']['id'])
            if user:
                login_user(user, remember=False)


@app.errorhandler(404)
def page_not_found(e):
    jsitem = deepcopy(app.config['JSITE_OPTIONS'])
    jsitem['facetview']['initialsearch'] = False
    return render_template('404.html', jsite_options=json.dumps(jsitem)), 404

@app.errorhandler(401)
def page_not_found(e):
    jsitem = deepcopy(app.config['JSITE_OPTIONS'])
    jsitem['facetview']['initialsearch'] = False
    return render_template('401.html', jsite_options=json.dumps(jsitem)), 401


# catch mailer requests and send them on
@app.route('/contact', methods=['GET','POST'])
def mailer():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        try:
            if request.values.get('message',False) and not request.values.get('not',False):
                util.send_mail(
                    [app.config['ADMIN_NAME'] + ' <' + app.config['ADMIN_EMAIL'] + '>'],
                    request.values.get('email',app.config['ADMIN_NAME'] + ' <' + app.config['ADMIN_EMAIL'] + '>'),
                    'website enquiry',
                    request.values['message']
                )
                return ''
            else:
                abort(403)
        except:
            abort(500)


# pass queries direct to index. POST only for receipt of complex query objects
@app.route('/query/<path:path>', methods=['GET','POST'])
@app.route('/query/', methods=['GET','POST'])
@util.jsonp
def query(path='Record'):
    pathparts = path.split('/')
    subpath = pathparts[0]
    if subpath.lower() in app.config['NO_QUERY_VIA_API']:
        abort(401)
    klass = getattr(cl.dao, subpath[0].capitalize() + subpath[1:] )
    
    if len(pathparts) > 1 and pathparts[1] == '_mapping':
        resp = make_response( json.dumps(klass().query(endpoint='_mapping')) )
    elif len(pathparts) == 2 and pathparts[1] not in ['_mapping','_search']:
        if request.method == 'POST':
            abort(401)
        else:
            rec = klass().pull(pathparts[1])
            if rec:
                if ( not app.config['ANONYMOUS_SEARCH_FILTER'] ) or ( app.config['ANONYMOUS_SEARCH_FILTER'] and rec['visible'] and rec['accessible'] ):
                    resp = make_response( rec.json )
                else:
                    abort(401)
            else:
                abort(404)
    else:
        if request.method == "POST":
            if request.json:
                qs = request.json
            else:
                qs = dict(request.form).keys()[-1]
        elif 'q' in request.values:
            qs = {'query': {'query_string': { 'query': request.values['q'] }}}
        elif 'source' in request.values:
            qs = json.loads(urllib2.unquote(request.values['source']))
        else: 
            qs = ''
        for item in request.values:
            if item not in ['q','source','callback','_'] and isinstance(qs,dict):
                qs[item] = request.values[item]
        if 'sort' not in qs and app.config['SEARCH_SORT']:
            qs['sort'] = {app.config['SEARCH_SORT'].rstrip(app.config['FACET_FIELD']) + app.config['FACET_FIELD'] : {"order":app.config.get('SEARCH_SORT_ORDER','asc')}}
        if app.config['ANONYMOUS_SEARCH_FILTER'] and current_user.is_anonymous():
            terms = {'visible':True,'accessible':True}
        else:
            terms = ''
        resp = make_response( json.dumps(klass().query(q=qs, terms=terms)) )
    resp.mimetype = "application/json"
    return resp
        
        
# implement a JSON stream that can be used for autocompletes
# index type and key to choose should be provided, and can be comma-separated lists
# "q" param can provide query term to filter by
# "counts" param indicates whether to return a list of strings or a list of lists [string, count]
# "size" can be set to get more back
# NOTE THIS DOES NOT USE THE DAO- IT IS DIRECT TO ES
@app.route('/stream')
@app.route('/stream/<index>')
@app.route('/stream/<index>/<key>')
def stream(index='record',key='tags'):

    t = 'http://' + str(app.config['ELASTIC_SEARCH_HOST']).lstrip('http://').rstrip('/') + '/' + app.config['ELASTIC_SEARCH_DB'] + '/'

    if index in app.config['NO_QUERY_VIA_API']: abort(401)
    indices = []
    for idx in index.split(','):
        if idx not in app.config['NO_QUERY_VIA_API']:
            indices.append(idx)

    keys = key.split(',')

    q = request.values.get('q','*')
    if not q.endswith("*"): q += "*"
    if not q.startswith("*"): q = "*" + q

    qry = {
        #'query':{'query_string':{'query':q}},
        'query':{'match_all':{}},
        'size': 0,
        'facets':{}
    }
    for ky in keys:
        qry['facets'][ky] = {"terms":{"field":ky+app.config['FACET_FIELD'],"order":request.values.get('order','term'), "size":request.values.get('size',1000)}}
    
    r = requests.post(t + ','.join(indices) + '/_search', json.dumps(qry))

    res = []
    if request.values.get('counts',False):
        for k in keys:
            res = res + [[i['term'],i['count']] for i in r.json()['facets'][k]["terms"]]
    else:
        for k in keys:
            res = res + [i['term'] for i in r.json()['facets'][k]["terms"]]

    resp = make_response( json.dumps(res) )
    resp.mimetype = "application/json"
    return resp


@app.route('/deduplicate', methods=['GET', 'POST'])
def deduplicate(path='',duplicates=[],target='/'):
    if current_user.is_anonymous():
        abort(401)
    elif request.method == 'GET':
        jsitem = deepcopy(app.config['JSITE_OPTIONS'])
        jsitem['facetview']['initialsearch'] = False
        return render_template('deduplicate.html', jsite_options=json.dumps(jsitem), duplicates=duplicates, url=target)
    elif request.method == 'POST':
        for k,v in request.values.items():
            if v and k not in ['url', 'submit']:
                if k.startswith('delete_'):
                    rec = cl.dao.Record.pull(k.replace('delete_',''))
                    if rec is not None: rec.delete()
                else:
                    rec = cl.dao.Record.pull(k)
                    rec.data['url'] = v
                    rec.save()
        if 'url' in request.values: target = request.values['url']
        return redirect(target)


# this is a catch-all that allows us to present everything as a search
@app.route('/', methods=['GET','POST','DELETE'])
@app.route('/<path:path>', methods=['GET','POST','DELETE'])
def default(path=''):
    jsite = deepcopy(app.config['JSITE_OPTIONS'])
    if current_user.is_anonymous():
        jsite['loggedin'] = False
    else:
        jsite['loggedin'] = True

    url = '/' + path.lstrip('/').rstrip('/')
    if url == '/': url += 'index'
    if url.endswith('.json'): url = url.replace('.json','')
    rec = cl.dao.Record.pull_by_url(url)
        
    # if no record returned by URL check if it is a duplicate
    if not rec:
        duplicates = cl.dao.Record.check_duplicate(url)
        if duplicates and not current_user.is_anonymous():
            return deduplicate(path,duplicates,url)
        elif duplicates:
            abort(404)

    if request.method == 'GET':
        if util.request_wants_json():
            if not rec or (current_user.is_anonymous() and not app.config['PUBLIC_ACCESSIBLE_JSON']):
                abort(404)
            resp = make_response( rec.json )
            resp.mimetype = "application/json"
            return resp

        content = ''

        # build the content
        if rec:

            if not rec.data.get('accessible',False) and current_user.is_anonymous():
                abort(401)

            # update content from collaborative pad
            if jsite['collaborative'] and not rec.get('decoupled',False):
                c = requests.get('http://pads.cottagelabs.com/p/' + rec.id + '/export/txt')
                if rec.data.get('content',False) != c.text:
                    rec.data['content'] = c.text
                    rec.save()
            cont = rec.data.get('content','').encode('utf-8').decode('utf-8').replace(u'Â','') # works. leave it.
            # etherpads insert asterisks (*) sometimes when they see \t tabs, bless 'em
            cont = re.sub('\*<', '<', cont ) # it can break HTML tags
            cont = re.sub('(^\s*\*\s*$)', '', cont) # still get stand-alone * on blank lines with tabs in them

            content += markdown.markdown( cont )

            # if an embedded file url has been provided, embed it in the content too
            if rec.data.get('embed', False):
                if rec.data['embed'].find('/pub?') != -1 or rec.data['embed'].find('docs.google.com') != -1:
                    content += '<iframe id="embedded" src="' + rec.data['embed'] + '" width="100%" height="1000" style="border:none;"></iframe>'
                else:
                    content += '<iframe id="embedded" src="http://docs.google.com/viewer?url=' + urllib.quote_plus(rec.data['embed']) + '&embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
            
            # remove the content box from the js to save load - it is built separately
            jsite['data'] = rec.data
            del jsite['data']['content']

        elif current_user.is_anonymous():
            abort(404)
        else:
            # create a new record for a new page here
            newrecord = {
                'id': cl.dao.makeid(),
                'url': url,
                'title': url.split('/')[-1],
                'author': current_user.id,
                'content': '',
                'comments': False,
                'embed': '',
                'visible': False,
                'accessible': True,
                'editable': True,
                'image': '',
                'excerpt': '',
                'tags': [],
            }
            rec = cl.dao.Record(**newrecord)
            rec.save()
            jsite['newrecord'] = True
            jsite['data'] = newrecord                
        
        title = ''
        if rec:
            title = rec.data.get('title','')

        # if on the /search page, wire in the search everything box to the displayed search results
        search = False
        if url == '/search':
            search = True

        return render_template('index.html', content=content, title=title, search=search, jsite_options=json.dumps(jsite), offline=jsite['offline'])

    elif request.method == 'POST':
        if rec:
            if not rec.data.get('accessible',False) and current_user.is_anonymous():
                abort(401)
            else:
                # content is not always sent, to save transmission size. If not there, don't overwrite it to blank
                newdata = request.json
                if 'content' not in newdata: newdata['content'] = rec.data['content']
                rec.data = newdata
        else:
            if current_user.is_anonymous():
                abort(401)
            else:
                newrec = request.json
                rec = cl.dao.Record(**newrec)
        rec.save()
        resp = make_response( rec.json )
        resp.mimetype = "application/json"
        return resp
    
    elif request.method == 'DELETE':
        if current_user.is_anonymous():
            abort(401)
        try:
            rec.delete()
            return ""
        except:
            abort(404)


if __name__ == "__main__":
    cl.dao.initialise()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])

