import json

from flask import Blueprint, request, flash, abort, make_response
from flask import render_template, redirect, url_for
from flask.ext.login import current_user

from portality.core import app
import portality.models as models
import portality.util as util

from portality.view.forms import dropdowns


blueprint = Blueprint('admin', __name__)


# restrict everything in admin to logged in users
@blueprint.before_request
def restrict():
    if current_user.is_anonymous():
        abort(401)    
    

# build an admin page where things can be done
@blueprint.route('/')
def index():
    return render_template('admin/index.html')


# show/save a particular admin item or show the default page for the admin item
@blueprint.route('/project', methods=['GET','POST'])
#@blueprint.route('/<itype>/', methods=['GET','POST'])
@blueprint.route('/<itype>/<iid>', methods=['GET','POST','DELETE'])
def adminitem(itype,iid=False):
    #try:
    klass = getattr(models, itype[0].capitalize() + itype[1:] )

    if iid:
        if iid.endswith('.json'): iid = iid.replace('.json','')
        if iid == "new":
            rec = None
        else:
            rec = klass.pull(iid)
        if request.method == 'GET':
            if not util.request_wants_json():
                return render_template(
                    'admin/' + itype + '.html', 
                    record=rec,
                    dropdowns = {
                        "clpeople": dropdowns('account','id'),
                        "partners": [i['_source']['id'] for i in models.Account.query(terms={"partner":"yes"},size=1000).get('hits',{}).get('hits',[])],
                        "seniors": [i['_source']['id'] for i in models.Account.query(terms={"senior":"yes"},size=1000).get('hits',{}).get('hits',[])],
                        "contacts": dropdowns('project',['externals','customer','funder']),
                        "tags":dropdowns('project',['tags'])
                    }
                )
            elif rec is not None:
                resp = make_response( rec.json )
                resp.mimetype = "application/json"
                return resp
            else:
                abort(404)

        elif ( rec and (request.method == 'DELETE' or 
                ( request.method == "POST" and 
                request.form.get('submit',False).lower() == "delete")) ):
            rec.delete()
            flash('Deleted')
            return redirect(url_for('.index'))

        elif request.method == 'POST':
            if rec is None:
                rec = klass()
            rec.save_from_form(request)
            if iid == "new":
                flash('Created')
                return redirect(url_for('.index') + itype + '/' + rec.id)
            else:
                flash('Updated')
                return redirect(url_for('.index') + itype + '/' + iid)
            
    else:
        return redirect(url_for('.index') + itype + '/new')
    #except:
    #    abort(404)




