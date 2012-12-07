import os, json, UserDict, requests, uuid
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from cl.core import app, current_user
import cl.util, cl.auth


def makeid():
    '''Create a new id for data object
    customise this if specific ID types are required'''
    return uuid.uuid4().hex
    
    
def initialise():
    mappings = app.config['MAPPINGS']
    for mapping in mappings:
        t = 'http://' + str(app.config['ELASTIC_SEARCH_HOST']).lstrip('http://').rstrip('/')
        t += '/' + app.config['ELASTIC_SEARCH_DB'] + '/' + mapping + '/_mapping'
        r = requests.get(t)
        if r.status_code == 404:
            r = requests.put(t, data=json.dumps(mappings[mapping]) )
            print r.text
    firstsu = app.config['SUPER_USER'][0]
    if not Account.pull(firstsu):
        su = Account(id=app.config['SUPER_USER'][0])
        su.set_password(firstsu)
        su.save()
        print 'superuser account named - ' + firstsu + ' created. default password matches username. Change it.'
    if not os.path.exists('media'):
        os.makedirs('media')
        print 'created empty media directory. If you are using dropbox syncing, ensure this folder (and the content folder if desired) are symlinked into your dropbox tracked folder'
    if not os.path.exists('content'):
        os.makedirs('content')
        print 'created empty content directory. If you intend to sync this with a git repo, you should recreate it using git.'
    try:
        sitemap = json.load(open('cl/templates/sitemap/sitemap.json'))
        out = open('cl/templates/sitemap/sitenav.html')
        out.close()
        out = open('cl/templates/sitemap/sitemap_private.html')
        out.close()
        out = open('cl/templates/sitemap/sitemap_public.html')
        out.close()
    except:
        out = open('cl/templates/sitemap/sitemap.json','w')
        out.write('{}')
        out.close()
        out = open('cl/templates/sitemap/sitenav.html','w')
        out.close()
        out = open('cl/templates/sitemap/sitemap_private.html','w')
        out.close()
        out = open('cl/templates/sitemap/sitemap_public.html','w')
        out.close()
        print ("created default emtpy sitemaps")


def get_user():
    try:
        usr = current_user.id
    except:
        usr = "anonymous"
    return usr


class InvalidDAOIDException(Exception):
    pass
    
    
class DomainObject(UserDict.IterableUserDict):
    __type__ = None

    def __init__(self, **kwargs):
        if '_source' in kwargs:
            self.data = dict(kwargs['_source'])
            self.meta = dict(kwargs)
            del self.meta['_source']
        else:
            self.data = dict(kwargs)
            
    @classmethod
    def target(cls):
        t = 'http://' + str(app.config['ELASTIC_SEARCH_HOST']).lstrip('http://').rstrip('/') + '/'
        t += app.config['ELASTIC_SEARCH_DB'] + '/' + cls.__type__ + '/'
        return t
    
    @property
    def id(self):
        return self.data.get('id', None)
        
    @property
    def version(self):
        return self.meta.get('_version', None)

    @property
    def json(self):
        return json.dumps(self.data)

    def save(self):
        if 'id' in self.data:
            id_ = self.data['id'].strip()
        else:
            id_ = makeid()
            self.data['id'] = id_
        
        self.data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H%M")

        if 'created_date' not in self.data:
            self.data['created_date'] = datetime.now().strftime("%Y-%m-%d %H%M")
            
        if 'author' not in self.data:
            self.data['author'] = get_user()

        r = requests.post(self.target() + self.data['id'], data=json.dumps(self.data))

    @classmethod
    def pull(cls, id_):
        '''Retrieve object by id.'''
        if id_ is None:
            return None
        try:
            out = requests.get(cls.target() + id_)
            if out.status_code == 404:
                return None
            else:
                return cls(**out.json)
        except:
            return None

    @classmethod
    def keys(cls,mapping=False,prefix=''):
        # return a sorted list of all the keys in the index
        if not mapping:
            mapping = cls.query(endpoint='_mapping')[cls.__type__]['properties']
        keys = []
        for item in mapping:
            if mapping[item].has_key('fields'):
                for item in mapping[item]['fields'].keys():
                    if item != 'exact' and not item.startswith('_'):
                        keys.append(prefix + item + app.config['FACET_FIELD'])
            else:
                keys = keys + cls.keys(mapping=mapping[item]['properties'],prefix=prefix+item+'.')
        keys.sort()
        return keys
        
    @classmethod
    def query(cls, recid='', endpoint='_search', q='', terms=None, facets=None, **kwargs):
        '''Perform a query on backend.

        :param recid: needed if endpoint is about a record, e.g. mlt
        :param endpoint: default is _search, but could be _mapping, _mlt, _flt etc.
        :param q: maps to query_string parameter if string, or query dict if dict.
        :param terms: dictionary of terms to filter on. values should be lists. 
        :param facets: dict of facets to return from the query.
        :param kwargs: any keyword args as per
            http://www.elasticsearch.org/guide/reference/api/search/uri-request.html
        '''
        if recid and not recid.endswith('/'): recid += '/'
        if isinstance(q,dict):
            query = q
        elif q:
            query = {'query': {'query_string': { 'query': q }}}
        else:
            query = {'query': {'match_all': {}}}

        if facets:
            if 'facets' not in query:
                query['facets'] = {}
            for k, v in facets.items():
                query['facets'][k] = {"terms":v}

        if terms:
            boolean = {'must': [] }
            for term in terms:
                if not isinstance(terms[term],list): terms[term] = [terms[term]]
                for val in terms[term]:
                    obj = {'term': {}}
                    obj['term'][ term ] = val
                    boolean['must'].append(obj)
            if q and not isinstance(q,dict):
                boolean['must'].append( {'query_string': { 'query': q } } )
            elif q and 'query' in q:
                boolean['must'].append( query['query'] )
            query['query'] = {'bool': boolean}

        for k,v in kwargs.items():
            query[k] = v

        if endpoint in ['_mapping']:
            r = requests.get(cls.target() + recid + endpoint)
        else:
            r = requests.post(cls.target() + recid + endpoint, data=json.dumps(query))
        return r.json

    def accessed(self):
        if 'last_access' not in self.data:
            self.data['last_access'] = []
        self.data['last_access'].insert(0, { 'user':get_user(), 'date':datetime.now().strftime("%Y-%m-%d %H%M") } )        
        r = requests.put(self.target() + self.data['id'], data=json.dumps(self.data))

    def delete(self):        
        r = requests.delete(self.target() + self.id)


class Record(DomainObject):
    __type__ = 'record'

    @classmethod
    def pull_by_url(cls,url):
        res = cls.query(q='url.exact:' + url)
        if res['hits']['total'] == 1:
            return cls(**res['hits']['hits'][0]['_source'])
        else:
            return None

    @classmethod
    def check_duplicate(cls,url):
        res = cls.query(q='url.exact:' + url)
        if res['hits']['total'] > 1:
            return [i['_source'] for i in res['hits']['hits']]
        else:
            return None


class Account(DomainObject, UserMixin):
    __type__ = 'account'

    def set_password(self, password):
        self.data['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.data['password'], password)

    @property
    def is_super(self):
        return cl.auth.user.is_super(self)
    

