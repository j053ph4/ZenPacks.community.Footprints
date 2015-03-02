# Copyright (c) 2013, Agero, Inc. <info@agero.com>

import json
import urllib2

import logging
log = logging.getLogger("zen.footprints.actions")

import Globals

from zope.interface import implements, providedBy
from zenoss.protocols.protobufs.zep_pb2 import STATUS_ACKNOWLEDGED

from Products.ZenModel.UserSettings import GroupSettings
from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenUtils.ProcessQueue import ProcessQueue
from Products.Zuul import getFacade, listFacades

from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import IActionBase, ActionExecutionException
from Products.ZenModel.actions import  processTalSource,_signalToContextDict
#from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION

from ZenPacks.community.Footprints.interfaces import IFootprintsEventsAPIActionContentInfo
from ZenPacks.community.Footprints.constants import EventType, enum

from ZenPacks.community.Footprints.lib.WebServicesAPI import *
from ZenPacks.community.Footprints.routers import *

from ZenPacks.community.ZenossAPI.lib.ZenossHandler import *


NotificationProperties = enum(PROJECTID='projectid', PROJECTNAME='projectname', SUMMARY='summary', DESCRIPTION='description',
                              INCIDENT_KEY='incident_key', DETAILS='details')

REQUIRED_PROPERTIES = [NotificationProperties.PROJECTID, NotificationProperties.PROJECTNAME, NotificationProperties.SUMMARY,
                       NotificationProperties.DESCRIPTION, NotificationProperties.INCIDENT_KEY]

API_TIMEOUT_SECONDS = 40

class FootprintsEventsAPIAction(IActionBase,WebServicesAPI):
    """
    Derived class to contact Footprints's SOAP API when a notification is
    triggered.
    """
    implements(IAction)

    id = 'footprints'
    name = 'Footprints'
    actionContentInfo = IFootprintsEventsAPIActionContentInfo

    shouldExecuteInBatch = False

    def __init__(self):
        super(FootprintsEventsAPIAction, self).__init__()
    
    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)
        self.dmd = dmd
        rtr = FootprintsServerRouter(dmd)
        self.account = rtr.get_account_settings().data['data']
        self.footprints = WebServicesAPI(self.account['server'], self.account['user'], self.account['password'])
        #self.eventField = 'ZenossEventID'
        self.zenoss = ZenossHandler('localhost', 'admin', 'z3n055', False)
        self.zep = getFacade('zep')

    def execute(self, notification, signal):
        """
        """
        print "CONTENT: %s" % notification.content
        #self.footprints.projectID = 8
        self.footprints.projectID = notification.content[NotificationProperties.PROJECTID]
        print "PROJECT ID: %s" % self.footprints.projectID
        # determine what type of action to take
        if signal.clear:
            self.eventType = EventType.CLOSE
        else:
            self.eventType = EventType.OPEN
        
        print "EVENT TYPE: %s" % self.eventType 
        self.details = {}
        
        #self.details['summary'] = notification.content[NotificationProperties.SUMMARY]
        # Set up the TALES environment
        environ = {'dmd': notification.dmd, 'env':None}
        
        actor = signal.event.occurrence[0].actor
        
        device = None
        if actor.element_uuid:
            device = self.guidManager.getObject(actor.element_uuid)
        environ.update({'dev': device})

        component = None
        if actor.element_sub_uuid:
            component = self.guidManager.getObject(actor.element_sub_uuid)
        environ.update({'component': component})
        
        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)
        environ.update(data)
        
        try:
            details_list = json.loads(notification.content['details'])
        except ValueError:
            raise ActionExecutionException('Invalid JSON string in details')
        
        #self.details.update(notification.content)
        body = {'event_type': self.eventType,
                'client'    : 'Zenoss',
                'client_url': '${urls/eventUrl}'}

        for kv in details_list:
            body[kv['key']] = kv['value']
        
        self.details = eval(processTalSource(body, **environ))
        print "DETAILS: %s " % self.details
        
        self.issueInfo()
        self.createOrUpdateIssue()

    def updateContent(self, content=None, data=None):
        """"""
        updates = dict()
        for k in NotificationProperties.ALL:
            updates[k] = data.get(k)
        content.update(updates)
    
    def createOrUpdateIssue(self):
        """ Open or Close an issue
        """
        eventID = self.details['eventID']
        print "EVENT ID: %s" % eventID
        self.issueInfo()
        if self.eventType == EventType.OPEN:
            # first check that it doesn't already exist
            test = self.footprints.getIssueID(eventID)
            if len(test) == 0:
                self.footprints.argumentHash = self.issueOpenDictionary()
                #self.footprints.argumentHash.update(self.extendedDictionary())
                mrID = str(self.footprints.createIssue())
                # need new API method to manipulate custom event property for ticket ID
                msg = "Issue %s was created" % mrID
                self.zep.addNote(eventID, msg, userName='admin')
                self.zep.acknowledgeEventSummaries(eventID)
            else: # reopen the event in footprints
                mrID = test[0]['mrid']
                self.footprints.mrID = mrID
                print "issue already exists %s" % mrID
                data = self.issueClosedDictionary()
                self.footprints.argumentHash = self.issueClosedDictionary()
                output = self.footprints.editIssue()
                msg = "ticket %s was reopened" % self.footprints.mrID
                self.zep.addNote(eventID, msg, userName='admin')
        else:
            try:
                mrID = self.footprints.getIssueID(eventID)[0]['mrid']
                self.footprints.mrID = mrID
                self.footprints.argumentHash = self.issueClosedDictionary()
                output = self.footprints.editIssue()
                msg = "ticket %s was closed" % self.footprints.mrID
                self.zep.addNote(eventID, msg, userName='admin')
            except:
                print "closing failed"
                pass

    def issueInfo(self):
        """ Build ticket info
        """
        self.title = "%s: %s" % (self.details['device'],self.details['message'])
        self.description = ''
        for k,v in self.details.items():
            line = "%s: %s\n" % (k,v)
            self.description += line
        self.priority = 6 - int(self.details['severity'])
    
    def issueOpenDictionary(self):
        """ Create args for opening an issue
        """
        data = {
                'projectID' : self.footprints.projectID,
                'title' : self.title,
                'priorityNumber' : self.priority,
                'status' : self.eventType,
                'description' : self.description,
                }
        return data
    
    def issueClosedDictionary(self):
        """ Create args for closing a ticket
        """
        data = {
                'projectID' : self.footprints.projectID,
                'mrID' : self.footprints.mrID,
                'status' : self.eventType,
                'description' : self.details['message'],
                }
        return data

#    def extendedDictionary(self):
#        """ Extended ticket dictionary
#        """
#        data = {
#            self.eventField : self.details['eventID'],
#            'Reporting__bSource' : 'Zenoss',
#            }
#        return data
        
