import json, os

from flask import Blueprint, request, url_for, flash, redirect, abort, make_response
from flask import render_template
from flask.ext.login import current_user
from copy import deepcopy
import werkzeug

from cl.core import app
import cl.util as util


blueprint = Blueprint('media', __name__)


mediadir = os.path.dirname(os.path.abspath(__file__)).replace('/cl/view','/') + app.config['MEDIA_FOLDER']

@blueprint.route('.json')
@blueprint.route('/')
def media():
    jsite = deepcopy(app.config['JSITE_OPTIONS'])
    jsite['data'] = False
    jsite['editable'] = False
    jsite['facetview']['initialsearch'] = False
    listing = os.listdir( mediadir )
    if util.request_wants_json():
        response = make_response( json.dumps(listing,"","    ") )
        response.headers["Content-type"] = "application/json"
        return response
    else:
        return render_template('media/media.html', jsite_options=json.dumps(jsite), files=sorted(listing, key=str.lower), nosettings=True)



@blueprint.route('/<path:path>', methods=['GET','POST','DELETE'])
def medias(path=''):
    if request.method == 'GET':
        # NOTE: this is only an alternative for when running in debug mode - it delivers images from media folder successfully
        # otherwise you should set your web server (nginx, apache, whatever) to serve GETs on /media/.*
        loc = mediadir + '/' + path
        if app.config['DEBUG'] and os.path.isfile(loc):
            response = make_response(open(loc).read())
            response.headers["Content-type"] = "image"
            return response
        else:
            abort(404)
    
    elif request.method == 'POST' and not current_user.is_anonymous():
        # TODO: check the file type meets the allowed ones, and if so put it in media dir
        filename = werkzeug.secure_filename(path)
        out = open(mediadir + '/' + filename, 'w')
        out.write(request.data)
        out.close()
        return ''

    elif request.method == 'DELETE' and not current_user.is_anonymous():
        try:
            loc = mediadir + '/' + path
            if os.path.isfile(loc):
                os.remove(loc)
        except:
            pass
        return ''

    else:
        abort(401)    

