import json, os

from flask import Blueprint, request, url_for, flash, redirect, abort, make_response
from flask import render_template
from flask.ext.login import current_user
from copy import deepcopy
import werkzeug

from cl.core import app
import cl.util as util


blueprint = Blueprint('media', __name__)


@blueprint.route('/')
def media():
    jsite = deepcopy(app.config['JSITE_OPTIONS'])
    jsite['data'] = False
    jsite['editable'] = False
    jsite['facetview']['initialsearch'] = False
    listing = os.listdir( app.config['MEDIA_FOLDER'] )
    if util.request_wants_json():
        response = make_response( json.dumps(listing,"","    ") )
        response.headers["Content-type"] = "application/json"
        return response
    else:
        # TODO: this may be obsoleted - or else add some sort of delete and other 
        # functionality to the media page display...
        files = ''
        for f in listing:
            if f.split('.')[-1] in ['png','jpg','jpeg','gif']:
                files += '<a rel="gallery" class="span2 thumbnail" href="/' + app.config['MEDIA_FOLDER'] + '/'
                files += f + '"><img src="/' + app.config['MEDIA_FOLDER'] + '/' + f + '" /></a>'
            else:
                files += '<div class="span2 thumbnail"><h3><a _target="blank" href="/' 
                files += app.config['MEDIA_FOLDER'] + '/' + f + '">' + f + '</a></h3></div>'
        return render_template('media/media.html', jsite_options=json.dumps(jsite), files=files)


@blueprint.route('/<path:path>', methods=['GET','POST'])
def medias(path=''):
    # TODO: this GET is just for dev. This should be a setting on the nginx server
    if request.method == 'GET':
        loc = app.config['MEDIA_FOLDER'] + '/' + path
        if app.config['DEBUG'] and os.path.isfile(loc):
            response = make_response(open(loc).read())
            response.headers["Content-type"] = "image"
            return response
        else:
            abort(404)
    
    elif request.method == 'POST':
        if not current_user.is_anonymous():
            # TODO: check the file type meets the allowed ones, and if so put it in media dir
            filename = werkzeug.secure_filename(path)
            out = open(app.config['MEDIA_FOLDER'] + '/' + filename, 'w')
            out.write(request.data)
            out.close()
            return ''
        else:
            abort(401)    

