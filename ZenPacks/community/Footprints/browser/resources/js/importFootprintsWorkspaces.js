(function(){
    Ext.onReady(function(){
        var fp_server_router = Zenoss.remote.FootprintsServerRouter;
        var workspaces_router = Zenoss.remote.WorkspacesRouter;

        Ext.define('com.footprints.ImportWorkspacePanel', {
            extend: 'Ext.form.Panel',
            alias: 'widget.com-footprints-import-workspace-panel',
            title: 'Footprints Settings',
            id: 'fpSettingsPanel',
            defaults: {
                listeners: {
                    specialkey: function(field, event) {
                        if (event.getKey() == event.ENTER) {
                           field.up('form').submit();
                        }
                    }
                }
            },
            items: [
                {
                    fieldLabel: 'Server',
                    labelWidth: 150,
                    name: 'server',
                    width: 400,
                    xtype: 'textfield'
                },
                {
                    fieldLabel: 'Username',
                    labelWidth: 150,
                    name: 'user',
                    width: 400,
                    xtype: 'textfield'
                },
                {
                    fieldLabel: 'Password',
                    labelWidth: 150,
                    name: 'password',
                    width: 400,
                    xtype: 'textfield'
                },
                {
                    xtype: 'button',
                    text: 'Apply',
                    style: {
                        marginBottom: '15px'
                    },
                    handler: function() {
                        var panel = Ext.getCmp('fpSettingsPanel');
                        panel.submit();
                    }
                },
                {
                    xtype: 'grid',
                    name: 'fp_workspace_grid',
                    title: 'Footprints Workspaces',
                    columns: [{header: 'Workspace Name', dataIndex: 'projectname', flex: 1}],
                    sortableColumns: false,
                    enableColumnHide: false,
                    enableColumnMove: false,
                    enableColumnResize: true,
                    hideHeaders: true,
                    store: Ext.create('Ext.data.Store', {
                        storeId: 'fpWorkspaceStore',
                        model: 'footprints.model.Workspace'
                    }),
                    flex: 1
                },
            ],
            onRender: function() {
                this.callParent(arguments);
                this.load();
            },
            load: function() {
                fp_server_router.get_account_settings({}, function(result) {
                    if (!result.success)
                        return;

                    this.getForm().setValues(result.data);

                    if ((result.data.server && result.data.user) && result.data.password) {
                        workspaces_router.get_workspaces({wants_messages: true}, function(result) {
                            var fpWorkspaceStore = Ext.data.StoreManager.lookup('fpWorkspaceStore');
                            fpWorkspaceStore.loadData((result.success && result.data) ? result.data : []);
                        }, this);
                    }
                }, this);
            },
            submit: function() {
                var values = this.getForm().getValues();
                fp_server_router.update_account_settings(values, function(result) {
                    var fpWorkspaceStore = Ext.data.StoreManager.lookup('fpWorkspaceStore');
                    fpWorkspaceStore.loadData((result.success && result.data) ? result.data : []);
                });
            },
        });

        var settings = Ext.create(com.footprints.ImportWorkspacePanel, {
            renderTo: 'import-footprints-workspaces'
        });
    });
})();

