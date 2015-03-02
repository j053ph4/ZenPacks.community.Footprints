from models import enum

ALL_PROPERTIES = ['projectid', 'projectname', 'summary', 'description', 'incident_key', 'details']

EventType = enum(OPEN='Open', CLOSE='Closed', ASSIGNED='Assigned')

Properties = enum(PROJECTID='projectid', PROJECTNAME='projectname', SUMMARY='summary', DESCRIPTION='description',
                  INCIDENT_KEY='incident_key', DETAILS='details')

REQUIRED_PROPERTIES = [Properties.PROJECTID, Properties.SUMMARY, Properties.DESCRIPTION, Properties.INCIDENT_KEY]
