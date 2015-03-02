
class Issue(object):
    ''''''
    def __init__(self):
        self.data = {'mandatory': {}, 'optional': {}}
        
    def createFields(self, project, title, status, priority, description ):
        self.data['mandatory'] = {
                     # mandatory
                    'projectID' : project, # Workspace number
                    'title' : title, # Title of issue
                    'status' : status, # Status in unfixed format
                    'priorityNumber' : priority, # Number for issue priority
                    #'priorityWords' : None, # Words representing priority
                    'description' : description, # Description in plain text
                    }
        
        self.data['optional'] = {
                    'assignees': None, # Reference to array of assignees (teams must be listed in fixed form, e.g., Tier__bOne)
                    'submitter' : None, # Userid of submitter
                    'permanentCCs' : None, # Reference to array of permanent CCs (userids or email addresses, with teams listed in fixed form)
                    'oneTimeCCs' : None, # Reference to array of one-time CCs (userids or email addresses, with teams listed in fixed form)
                    'mail' : None,
                    'projfields' : { 'Reporting__bSource' : 'Zenoss' }, # Reference to hash containing proj fields in form: fieldname=>fieldvalue, where fieldvalue is in the same form as a user would type it in from the web
                    'abfields' : None, # Reference to hash containing ab fields in form: fieldname=>fieldvalue, where fieldvalue is in the same form as a user would type it in from the web
                    'selectContact' : None, # Primary key value of contact in unfixed form
                     }
        
    def editFields(self, project, number):
        self.data['mandatory'] = {
                    'projectID' : project, # Project ID
                    'mrID' : number, # Issue ID
                    }
        
        self.data['optional'] = {
                    'status' : None,
                    'description' : None,
                    'title' : None,
                    'priorityNumber' : None,
                    'priorityWords' : None,
                    'assignees': None,
                    'submitter' : None,
                    'permanentCCs' : None,
                    'oneTimeCCs' : None,
                    'mail' : None, # dict
                    'projfields' : { 'Reporting__bSource' : 'Zenoss' },
                    'abfields' : None, #dict
                    'selectContact' : None,
                     }
    
    
    def mailArgs(self):
        '''
        0 turns email off
        '''
        return {
                'assignees' : 1,
                'contact' : 1,
                'permanentCCs' : 1,
                }
    
    def getArgs(self):
        '''
            return arguments suitable for SOAP query
        '''
        args= {}
        for k,v in self.data['mandatory'].items():
            if v is not None:  args[k] = v
        for k,v in self.data['optional'].items():
            if v is not None:  args[k] = v 
        return args


