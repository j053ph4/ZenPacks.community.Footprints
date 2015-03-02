# Copyright (c) 2013, Agero, Inc. <info@agero.com>

from . import enum
import serialization
import json

class Workspace(object):
    ''''''
    def __init__(self,projectid,projectname):
        self.projectid = projectid
        self.projectname = projectname

    def __repr__(self):
        return "Workspace(projectid='%s', projectname='%s')" % (self.projectid, self.projectname)

    def __json__(self):
        return json.dumps(self, cls=serialization.JSONEncoder)
