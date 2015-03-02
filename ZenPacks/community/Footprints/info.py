# Copyright (c) 2013, Agero, Inc. <info@agero.com>

import Globals

from zope.component import adapts
from zope.interface import implements

from Products.ZenModel.NotificationSubscription import NotificationSubscription

from Products.Zuul.infos import InfoBase
from Products.Zuul.infos.actions import ActionFieldProperty

from interfaces import IFootprintsEventsAPIActionContentInfo

class FootprintsEventsAPIActionContentInfo(InfoBase):
    """
    Provides the "implementation" for IFootprintsEventsAPIActionContentInfo.

    Based on the definitions for the builtin actions in Products.Zuul.infos.actions.
    """
    implements(IFootprintsEventsAPIActionContentInfo)
    adapts(NotificationSubscription)

    projectid = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'projectid')
    summary = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'summary')
    description = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'description')
    incident_key = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'incident_key')
    assignees = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'assignees')
    details = ActionFieldProperty(IFootprintsEventsAPIActionContentInfo, 'details')
