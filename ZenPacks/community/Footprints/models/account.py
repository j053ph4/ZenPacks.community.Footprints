# Copyright (c) 2013, Agero, Inc. <info@agero.com>
import serialization
from workspace import Workspace
import json

class Account(object):
    """
    A Footprints account consists of a server, username, and password
    """
    def __init__(self, server=None, user=None, password=None):
        self.server = server
        self.user = user
        self.password = password

    def __json__(self):
        return json.dumps(self, cls=serialization.JSONEncoder)
