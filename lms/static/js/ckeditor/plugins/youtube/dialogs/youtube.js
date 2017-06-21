CKEDITOR.dialog.add( 'youtube', function( editor ) {
    return {
        title: editor.lang.youtube.title,
        minWidth: 500,
        minHeight: 100,
        contents: [ {
            id: 'info',
            label: editor.lang.youtube.infoLabel,
            elements: [ {
                type: 'vbox',
                padding: 0,
                children: [
                    {
                    type: 'hbox',
                    widths: [ '365px', '110px' ],
                    align: 'right',
                    children: [ {
                        type: 'text',
                        id: 'url',
                        label: editor.lang.youtube.allowed,
                        required: true,
                        validate: CKEDITOR.dialog.validate.notEmpty( editor.lang.youtube.urlMissing ),
                        setup: function( widget ) {
                            this.setValue( widget.data.origin );
                        },
                        commit: function( widget ) {
                            widget.setData( 'origin', this.getValue() );
                        }
                    },
                    {
                        type: 'button',
                        id: 'browse',
                        // v-align with the 'txtUrl' field.
                        // TODO: We need something better than a fixed size here.
                        style: 'display:inline-block;margin-top:14px;',
                        align: 'center',
                        label: editor.lang.common.browseServer,
                        hidden: true,
                        filebrowser: 'info:url'
                    } ]
                } ]
            },
            {
                type: 'hbox',
                id: 'size',
                children: [ {
                    type: 'text',
                    id: 'width',
                    label: editor.lang.common.width,
                    setup: function( widget ) {
                        if ( widget.data.width ) {
                            this.setValue( widget.data.width );
                        }
                    },
                    commit: function( widget ) {
                        widget.setData( 'width', this.getValue() );
                    }
                },
                {
                    type: 'text',
                    id: 'height',
                    label: editor.lang.common.height,
                    setup: function( widget ) {
                        if ( widget.data.height ) {
                            this.setValue( widget.data.height );
                        }
                    },
                    commit: function( widget ) {
                        widget.setData( 'height', this.getValue() );
                    }
                },
                ]
            },

             ]
        },
        {
            id: 'Upload',
            hidden: true,
            filebrowser: 'uploadButton',
            label: editor.lang.youtube.upload,
            elements: [ {
                type: 'file',
                id: 'upload',
                label: editor.lang.youtube.btnUpload,
                style: 'height:40px',
                size: 38
            },
            {
                type: 'fileButton',
                id: 'uploadButton',
                filebrowser: 'info:url',
                label: editor.lang.youtube.btnUpload,
                'for': [ 'Upload', 'upload' ]
            } ]
        },
         ]
    };
} );
