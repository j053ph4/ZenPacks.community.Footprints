# Copyright (c) 2013, Agero, Inc. <info@agero.com>
import serialization
import json

class Assignee(object):
    ''''''
    def __init__(self, internal_name, external_name):
        self.internal_name = internal_name
        self.external_name = external_name
        
    def __repr__(self):
        return "Assignee(internal_name='%s', external_name='%s')" % (self.internal_name, self.external_name)

    def __json__(self):
        return json.dumps(self, cls=serialization.JSONEncoder)
    
