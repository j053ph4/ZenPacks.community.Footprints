# Copyright (c) 2013, Agero, Inc. <info@agero.com>

import json

class JSONEncoder(json.JSONEncoder):
     def default(self, obj):
         import account
         import workspace
         import assignee
         
         if not isinstance(obj, (account.Account, workspace.Workspace, assignee.Assignee)):
             return super(JSONEncoder, self).default(obj)

         return obj.__dict__

