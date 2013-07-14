import json

from flask import Blueprint, request, url_for, flash, redirect, abort, make_response
from flask import render_template
from flask.ext.login import current_user
from copy import deepcopy

from cl import auth
from cl.core import app
import cl.util as util
import cl.dao


blueprint = Blueprint('sitemap', __name__)


@blueprint.route('/', methods=['GET','POST'])
def index():
    jsitemap = deepcopy(app.config['JSITE_OPTIONS'])
    jsitemap['facetview']['initialsearch'] = False
    jsitemap['editable'] = False

    if current_user.is_anonymous():
        return render_template('sitemap/sitemap.html', public=True, jsite_options=json.dumps(jsitemap), nosettings=True)
    else:
        if request.method == 'POST' and request.values.get('sitenav','') != '':
            out = open('cl/templates/sitemap/sitenav.html','w')
            out.write(request.values['sitenav'])
            out.close()
            flash('Site navigation has been updated')

        return render_template('sitemap/sitemap.html', public=False, jsite_options=json.dumps(jsitemap), nosettings=True)

@blueprint.route('.xml')
def xml():
    resp = render_template('sitemap/sitemap.xml')
    resp.mimetype = "application/xml"
    return resp

def generate_sitemap_xml(sitemap=False):
     # TODO: finish this, have it meet google sitemap / resourcesync reqs
     # add anything necessary to handle versioning for resourcesync above too
    pass
    

