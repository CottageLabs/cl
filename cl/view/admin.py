import json, time

from flask import Blueprint, request, url_for, flash, redirect, abort, make_response
from flask import render_template
from flask.ext.login import current_user
from copy import deepcopy

from cl import auth
from cl.core import app
import cl.util as util
import cl.dao


blueprint = Blueprint('admin', __name__)

# restrict everything in admin to logged in users
@blueprint.before_request
def restrict():
    if current_user.is_anonymous():
        abort(401)

# get dropdown info from terms
def drops(model,keys=['name']):
    qry = {
        'query':{'match_all':{}},
        'size': 0,
        'facets':{}
    }
    if not isinstance(keys,list):
        keys = [keys]
    for key in keys:
        qry['facets'][key] = {"terms":{"field":key+app.config['FACET_FIELD'],"order":'term', "size":100000}}
    klass = getattr(cl.dao, model[0].capitalize() + model[1:] )
    r = klass().query(q=qry)
    results = []
    for key in keys:
        results = results + [i.get('term','') for i in r.get('facets',{}).get(key,{}).get("terms",[])]
    return results


# define the dropdowns to be used in the admin pages
def dropdowns():
    dropdowns = {
        "clpeople": [str(i['_source']['id']) for i in cl.dao.Account.query(q="*",size=1000000).get('hits',{}).get('hits',[])],
        "partners": [i['_source']['id'] for i in cl.dao.Account.query(terms={"partner":"yes"},size=1000000).get('hits',{}).get('hits',[])],
        "seniors": [i['_source']['id'] for i in cl.dao.Account.query(terms={"senior":"yes"},size=1000000).get('hits',{}).get('hits',[])],
        "contacts": drops('project',['externals','customer','funder']),
        "tags":drops('project',['tags'])
    }
    return dropdowns
    


# build an admin page where things can be done
@blueprint.route('/')
def index():
    opts = deepcopy(app.config['JSITE_OPTIONS'])
    opts['data'] = {"editable":False}
    return render_template('admin/index.html', jsite_options=json.dumps(opts), offline=opts['offline'])


# show/save a particular admin item or else redirect back up to default page behaviour
@blueprint.route('/project', methods=['GET','POST'])
#@blueprint.route('/<itype>/', methods=['GET','POST'])
@blueprint.route('/<itype>/<iid>', methods=['GET','POST','DELETE'])
def adminitem(itype,iid=False):
    opts = deepcopy(app.config['JSITE_OPTIONS'])
    opts['data'] = {"editable":False}
    if itype in ['project']:
        klass = getattr(cl.dao, itype[0].capitalize() + itype[1:] )
        if not iid and request.json:
            iid = request.json.get("id",False)
            if not iid:
                iid = request.json.get("name",'')
                if iid and 'companyname' in request.json:
                    iid += '_' + request.json["companyname"]
            if not iid:
                iid = request.json.get("reference",'')
                if iid:
                    exists = klass.pull(iid)
                    if exists:
                        iid = False
            if not iid:
                iid = cl.dao.makeid()

        if iid:
            if iid.endswith('.json'): iid = iid.replace('.json','')
            if iid == "new":
                rec = None
            else:
                rec = klass.pull(iid)
            if request.method == 'GET':
                if not util.request_wants_json():
                    return render_template('admin/project.html', jsite_options=json.dumps(opts), offline=opts['offline'], dropdowns=dropdowns(), jdropdowns=json.dumps(dropdowns()), record=rec)
                elif rec is not None:
                    resp = make_response( rec.json )
                    resp.mimetype = "application/json"
                    return resp
                else:
                    abort(404)
            elif rec and (request.method == 'DELETE' or ( request.method == "POST" and request.form.get('submit',False) == "delete")):
                rec.delete()
                time.sleep(300)
                return redirect(url_for('.index'))
            elif request.method == 'POST':
                if rec is None:
                    rec = klass()
                if itype in ['project']:
                    rec.save_from_form(request)
                else:
                    rec.data = request.json
                    rec.save()
                return render_template('admin/' + itype + '.html', jsite_options=json.dumps(opts), offline=opts['offline'], dropdowns=dropdowns(), jdropdowns=json.dumps(dropdowns()), record=rec)
                
        else:
            abort(404)
    else:
        abort(404)



