# Copyright (c) 2013, Agero, Inc. <info@agero.com>

import routers

import logging
log = logging.getLogger('zen.Fooprints')

import Globals

from Products.ZenModel.ZenossSecurity import ZEN_MANAGE_DMD
from Products.ZenModel.DataRoot import DataRoot
from Products.ZenModel.UserSettings import UserSettingsManager
from Products.ZenModel.ZenossInfo import ZenossInfo
from Products.ZenModel.ZenPackManager import ZenPackManager
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import monkeypatch, unused
unused(Globals)

import pkg_resources

BROWSER_PAGE = 'fp-import-workspaces-page'
ACTION_NAME  = 'footprints'

# Add "Footprints" to left navigation on Advanced / Settings page. This
# is so ugly because the settings page is still a Zenoss 2 "back-compat"
# page.
for klass in (DataRoot, UserSettingsManager, ZenossInfo, ZenPackManager):
    action = BROWSER_PAGE
    if klass == ZenPackManager:
        action = '../%s' % action

    fti = klass.factory_type_information[0]
    fti['actions'] = fti['actions'] + ({
        'id': BROWSER_PAGE,
        'name': 'Footprints',
        'action': action,
        'permissions': (ZEN_MANAGE_DMD,)
    },)

@monkeypatch('Products.ZenUI3.navigation.menuitem.PrimaryNavigationMenuItem')
def update(self):
    '''
    Update subviews for this PrimaryNavigationMenuItem.

    Post-processes default behavior to add our subview. This allows the
    secondary navigation bar to be rendered properly when the user is
    looking at the Footprints settings screen.
    '''
    # original gets injected into locals by monkeypatch decorator.
    original(self)

    if '/zport/dmd/dataRootManage' in self.subviews:
        self.subviews.append('/zport/dmd/%s' % BROWSER_PAGE)

@monkeypatch('Products.Zuul.facades.triggersfacade.TriggersFacade')
def createNotification(self, id, action, *args, **kwargs):
    '''
    Overrides createNotification to provide reasonable defaults for Footprints
    notifications
    '''

    # original gets injected into locals by monkeypatch decorator.
    notification = original(self, id, action, *args, **kwargs)

    if notification.action.lower() == ACTION_NAME:
        notification.send_clear = True
        notification.repeat_seconds = 60
        notification.send_initial_occurrence = False

    return notification

def version():
    """
    Convenience function to determine the ZenPack version at runtime since
    it must be hardcoded in setup.py.
    """
    resources = pkg_resources.require(__name__)
    if not resources:
        return None

    return resources[0].version

class ZenPack(ZenPackBase):
    def remove(self, app, leaveObjects=False):
        """
        Remove Footprints account model on uninstall
        """
        if not leaveObjects:
            log.info('Removing Footprints account info')
            dmdRoot = routers._dmdRoot(app.zport.dmd)
            if hasattr(dmdRoot, routers.ACCOUNT_ATTR):
                delattr(dmdRoot, routers.ACCOUNT_ATTR)

            log.info('Removing Footprints notifications')
            allNotifications = app.zport.dmd.NotificationSubscriptions
            footprintsNotificationIDs = [allNotifications.findChild(notification).id
                                        for notification in allNotifications.keys()
                                            if allNotifications.findChild(notification).action == ACTION_NAME]

            for pdid in footprintsNotificationIDs:
                allNotifications.findChild(pdid).getPrimaryParent()._delObject(pdid)

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

