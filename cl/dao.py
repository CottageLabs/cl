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
    try:
        out = open('cl/templates/sitemap/sitenav.html')
        out.close()
    except:
        out = open('cl/templates/sitemap/sitenav.html','w')
        out.close()
        print ("created default emtpy sitemap")


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

        return requests.post(self.target() + self.data['id'], data=json.dumps(self.data))

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
                return cls(**out.json())
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
            if k == '_from':
                query['from'] = v
            else:
                query[k] = v

        if endpoint in ['_mapping']:
            r = requests.get(cls.target() + recid + endpoint)
        else:
            r = requests.post(cls.target() + recid + endpoint, data=json.dumps(query))
        return r.json()

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
        res = cls.query(q={"query":{"term":{'url.exact':url}}})
        if res.get('hits',{}).get('total',0) == 1:
            return cls(**res['hits']['hits'][0]['_source'])
        else:
            return None

    @classmethod
    def check_duplicate(cls,url):
        res = cls.query(q={"query":{"term":{'url.exact':url}}},size=1000000)
        print res
        if res.get('hits',{}).get('total',0) > 1:
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
    
    @property
    def projects(self):
        comms = self.commitments()
        p = []
        for item in comms:
            if item['data']['project'] not in p:
                p.append(Project.pull(item['data']['project']))
        return p
    
    def share(self,datefrom='',dateto='',projects=[]):
        # return the total amount due to this partner during given date range, filtered by project ID list if necessary
        if not projects:
            projects = [i.id for i in self.projects]
        commitments = Commitment().query(terms={"name":self.id,"project":projects})# add a date filter
        financials = Finance().query(terms={"name":self.id,"project":projects}) # add a date filter to this
        # list and total these values and return them
        # perhaps include expenses in this
        pass
    
    def expenses(self,datefrom='',dateto='',projects=[]):
        # return the total expenses due back to this partner during given date range, filtered by project list if necessary
        pass
    
    def commitments(self,datefrom='',dateto=''):
        c = [Commitment.pull(i['_source']['id']) for i in Commitment.query(terms={'who':self.id},size=100000,sort={"start":{"order":"desc"}}).get('hits',{}).get('hits',[])]
        
        if len(c) == 0:
            return []
        else:
            if not datefrom: datefrom = c[-1]['data']['start']
            if not dateto:
                cto = [Commitment.pull(i['_source']['id']) for i in Commitment.query(terms={'who':self.id},size=1,sort={"end":{"order":"desc"}}).get('hits',{}).get('hits',[])]
                dateto = cto[0]['data']['end']
            cs = []
            for item in c:
                if self.data["end"] > datefrom and self.data["start"] < dateto:
                    cs.append(item)
            return cs
        
    def committed(self,datefrom='',dateto=''):
        comms = self.commitments(datefrom,dateto)
        tc = 0
        for c in comms:
            pass # % score of commitment between date range
        return tc
    

class Project(DomainObject):
    __type__ = 'project'

    def save_from_form(self, request):
        rec = {
            "notes": [],
            "commitments": [],
            "financials": []
        }

        for k,v in enumerate(request.form.getlist('note_date')):
            if v is not None and len(v) > 0 and v != " ":
                try:
                    note = {
                        "date": v,
                        "author": current_user.id,
                        "note": request.form.getlist('note_note')[k]
                    }
                    if len(note['date']) == 0: del note['date']
                    rec["notes"].append(note)
                except:
                    pass
        
        for k,v in enumerate(request.form.getlist('commitment_name')):
            if v is not None and len(v) > 0 and v != " ":
                try:
                    commitment = {
                        "name": v,
                        "datefrom": request.form.getlist('commitment_datefrom')[k],
                        "dateto": request.form.getlist('commitment_dateto')[k],
                        "time": request.form.getlist('commitment_time')[k],
                        "share": request.form.getlist('commitment_share')[k]
                    }
                    if len(commitment['datefrom']) == 0: del commitment['datefrom']
                    if len(commitment['dateto']) == 0: del commitment['dateto']
                    rec['commitments'].append(commitment)
                except:
                    pass

        for k,v in enumerate(request.form.getlist('financial_type')):
            if v is not None and len(v) > 0 and v != " ":
                try:
                    financial = {
                        "type": v,
                        "description": request.form.getlist('financial_description')[k],
                        "reference": request.form.getlist('financial_reference')[k],
                        "datedue": request.form.getlist('financial_datedue')[k],
                        "cost": request.form.getlist('financial_cost')[k],
                        "vat": request.form.getlist('financial_vat')[k],
                        "dateapproved": request.form.getlist('financial_dateapproved')[k]
                    }
                    if len(financial['datedue']) == 0: del financial['datedue']
                    rec["financials"].append(financial)
                except:
                    pass

        for key in request.form.keys():
            if not key.startswith("commitment_") and not key.startswith("financial_") and not key.startswith("note_") and key not in ['submit']:
                if key == 'tags':
                    val = request.form[key].split(",")
                else:
                    val = request.form[key]
                if val == "on":
                    rec[key] = True
                elif val == "off":
                    rec[key] = False
                elif key in ["datefrom","dateto"] and len(val) == 0:
                    pass
                else:
                    rec[key] = val

        if self.id is not None: rec['id'] = self.id
        self.data = rec
        self.save()


    @property
    def commitments(self):
        return [Commitment.pull(i['_source']['id']) for i in Commitment.query(terms={'project':self.id},size=100000,sort={"start":{"order":"desc"}}).get('hits',{}).get('hits',[])]
        
    @property
    def financials(self):
        return [Finance.pull(i['_source']['id']) for i in Finance.query(terms={'project':self.id},size=100000,sort={"created_date":{"order":"desc"}}).get('hits',{}).get('hits',[])]

    @property
    def outgoings(self):
        dets = {"total":0,"transactions":[]}
        for item in self.financials:
            if item.data['cost'] < 0:
                dets["total"] += item.data['cost']
                dets["transactions"].append((item.data['date'],item.data['cost']))
        return dets

    @property
    def income(self):
        dets = {"total":0,"transactions":[]}
        for item in self.financials:
            if item.data['cost'] > 0:
                dets["total"] += item.data['cost']
                dets["transactions"].append((item.data['date'],item.data['cost']))
        return total

    @property
    def report(self):
        today = datetime.now().strftime("%Y-%m-%d %H%M")        
        res = {
            "status": self.data["status"],
            "state": "green", # one of green, yellow, red
            "warnings":[], # a human-readable list of things that are wrong, with embedded links where relevant
            "totalincome": self.income["total"],
            "totaloutgoings": self.outgoings["total"],
            "financials": self.financials,
            "commitments": self.commitments,
            "data": self.data
        }

        if self.data['datefrom'] < today and self.data["status"] in ["proposed","current"]:
            if len(self.commitments) == 0:
                res["state"] = "yellow"
                res["warnings"].append("Project start date has passed but there are no people commitments listed for it")
            if len(self.financials) == 0:
                res["state"] = "yellow"
                res["warnings"].append("Project start date has passed but there are no financial transactions listed for it")

        # check if any incoming invoice events have occurred and no subsequent payments out
        outgoingpaymentfound = False
        incomingpaymentrequestfound = False 
        for item in self.financials:
            if outgoingpaymentfound or incomingpaymentrequestfound: # don't need to go further
                break
            elif True: # if this is a request for payment, note it
                incomingpaymentrequestfound = True
            elif False: # if this is an outoing payment, note it
                outgoingpaymentfound = True
        if incomingpaymentrequestfound and not outgoingpaymentfound:
            res["state"] = "yellow"
            res["warnings"].append("There is at least one incoming payment request for which payment has not yet been made")

        # check if any of our invoices are more than 30 days since sending out, but not yet paid
        for item in self.financials:
            if item.data['event'] == "":
                if item.data["created_date"] < today - 30:
                    res["state"] = "yellow"
                    res["warnings"].append("There is at least one invoice issued more than 30 days ago for which payment has not yet been received")
                    
        
        # check if any project team members are extremely busy over the remaining duration
        for item in self.commitments:
            person = Account.pull(item.data["who"])
            if person.committed(today, self.data["dateto"]) > 95:
                res["state"] = "yellow"
                res["warnings"].append("Team member " + person.id + " is more than 95% committed during the remaining duration of this project")

        # check if total costs paid out are approaching total budget
        if self.outgoings > self.data["budget"] * .8:
            res["state"] = "yellow"
            res["warnings"].append("The total outgoings on this project are already more than 80% of total available budget")

        # check status against end date, and check if status is late
        if project.data['status'] == "current" and project.data["dateto"] < today:
            res["state"] = "red"
            res["warnings"].append("Project status is listed as current but project end date has passed")

        return res




