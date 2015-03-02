# Copyright (c) 2013, Agero, Inc. <info@agero.com>

#import json
from lib.WebServicesAPI import *
from models.workspace import Workspace
from models.assignee import Assignee

def retrieve_workspaces(account):
    """
    Fetches the list of all workspaces for an Account from the Footprints API.

    Returns:
        A list of Workspace objects.
    """
    fp = WebServicesAPI(account.server,account.user,account.password,False)
    workspace_data = fp.listWorkspaces() 
    workspaces = []
    for data in workspace_data:
        projectid = data['counterid']
        projectname = data['counter'].replace('ProjectName:','')
        workspace = Workspace(projectid, projectname)
        workspaces.append(workspace)
    return workspaces

def retrieve_assignees(account, workspace, users=True):
    """
    Fetches the list of all assignees for an Account from the Footprints API.
    Returns:
        A list of Workspace objects.
    """
    fp = WebServicesAPI(account.server,account.user,account.password,False)
    try:
        fp.projectID = workspace.projectid
    except:
        pass
    assignee_data = fp.listAssignees(users)
    assignees = []
    for data in assignee_data:
        internal = data['value_int']
        external = data['value_ext']
        assignee = Assignee(internal,external)
        assignees.append(assignee)
    return assignees

