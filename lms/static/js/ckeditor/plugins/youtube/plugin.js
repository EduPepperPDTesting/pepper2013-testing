CKEDITOR.plugins.add( 'youtube', {
    requires: 'widget',
    lang: 'en', // 'de,en,eu,es,ru,uk,fr',
    icons: 'youtube',
    init: function( editor ) {
        editor.widgets.add( 'youtube', {
            button: editor.lang.youtube.button,
            template: '<div class="ckeditor-youtube"></div>',
            /*
             * Allowed content rules (http://docs.ckeditor.com/#!/guide/dev_allowed_content_rules):
             *  - div-s with text-align,float,margin-left,margin-right inline style rules and required ckeditor-youtube class.
             *  - video tags with src, width and height attributes.
             */
            allowedContent: 'div(!ckeditor-youtube){margin-left,margin-right}; iframe[origin,src,width,height]{max-width,height};',
            requiredContent: 'div(ckeditor-youtube); iframe[origin,src,width,height];',
            upcast: function( element ) {
                return element.name === 'div' && element.hasClass( 'ckeditor-youtube' );
            },
            dialog: 'youtube',
            init: function() {
                var origin = '';
                var src = '';

                var width = '';
                var height = '';

                // If there's a child (the video element)
                if ( this.element.getChild( 0 ) ) {
                    // get it's attributes.
                    origin = this.element.getChild( 0 ).getAttribute( 'origin' );
                    src = this.element.getChild( 0 ).getAttribute( 'src' );
                    width = this.element.getChild( 0 ).getAttribute( 'width' );
                    height = this.element.getChild( 0 ).getAttribute( 'height' );
                }

                if ( origin ) {
                    this.setData( 'origin', origin );
                    
                    this.setData( 'src', src );

                    if ( width ) {
                        this.setData( 'width', width );
                    }

                    if ( height ) {
                        this.setData( 'height', height );
                    }
                }
            },
            data: function() {
                // If there is an video source
                if ( this.data.origin ) {
                    // and there isn't a child (the video element)
                    if ( !this.element.getChild( 0 ) ) {
                        // Create a new <video> element.
                        var videoElement = new CKEDITOR.dom.element( 'iframe' );
                                    // Append it to the container of the plugin.
                        this.element.append( videoElement );
                    }
                    this.element.getChild( 0 ).setAttribute( 'origin', this.data.origin );

                    var src = this.data.origin;
                    if(src.indexOf("youtube") > -1){
                        src = src.replace('watch?v=', 'embed/');
                    }else if(src.indexOf("youtu.be") > -1){
                        src = src.replace('youtu.be', 'youtube.com/embed/')
                    }
                    this.data.src = src;
                    this.element.getChild( 0 ).setAttribute( 'src', this.data.src );
                    if (this.data.width) this.element.getChild( 0 ).setAttribute( 'width', this.data.width );
                    if (this.data.height) this.element.getChild( 0 ).setAttribute( 'height', this.data.height );
                }
                this.element.removeStyle( 'float' );
                this.element.removeStyle( 'margin-left' );
                this.element.removeStyle( 'margin-right' );
            }
        } );
        if ( editor.contextMenu ) {
            editor.addMenuGroup( 'youtubeGroup' );
            editor.addMenuItem( 'youtubePropertiesItem', {
                label: editor.lang.youtube.videoProperties,
                icon: 'youtube',
                command: 'youtube',
                group: 'youtubeGroup'
            });
            editor.contextMenu.addListener( function( element ) {
                if ( element &&
                     element.getChild( 0 ) &&
                     element.getChild( 0 ).hasClass &&
                     element.getChild( 0 ).hasClass( 'ckeditor-youtube' ) ) {
                    return { youtubePropertiesItem: CKEDITOR.TRISTATE_OFF };
                }
            });
        }
        CKEDITOR.dialog.add( 'youtube', this.path + 'dialogs/youtube.js' );
    }
} );
