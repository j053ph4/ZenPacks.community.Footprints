# Copyright (c) 2013, Agero, Inc. <info@agero.com>

import requests
import models.account
import models.serialization
from models.workspace import Workspace
from models.assignee import Assignee

from Products.ZenUtils.Ext import DirectRouter, DirectResponse
import json
import logging
log = logging.getLogger('zen.Footprints.WorkspacesRouter')

ACCOUNT_ATTR = 'footprints_account'

def _dmdRoot(dmdContext):
    return dmdContext.getObjByPath("/zport/dmd/")

def _success(model_obj, msg=None):
    obj_data = json.loads(json.dumps(model_obj, cls=models.serialization.JSONEncoder))
    return DirectResponse.succeed(msg=msg, data=obj_data)

def _retrieve_workspaces(account):
    log.info("Fetching list of Footprints workspaces for %s..." % account.server)
    try:
        workspaces = requests.retrieve_workspaces(account)
    except:
        log.warn("Problem retrieving workspaces")
    
    log.info("Found %d workspaces for %s" % (len(workspaces), account.server))
    return workspaces

def _retrieve_assignees(account, workspace, users):
    log.info("Fetching list of Footprints workspaces for %s..." % account.server)
    try:
        assignees = requests.retrieve_assignees(account, workspace, users)
    except:
        log.warn("Problem retrieving assignees")
    
    log.info("Found %d assignees for %s project: %s" % (len(assignees), account.server, workspace.projectname))
    return assignees

class FootprintsServerRouter(DirectRouter):
    def __init__(self, context, request=None):
        super(FootprintsServerRouter, self).__init__(context, request)

    def get_account_settings(self):
        """
        Retrieves the account object from /zport/dmd/footprints_account.
        """
        dmdRoot = _dmdRoot(self.context)
        account = getattr(dmdRoot, ACCOUNT_ATTR, models.account.Account(None, None, None))
        return _success(account)
    
    def update_account_settings(self, server=None, user=None, password=None, wants_messages=True):
        """
        Saves the account object and returns a list of workspaces associated
        with that account.  Returns nothing if invalid account info is set.

        The account object is saved as /zport/dmd/footprints_account
        (aka, dmdRoot.footprints_account)
        """
        account = models.account.Account(server, user, password)
        dmdRoot = _dmdRoot(self.context)
        setattr(dmdRoot, ACCOUNT_ATTR, account)
        
        if not account.server or not account.user or not account.password:
            return DirectResponse.succeed()
        
        workspaces_router = WorkspacesRouter(self.context, self.request)
        result = workspaces_router.get_workspaces(wants_messages)
        
        if result.data['success']:
            result.data['msg'] = "Footprints workspaces retrieved successfully."
            workspaces = result.data['data']
            log.info("Successfully fetched %d Footprints workspaces.", len(workspaces))
        
        return result
        
class WorkspacesRouter(DirectRouter):
    """
    Simple router responsible for fetching the list of workspaces from Footprints.
    """
    def get_workspaces(self, wants_messages=False):
        dmdRoot = _dmdRoot(self.context)
        no_account_msg = 'Footprints account info not set.'
        set_up_api_key_inline_msg = 'Set up your account info in "Advanced... Footprints Settings"'
        msg = no_account_msg if wants_messages else None
        if not hasattr(dmdRoot, ACCOUNT_ATTR):
            return DirectResponse.fail(msg=msg, inline_message=set_up_api_key_inline_msg)
        
        account = getattr(dmdRoot, ACCOUNT_ATTR)
        if not account.server or not account.user or not account.password:
            return DirectResponse.fail(msg=msg, inline_message=set_up_api_key_inline_msg)
        try:
            workspaces = _retrieve_workspaces(account)
        except:
            msg = 'Failed to retrieve workspaces' if wants_messages else None
            return DirectResponse.fail(msg=msg, inline_message='Check settings: Go to "Advanced... Footprints Settings"')
        
        if not workspaces:
            msg = ("No workspaces were found for %s." % account.server) if wants_messages else None
            return DirectResponse.fail(msg=msg)
        
        return _success(workspaces)

class AssigneesRouter(DirectRouter):
    """
    Simple router responsible for fetching the list of assignees by workspace from Footprints.
    """
    def get_assignees(self, projectid, wants_messages=False):
        dmdRoot = _dmdRoot(self.context)
        no_account_msg = 'Footprints account info not set.'
        set_up_api_key_inline_msg = 'Set up your account info in "Advanced... Footprints Settings"'
        msg = no_account_msg if wants_messages else None
        if not hasattr(dmdRoot, ACCOUNT_ATTR):
            return DirectResponse.fail(msg=msg, inline_message=set_up_api_key_inline_msg)
        
        account = getattr(dmdRoot, ACCOUNT_ATTR)
        if not account.server or not account.user or not account.password or not projectid:
            return DirectResponse.fail(msg=msg, inline_message=set_up_api_key_inline_msg)
        
        workspaces = _retrieve_workspaces(account)
        for w in workspaces:
            print "project: %s" % w.projectname
            if w.projectid == projectid:
                workspace = w
                
        if not workspace:
            msg = ("No workspace was found for %s." % account.server) if wants_messages else None
            return DirectResponse.fail(msg=msg)
        
        try:
            assignees = _retrieve_assignees(account,workspace,True)
        except:
            msg = 'Failed to retrieve workspace' if wants_messages else None
            return DirectResponse.fail(msg=msg, inline_message='Check settings: Go to "Advanced... Footprints Settings"')
        
        if not assignees:
            msg = ("No assignees were found for %s." % account.server) if wants_messages else None
            return DirectResponse.fail(msg=msg)
        
        return _success(assignees)

