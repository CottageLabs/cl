import json, requests
from flask import Flask, jsonify, json, request, redirect, abort, make_response
from flask import render_template, flash
from flask.views import View, MethodView
from flask.ext.login import login_user, current_user
import markdown
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
                abort(500)
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
        resp = make_response( json.dumps(klass().mapping()) )
    elif len(pathparts) == 2 and pathparts[1] not in ['_mapping','_search']:
        if request.method == 'POST':
            abort(401)
        else:
            rec = klass().pull(pathparts[1])
            if rec:
                resp = make_response( rec.json )
            else:
                abort(404)
    else:
        # TODO: add check for anonymous user
        # if so, add AND access:public AND listed:true to search params
        if request.method == "POST":
            qs = request.json
        else:
            qs = request.query_string
        resp = make_response( json.dumps(klass().query(qs=qs)) )
    resp.mimetype = "application/json"
    return resp
        
        
# this is a catch-all that allows us to present everything as a search
@app.route('/', methods=['GET','POST','DELETE'])
@app.route('/<path:path>', methods=['GET','POST','DELETE'])
def default(path=''):
    jsite = deepcopy(app.config['JSITE_OPTIONS'])
    if current_user.is_anonymous():
        jsite['loggedin'] = False
    else:
        jsite['loggedin'] = True

    ident = '___' + path.rstrip('/').replace('/', '___')
    if ident == '___': ident += 'index'
    comments = False
    rec = cl.dao.Record.pull(ident)
    
    # TODO: this catch is here just to test for old URLs from old site.
    # THIS SHOULD BE REMOVED EVENTUALLY, AND NOT USED ANYWHERE ELSE
    if not rec and len(ident.split('___')) == 2:
        ident = '___news' + ident
        rec = cl.dao.Record.pull(ident)
        if rec:
            return redirect(rec['url'])
    if not rec and path.startswith('author'):
        return redirect( path.replace('author','people') )

    if request.method == 'GET':
        if util.request_wants_json():
            if not rec or current_user.is_anonymous():
                abort(404)
            resp = make_response( rec.json )
            resp.mimetype = "application/json"
            return resp

        content = ''

        if rec and not jsite['jspagecontent']:

            if not rec.data.get('accessible',False) and current_user.is_anonymous():
                abort(401)

            if jsite['collaborative']:
                c = requests.get('http://pads.cottagelabs.com/p/' + rec.id + '/export/txt')
                rec.data['content'] = c.text
            content += markdown.markdown( rec.data.get('content','') )

            if rec.data.get('embed', False):
                # check for dropbox and repo embeds too - consider having auth
                # TODO: change this to being a direct call for the content, then process and output
                if not rec.data['embed'].find('/pub?') and not rec.data['embed'].find('docs.google.com'):
                    content += '<iframe id="embedded" src="http://docs.google.com/viewer?url=' + rec.data['embed'] + '&embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
                else:
                    content += '<iframe id="embedded" src="' + rec.data['embed'] + '&amp;embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
            
            if rec.data.get('search',{}).get('hidden',False):
                jsite['facetview']['initialsearch'] = False
            else:
                jsite['facetview']['initialsearch'] = True
            if rec.data.get('search',{}).get('options',False):
                jsite['facetview'].update(rec.data['search']['options'])
            if rec.data['search']['format'] == 'list':
                jsite['facetview']['searchwrap_start'] = '<table id="facetview_results" class="table table-bordered table-striped table-condensed">'
                jsite['facetview']['searchwrap_end'] = '</table>'
                jsite['facetview']['resultwrap_start'] = '<tr><td>'
                jsite['facetview']['resultwrap_end'] = '</td></tr>'
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

            jsite['data'] = rec.data

        elif rec:
            jsite['data'] = rec.data

        else:
            # TODO: trigger a search for alternative content if not logged in
            jsite['data'] = False
            if current_user.is_anonymous():
                abort(404)
        
        return render_template('index.html', content=content, title=rec.data.get('title',''), jsite_options=json.dumps(jsite))

    elif request.method == 'POST':
        if rec:
            if rec.data.get('access','') == 'private' and current_user.is_anonymous():
                abort(401)
            else:
                rec.data = request.json
        else:
            if current_user.is_anonymous():
                abort(401)
            else:
                newrec = request.json
                newrec['id'] = ident
                rec = cl.dao.Record(**newrec)
        rec.save()
        resp = make_response( rec.json )
        resp.mimetype = "application/json"
        return resp
    
    elif request.method == 'DELETE':
        if current_user.is_anonymous():
            abort(401)
        try:
            # TODO: need to add a remove from sitemap/nav etc if listed
            # maybe this should be in the delete method of a record
            rec.delete()
            flash('you killed it! sad face...')
            return redirect('/')
        except:
            abort(404)


if __name__ == "__main__":
    cl.dao.initialise()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])

