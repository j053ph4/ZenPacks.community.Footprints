(function(){
    Ext.onReady(function() {
        var workspaces_router = Zenoss.remote.WorkspacesRouter;
        var assignees_router = Zenoss.remote.AssigneesRouter;
        
        Ext.define('footprints.model.Workspace', {
            extend: 'Ext.data.Model',
            fields: [
                {name: 'projectname',        type: 'string'},
                {name: 'projectid',          type: 'string'},
                {name: 'projectfield',          type: 'string'},
            ]
        });
        
        Ext.define('footprints.model.Assignee', {
            extend: 'Ext.data.Model',
            fields: [
                {name: 'internal_name',        type: 'string'},
                {name: 'external_name',          type: 'string'},
            ]
        });
        
        Ext.define('footprints.events.WorkspaceListWidget', {
            extend: 'Ext.container.Container',
            alias: 'widget.footprints-events-workspace-list',
            name: 'projectid',
            layout:'anchor',
            id: 'fpWorkspaceList',
            defaults: {
                anchor: '100%'
            },
            initComponent: function() {
                var container = this;

                this.store = Ext.create('Zenoss.NonPaginatedStore', {
                    storeId: 'workspace_store',
                    root: 'data',
                    autoLoad: true,
                    model: 'footprints.model.Workspace',
                    loaded: false,
                    flex: 1,

                    proxy: {
                        type:'direct',
                        limitParam:undefined,
                        startParam:undefined,
                        pageParam:undefined,
                        sortParam: undefined,
                        directFn: workspaces_router.get_workspaces,
                        reader: {
                            type:'json',
                            root: 'data'
                        },
                        listeners: {
                            exception: function(proxy, response, operation, eOpts) {
                                if (response.result && response.result.inline_message)
                                {
                                    Ext.getCmp('fpWorkspaceList').showError(response.result.inline_message);
                                }
                            }
                        }
                    },

                    isLoaded: function() {
                        return this.loaded;
                    },
                    listeners:  {
                        load: function() {
                            this.loaded = true;
                            var combo = Ext.getCmp('workspace_list_combo');
                            combo.synchronize();
                        }
                    }
                });

                var workspace_list_combo = Ext.create('Ext.form.field.ComboBox',
                    {
                        name: 'workspace_list_combo',
                        id: 'workspace_list_combo',
                        queryMode: 'local',
                        valueField: 'projectid',
                        displayField: 'projectname',
                        forceSelection: true,
                        fieldLabel: _t('Workspace'),
                        store: container.store,
                        listeners: {
                            select: function (combo, record, index) {
                                Ext.getCmp('projectid_textfield').synchronize(combo.value)
                            }
                        },
                        synchronize: function() {
                            var projectid = Ext.getCmp('projectid_textfield').value;
                            var workspace_record = this.findRecordByValue(projectid);
                            if (workspace_record) {
                                this.setValue(projectid);
                            } else {
                                this.setValue(null);
                            }
                        }
                    });

                var workspace_list_error = Ext.create('Ext.form.field.Text',
                    {
                        name: 'workspace_list_error',
                        id: 'workspace_list_error',
                        fieldLabel: _t('Workspace'),
                        hidden: true,
                        readOnly: true
                    });

                var projectid_textfield = Ext.create('Ext.form.field.Text',
                    {
                        name: 'projectid',
                        id: 'projectid_textfield',
                        fieldLabel: _t('Workspace ID'),
                        listeners: {
                            change: function() {
                                if (this.synchronizing)
                                    return;

                                var store = Ext.data.StoreManager.lookup('workspace_store');
                                if (store.isLoaded()) {
                                    var combo = Ext.getCmp('workspace_list_combo');
                                    combo.synchronize();
                                }
                            }
                        },
                        synchronizing: false,
                        synchronize: function(value) {
                            this.synchronizing = true;
                            this.setValue(value);
                            this.synchronizing = false;
                        }
                    });

                this.items = [workspace_list_combo, workspace_list_error, projectid_textfield];

                if (this.value) {
                    projectid_textfield.setValue(this.value);
                }

                this.callParent(arguments);
            },
            showError: function(msg) {
                var workspace_list_error = Ext.getCmp('workspace_list_error');
                var workspace_list_combo = Ext.getCmp('workspace_list_combo');
                workspace_list_combo.hide();
                workspace_list_error.show();
                workspace_list_error.setValue(msg);
            }

        });

        Ext.define('footprints.events.WorkspaceListWidget', {
            extend: 'Ext.container.Container',
            alias: 'widget.footprints-events-workspace-list',
            name: 'projectid',
            layout:'anchor',
            id: 'fpWorkspaceList',
            defaults: {
                anchor: '100%'
            },
            initComponent: function() {
                var container = this;

                this.store = Ext.create('Zenoss.NonPaginatedStore', {
                    storeId: 'workspace_store',
                    root: 'data',
                    autoLoad: true,
                    model: 'footprints.model.Workspace',
                    loaded: false,
                    flex: 1,

                    proxy: {
                        type:'direct',
                        limitParam:undefined,
                        startParam:undefined,
                        pageParam:undefined,
                        sortParam: undefined,
                        directFn: workspaces_router.get_workspaces,
                        reader: {
                            type:'json',
                            root: 'data'
                        },
                        listeners: {
                            exception: function(proxy, response, operation, eOpts) {
                                if (response.result && response.result.inline_message)
                                {
                                    Ext.getCmp('fpWorkspaceList').showError(response.result.inline_message);
                                }
                            }
                        }
                    },

                    isLoaded: function() {
                        return this.loaded;
                    },
                    listeners:  {
                        load: function() {
                            this.loaded = true;
                            var combo = Ext.getCmp('workspace_list_combo');
                            combo.synchronize();
                        }
                    }
                });

                var workspace_list_combo = Ext.create('Ext.form.field.ComboBox',
                    {
                        name: 'workspace_list_combo',
                        id: 'workspace_list_combo',
                        queryMode: 'local',
                        valueField: 'projectid',
                        displayField: 'projectname',
                        forceSelection: true,
                        fieldLabel: _t('Workspace'),
                        store: container.store,
                        listeners: {
                            select: function (combo, record, index) {
                                Ext.getCmp('projectid_textfield').synchronize(combo.value)
                            }
                        },
                        synchronize: function() {
                            var projectid = Ext.getCmp('projectid_textfield').value;
                            var workspace_record = this.findRecordByValue(projectid);
                            if (workspace_record) {
                                this.setValue(projectid);
                            } else {
                                this.setValue(null);
                            }
                        }
                    });

                var workspace_list_error = Ext.create('Ext.form.field.Text',
                    {
                        name: 'workspace_list_error',
                        id: 'workspace_list_error',
                        fieldLabel: _t('Workspace'),
                        hidden: true,
                        readOnly: true
                    });

                var projectid_textfield = Ext.create('Ext.form.field.Text',
                    {
                        name: 'projectid',
                        id: 'projectid_textfield',
                        fieldLabel: _t('Workspace ID'),
                        listeners: {
                            change: function() {
                                if (this.synchronizing)
                                    return;

                                var store = Ext.data.StoreManager.lookup('workspace_store');
                                if (store.isLoaded()) {
                                    var combo = Ext.getCmp('workspace_list_combo');
                                    combo.synchronize();
                                }
                            }
                        },
                        synchronizing: false,
                        synchronize: function(value) {
                            this.synchronizing = true;
                            this.setValue(value);
                            this.synchronizing = false;
                        }
                    });

                this.items = [workspace_list_combo, workspace_list_error, projectid_textfield];

                if (this.value) {
                    projectid_textfield.setValue(this.value);
                }

                this.callParent(arguments);
            },
            showError: function(msg) {
                var workspace_list_error = Ext.getCmp('workspace_list_error');
                var workspace_list_combo = Ext.getCmp('workspace_list_combo');
                workspace_list_combo.hide();
                workspace_list_error.show();
                workspace_list_error.setValue(msg);
            }

        });
        
        Ext.define('footprints.events.AssigneesListWidget', {
            extend: 'Ext.container.Container',
            alias: 'widget.footprints-events-assignees-list',
            name: 'assignees',
            layout:'anchor',
            id: 'fpAssigneesList',
            defaults: {
                anchor: '100%'
            },
            initComponent: function() {
                var container = this;

                this.store = Ext.create('Zenoss.NonPaginatedStore', {
                    storeId: 'assignees_store',
                    root: 'data',
                    autoLoad: true,
                    model: 'footprints.model.Assignee',
                    loaded: false,
                    flex: 1,

                    proxy: {
                        type:'direct',
                        limitParam:undefined,
                        startParam:undefined,
                        pageParam:undefined,
                        sortParam: undefined,
                        directFn: assignees_router.get_assignees('8'),
                        reader: {
                            type:'json',
                            root: 'data'
                        },
                        listeners: {
                            exception: function(proxy, response, operation, eOpts) {
                                if (response.result && response.result.inline_message)
                                {
                                    Ext.getCmp('fpAssigneesList').showError(response.result.inline_message);
                                }
                            }
                        }
                    },

                    isLoaded: function() {
                        return this.loaded;
                    },
                    listeners:  {
                        load: function() {
                            this.loaded = true;
                            var combo = Ext.getCmp('assignees_list_combo');
                            combo.synchronize();
                        }
                    }
                });

                var assignees_list_combo = Ext.create('Ext.form.field.ComboBox',
                    {
                        name: 'assignees_list_combo',
                        id: 'assignees_list_combo',
                        queryMode: 'local',
                        valueField: 'internal_name',
                        displayField: 'extermal_name',
                        forceSelection: true,
                        fieldLabel: _t('Assignees'),
                        store: container.store,
                        listeners: {
                            select: function (combo, record, index) {
                                Ext.getCmp('internal_name_textfield').synchronize(combo.value)
                            }
                        },
                        synchronize: function() {
                            var internal_name = Ext.getCmp('internal_name_textfield').value;
                            var assignee_record = this.findRecordByValue(internal_name);
                            if (assignee_record) {
                                this.setValue(internal_name);
                            } else {
                                this.setValue(null);
                            }
                        }
                    });

                var assignees_list_error = Ext.create('Ext.form.field.Text',
                    {
                        name: 'assignees_list_error',
                        id: 'assignees_list_error',
                        fieldLabel: _t('Assignees'),
                        hidden: true,
                        readOnly: true
                    });

                var internal_name_textfield = Ext.create('Ext.form.field.Text',
                    {
                        name: 'internal_name',
                        id: 'internal_name_textfield',
                        fieldLabel: _t('Assignee Name'),
                        listeners: {
                            change: function() {
                                if (this.synchronizing)
                                    return;

                                var store = Ext.data.StoreManager.lookup('assignees_store');
                                if (store.isLoaded()) {
                                    var combo = Ext.getCmp('assignees_list_combo');
                                    combo.synchronize();
                                }
                            }
                        },
                        synchronizing: false,
                        synchronize: function(value) {
                            this.synchronizing = true;
                            this.setValue(value);
                            this.synchronizing = false;
                        }
                    });

                this.items = [assignees_list_combo, assignees_list_error, internal_name_textfield];

                if (this.value) {
                	internal_name_textfield.setValue(this.value);
                }

                this.callParent(arguments);
            },
            showError: function(msg) {
                var assignees_list_error = Ext.getCmp('assignees_list_error');
                var assignees_list_combo = Ext.getCmp('assignees_list_combo');
                assignees_list_combo.hide();
                assignees_list_error.show();
                assignees_list_error.setValue(msg);
            }

        });
        

        Ext.define('footprints.events.DetailsField', {
            extend: 'Ext.container.Container',
            alias: 'widget.footprints-events-details-field',

            initComponent: function() {
                var store = Ext.create('Ext.data.JsonStore', {
                    autoSync: true,
                    fields: [{name: 'key'}, {name: 'value'}],
                    proxy: {type: 'memory'},
                    listeners: {
                        write: function(store, operation) {
                            if (!hidden_field) {
                                return;
                            }

                            vs = [];

                            Ext.each(store.getRange(), function(record) {
                                if (record.data.key) {
                                    vs.push(record.data);
                                }
                            });

                            hidden_field.setValue(Ext.JSON.encode(vs));
                        }
                    }
                });

                var hidden_field = Ext.create('Ext.form.field.Hidden', {name: 'details'});

                var row_editor = Ext.create('Ext.grid.plugin.RowEditing');

                var grid_panel = Ext.create('Ext.grid.Panel', {
                    title: _t('Details'),
                    height: 200,
                    plugins: [row_editor],
                    store: store,

                    dockedItems: [{
                        xtype: 'toolbar',
                        store: store,
                        items: [{
                            text: 'Add',
                            iconCls: 'add_button',
                            handler: function() {
                                store.insert(0, {key: '', value: ''});
                                row_editor.startEdit(0, 0);
                            }
                        }, '-', {
                            itemId: 'delete',
                            text: 'Delete',
                            iconCls: 'delete',
                            handler: function() {
                                var selection = grid_panel.getView().getSelectionModel().getSelection()[0];
                                if (selection) {
                                    store.remove(selection);
                                    store.sync();
                                }
                            }
                        }]
                    }],

                    columns: [{
                        header: _t('Key'),
                        dataIndex: 'key',
                        editor: { xtype: 'textfield', allowBlank: true },
                        sortable: true,
                        width: 200
                    },{
                        header: _t('Value'),
                        dataIndex: 'value',
                        editor: { xtype: 'textfield', allowBlank: true },
                        sortable: true,
                        flex: 1
                    }]
                });

                this.items = [hidden_field, grid_panel];

                if (this.value) {
                    hidden_field.setValue(this.value);
                    store.loadData(Ext.JSON.decode(this.value));
                }

                this.callParent(arguments);
            }
        });
    });
})();
