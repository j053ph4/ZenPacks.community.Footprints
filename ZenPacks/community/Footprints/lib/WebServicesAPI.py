import re, os, sys
from ZSI.client import AUTH, Binding
from ZSI import TC
from lxml import objectify
 
 
class WebServicesAPI():
    """ Class to manage FP Web Services API
        connection parameters for SOAP method calls
    """
    def __init__(self, host, userid, password, verbose=False):
        self.host = host
        self.userid = userid
        self.password = password
        self.url = 'http://%s/MRcgi/MRWebServices.pl' % self.host
        self.namespace = 'http://%s/MRWebServices' % self.host
        self.auth = (AUTH.httpbasic, self.userid, self.password)
        if verbose == True:
            self.server = Binding(url=self.url, auth=self.auth, ns=self.namespace, tracefile=sys.stdout)
        else:
            self.server = Binding(url=self.url, auth=self.auth, ns=self.namespace)
        self.argumentHash = {}
        self.extraInfo = ''
        self.projectID = '%'
        self.mrID = '%'
        self.reset()
    
    def reset(self):
        """
            reset variables to defaults
        """
        self.argtype = 'hash'
        self.query = ''
        self.method = ''
        self.uri = ''
        self.xml = True
        self.expected = TC.Any()
        self.output = None
    
    def listWorkspaces(self):
        ''''''
        return self.search("SELECT Counter, CounterId FROM FPCounters WHERE Counter LIKE 'ProjectName%'")
    
    def listAssignees(self, users=False):
        ''''''
        query = "SELECT B.PROJECTID,A.VALUE_INT,A.VALUE_EXT FROM SCHEMA_FIELDVALUES AS A INNER JOIN SCHEMA_FIELDS AS B ON A.FIELD_ID = B.FIELD_ID WHERE B.FIELD_NAME LIKE 'mrASSIGNEES' AND A.VALUE_INT NOT IN (SELECT user_id FROM users) AND B.PROJECTID LIKE '%s'" % self.projectID
        if users == True:
            query = "SELECT B.PROJECTID,A.VALUE_INT,A.VALUE_EXT FROM SCHEMA_FIELDVALUES AS A INNER JOIN SCHEMA_FIELDS AS B ON A.FIELD_ID = B.FIELD_ID WHERE B.FIELD_NAME LIKE 'mrASSIGNEES' AND B.PROJECTID LIKE '%s'" % self.projectID
        return self.search(query)
    
    def listCustomFields(self):
        """
        """
        query = "SELECT DISTINCT FIELD_NAME FROM SCHEMA_FIELDS WHERE PROJECTID LIKE '%s' AND FIELD_NAME NOT LIKE '%s'" % (self.projectID, 'mr%')
        return self.search(query)
    
    def getIssueID(self, evid='%'):
        """ search for an issue
        """
        query = "SELECT mrID FROM Master%s WHERE mrALLDESCRIPTIONS LIKE '%s'" % (self.projectID, "%"+evid+"%")
        return self.search(query)
    
    def parseIssueDetails(self):
        self.results()
        print self.output
        data = {}
        for k,v in self.output.items():
            print k,v
            if v.values()[-1] is not 'xsd:string':
                data[k] = v.values()[-1]
        return data
    
    def createCI(self):
        """ create a new CI
        """
        self.argtype = 'hash'
        self.xml = False
        return self.submit('MRWebServices__createCI')
    
    def editCI(self):
        """ edit an existing CI
        """
        self.argtype = 'hash'
        self.xml = False
        return self.submit('MRWebServices__editCI')
    
    def createCIRelation(self):
        """ create a relation between 2 CIs
        """
        self.argtype = 'hash'
        self.xml = False
        return self.submit('MRWebServices__createCIRelation')
    
    def createIssue(self):
        """ create an issue
        """
        self.argtype = 'hash'
        self.xml = False
        return self.submit('MRWebServices__createIssue')
    
    def editIssue(self):
        """ edit an issue
        ""        """
        self.argtype = 'hash'
        self.xml = True
        return self.submit('MRWebServices__editIssue')
    
    def getIssueDetails(self):
        """ get issue details
        """
        self.xml = True
        self.argtype = 'details'
        return self.submit('MRWebServices__getIssueDetails')
    
    def linkIssues(self):
        """ link two issues together
        """
        self.xml = True
        return self.submit('MRWebServices__linkIssues')
    
    def createCIIssueLink(self):
        """ link an issue to a CI
        """
        self.xml = True
        return self.submit('MRWebServices__createCIIssueLink')
    
    def search(self,query):
        """ execs SQL query via Web Services
            and returns list of dicts
        """
        self.xml = False
        self.argtype = 'search'
        self.query = query
        return self.submit('MRWebServices__search')
    
    def submit(self, method):
        """ execute SOAP RPC against Web Services API
        """
        self.output = None
        self.method = method
        self.uri = "%s#%s" % (self.namespace, self.method)
        self.formatArgs()
        self.typecode = TC.Struct(self, self.arguments, pname=(self.uri,self.method))
        # determine whether output should be XML
        if self.xml == True:
            self.expected = TC.XML()
        else:
            self.expected = TC.Any()
        # submit RPC
        try:
            self.reply = self.server.RPC(None, None, self, wsaction=self.uri, replytype=self.expected)
        except:
            self.reply = None
        return self.results()
    
    def results(self):
        """
            decide how to return consistent results (dictionary)
        """
        if self.xml == True:
            try:
                print "trying XML tree"
                tree = objectify.fromstring(self.server.ReceiveRaw())
                return self.xmlToDict(self.findReturn(tree))
            except:
                print "XML tree failed, returning raw"
                return self.server.RecieveRaw()
        else:
            try:
                print "trying simple return"
                return self.reply['return']
            except:
                try:
                    print "trying Any return"
                    return self.server.Recieve(TC.Any())['return']
                except:
                    print "returning raw"
                    return self.server.RecieveRaw()
    
    def findReturn(self, tree):
        """
            descend through XML output until the 'return' output is found
        """
        if tree.tag != 'return':
            try:
                return self.findReturn(tree.getchildren()[0])
            except:
                pass
        return tree
    
    def xmlToDict(self, tree):
        """
            convert XML response to python dictionary
        """
        data = {}
        for o in tree.getchildren():
            data[o.tag] = o.text
        return data
    
    def formatArgs(self):
        '''
            set correct args for method call
        '''
        self.arguments = [TC.String('userid'), TC.String('password'), TC.String('extraInfo')]
        if self.argtype == 'search':
            self.arguments.append(TC.String('query'))
        elif self.argtype == 'details':
            try:
                self.projectID = self.argumentHash['projectID']
                self.mrID = self.argumentHash['mrID']
            except:
                pass
            self.arguments.append(TC.String('projectID'))
            self.arguments.append(TC.String('mrID'))
        else:
            self.arguments.append(TC.Any('argumentHash',aslist=True))
