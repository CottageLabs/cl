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
from cl.view.media import blueprint as media
from cl import auth
from copy import deepcopy


app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(sitemap, url_prefix='/sitemap')
app.register_blueprint(media, url_prefix='/media')


@login_manager.user_loader
def load_account_for_login_manager(userid):
    out = cl.dao.Account.pull(userid)
    return out

@app.context_processor
def set_current_user():
    """ Set some template context globals. """
    return dict(current_user=current_user)

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
def query(path='Record'):
    pathparts = path.split('/')
    subpath = pathparts[0]
    if subpath.lower() == 'account':
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
        

@app.route('/deduplicate', methods=['GET', 'POST'])
def deduplicate(path='',duplicates=[],target='/'):
    if current_user.is_anonymous():
        abort(401)
    elif request.method == 'GET':
        jsitem = deepcopy(app.config['JSITE_OPTIONS'])
        jsitem['facetview']['initialsearch'] = False
        return render_template('deduplicate.html', jsite_options=json.dumps(jsitem), duplicates=duplicates, url=target)
    elif request.method == 'POST':
        # update the submittede record
        #try:
        for k,v in request.values.items():
            if v and v not in ['url', 'submit']:
                rec = cl.dao.Record.pull(k)
                rec.data['url'] = v
                rec.save()
        if 'url' in request.values: target = request.values['url']
        return redirect(target)
        #except:
        #    abort(404)


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
        
    # TODO: these catches are here just to test for old URLs from old site versions.
    # THIS SHOULD BE REMOVED EVENTUALLY, AND NOT USED ANYWHERE ELSE
    if not rec:
        ident = '___' + path.rstrip('/').replace('/', '___')
        if ident == '___': ident += 'index'
        if ident.endswith('.json'): ident = ident.replace('.json','')
        rec = cl.dao.Record.pull(ident)
    if not rec and len(url.split('/')) == 1:
        rec = cl.dao.Record.pull_by_url('/news/' + url)
        if rec:
            return redirect(rec['url'])
    if not rec and url.startswith('author'):
        return redirect( url.replace('author','people') )

    # if no record returned by URL check if it is a duplicate
    if not rec:
        duplicates = cl.dao.Record.check_duplicate(url)
        if duplicates and not current_user.is_anonymous():
            return deduplicate(path,duplicates,url)
        elif duplicates:
            abort(404)

    if request.method == 'GET':
        if util.request_wants_json():
            if not rec or current_user.is_anonymous():
                abort(404)
            resp = make_response( rec.json )
            resp.mimetype = "application/json"
            return resp

        content = ''

        # build the content unless it is being done by the js (unlikely)
        if rec and not jsite['jspagecontent']:

            if not rec.data.get('accessible',False) and current_user.is_anonymous():
                abort(401)

            # update content from collaborative pad
            if jsite['collaborative'] and not rec.get('decoupled',False):
                c = requests.get('http://pads.cottagelabs.com/p/' + rec.id + '/export/txt')
                if rec.data.get('content',False) != c.text:
                    rec.data['content'] = c.text
                    rec.save()
            content += markdown.markdown( rec.data.get('content','') )

            # this is a temporary catch from index errors - to be removed
            if not rec.data['embed'] or rec.data['embed'] == 'false':
                rec.data['embed'] = ""
                rec.save()

            # embed any file set as to be embedded
            if rec.data.get('embed', False):
                if rec.data['embed'].find('/pub?') != -1 or rec.data['embed'].find('docs.google.com') != -1:
                    content += '<iframe id="embedded" src="' + rec.data['embed'] + '" width="100%" height="1000" style="border:none;"></iframe>'
                else:
                    content += '<iframe id="embedded" src="http://docs.google.com/viewer?url=' + urllib.quote_plus(rec.data['embed']) + '&embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
            
            # setup search display
            if rec.data.get('search',{}).get('options',False):
                jsite['facetview'].update(rec.data['search']['options'])
            if rec.data['search']['format'] == 'features':
                jsite['facetview']['result_display'] = [
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
                ]
                jsite['facetview']['searchwrap_start'] = '<div class="row-fluid"><div class="well" style="margin-top:20px;"><div id="facetview_results" class="clearfix">'
                jsite['facetview']['searchwrap_end'] = '</div></div></div>'
                jsite['facetview']['resultwrap_start'] = '<div class="span3 feature_span">'
                jsite['facetview']['resultwrap_end'] = '</div>'
            if rec.data['search']['format'] == 'list':
                jsite['facetview']['searchwrap_start'] = '<table id="facetview_results" class="table table-bordered table-striped table-condensed">'
                jsite['facetview']['searchwrap_end'] = '</table>'
                jsite['facetview']['resultwrap_start'] = '<tr><td>'
                jsite['facetview']['resultwrap_end'] = '</td></tr>'
            if rec.data['search'].get('onlytitles',False):
                jsite['facetview']['result_display'] = [
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
                ]
            
            # as the page is not being built by js, remove the content to save load
            jsite['data'] = rec.data
            del jsite['data']['content']

        elif rec:
            jsite['data'] = rec.data

        elif current_user.is_anonymous():
            # TODO: trigger a search for alternative content if not logged in
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
                'search': {
                    'format':'panels',
                    'position':'hidden',
                    'options': {}
                }
            }
            rec = cl.dao.Record(**newrecord)
            rec.save()
            jsite['newrecord'] = True
            jsite['data'] = newrecord
                
        
        title = ''
        if rec:
            title = rec.data.get('title','')
        
        search = False
        if url == '/search':
            search = True

        return render_template('index.html', content=content, title=title, search=search, jsite_options=json.dumps(jsite))

    elif request.method == 'POST':
        if rec:
            if not rec.data.get('accessible',False) and current_user.is_anonymous():
                abort(401)
            else:
                rec.data = request.json
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
            flash('you killed it! sad face...')
            return redirect('/')
        except:
            abort(404)


if __name__ == "__main__":
    cl.dao.initialise()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])

