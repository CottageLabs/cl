
from datetime import datetime

from portality.core import app

from portality.dao import DomainObject as DomainObject


from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

class Account(DomainObject, UserMixin):
    __type__ = 'account'

    def set_password(self, password):
        self.data['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.data['password'], password)

    @property
    def is_super(self):
        return not self.is_anonymous() and self.id in app.config['SUPER_USER']
    
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

    
# a special object that allows a search onto all index types - FAILS TO CREATE INSTANCES
class Everything(DomainObject):
    __type__ = 'everything'

    @classmethod
    def target(cls):
        t = 'http://' + str(app.config['ELASTIC_SEARCH_HOST']).lstrip('http://').rstrip('/') + '/'
        t += app.config['ELASTIC_SEARCH_DB'] + '/'
        return t


# a page manager object, with a couple of extra methods
class Pages(DomainObject):
    __type__ = 'pages'

    @classmethod
    def pull_by_url(cls,url):
        res = cls.query(q={"query":{"term":{'url.exact':url}}})
        if res.get('hits',{}).get('total',0) == 1:
            return cls(**res['hits']['hits'][0]['_source'])
        else:
            return None

    def update_from_form(self, request):
        newdata = request.json if request.json else request.values
        self.data['editable'] = False
        self.data['accessible'] = False
        self.data['visible'] = False
        self.data['comments'] = False
        for k, v in newdata.items():
            if k == 'tags':
                tags = []
                for tag in v.split(','):
                    if len(tag) > 0: tags.append(tag)
                self.data[k] = tags
            elif k in ['editable','accessible','visible','comments']:
                if v == "on":
                    self.data[k] = True
                else:
                    self.data[k] = False
            elif k not in ['submit']:
                self.data[k] = v
        if not self.data['url'].startswith('/'):
            self.data['url'] = '/' + self.data['url']
        if 'title' not in self.data or self.data['title'] == "":
            self.data['title'] = 'untitled'

    def save_from_form(self, request):
        self.update_from_form(request)
        self.save()
    
    
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





