# Copyright (c) 2013, Agero, Inc. <info@agero.com>

"""
Actions in Zenoss define their properties through their 'actionContentInfo'
attribute. 'actionContentInfo' is a Zope interface which defines the names and
types of the properties of the action. 'actionContentInfo' is used by the
action to generate a block of JS that will render the action's content tab
in the UI (see Products.ZenModel.interfaces.IAction.generateJavascriptContent).

This module defines the Zope interface that is assigned to
actions.FootprintsEventsAPIAction.actionContentInfo.

Other example Zope interfaces used to define action properties are:

  * Products.Zuul.interfaces.actions.IEmailActionContentInfo
  * Products.Zuul.interfaces.actions.IPageActionContentInfo
  * Products.Zuul.interfaces.actions.ICommandActionContentInfo
  * Products.Zuul.interfaces.actions.ISnmpTrapActionContentInfo
"""

import json

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION
from Products.ZenUtils.Version import Version

import textwrap

# Make the UI look good in Zenoss 3 and Zenoss 4
if Version.parse('Zenoss %s' % ZENOSS_VERSION) >= Version.parse('Zenoss 4'):
    SingleLineText = schema.TextLine
    MultiLineText = schema.Text
else:
    SingleLineText = schema.Text
    MultiLineText = schema.TextLine

def _serialize(details):
    return [{u'key':a, u'value':b} for a,b in zip(details.keys(), details.values())]

class IFootprintsEventsAPIActionContentInfo(IInfo):
    """
    Zope interface defining the names and types of the properties used by
    actions.FootprintsEventsAPIAction.

    The "implementation" of this interface is defined in
    info.FootprintsEventsAPIActionContentInfo.
    """

    
    projectid = SingleLineText(
        title       = _t(u'Workspace ID'),
        description = _t(u'The ID of the selected Footprints workspace.'),
        xtype       = 'footprints-events-workspace-list'
    )

    summary = SingleLineText(
        title       = _t(u'Summary'),
        description = _t(u'The summary for the Footprints ticket.'),
        default     = u'${evt/summary}'
    )

    description = SingleLineText(
        title       = _t(u'Description'),
        description = _t(u'The description for the Footprints ticket.'),
        default     = u'${evt/device}: ${evt/summary}',
    )

    incident_key = SingleLineText(
        title       = _t(u'Incident Key'),
        description = _t(u'The incident key for the Footprints ticket.'),
        default     = u'${evt/evid}',
    )
    
    assignees = schema.List(
        title       = _t(u'Assignees'),
        description = _t(u'The Assignees for the Footprints ticket.'),
        default     = [],
        group       = _t(u'Assignees'),
        xtype='footprints-events-assignees-field')
    
    details = schema.List(
        title       = _t(u'Details'),
        description = _t(u'The incident key for the Footprints ticket.'),
        default     = [json.dumps(_serialize({
                    u'device':u'${evt/device}',
                    u'component':u'${evt/component}',
                    u'ipAddress':u'${evt/ipAddress}',
                    u'severity':u'${evt/severity}',
                    u'message':u'${evt/message}',
                    u'eventID':u'${evt/evid}',
                    }))],
        group       = _t(u'Details'),
        xtype='footprints-events-details-field')
