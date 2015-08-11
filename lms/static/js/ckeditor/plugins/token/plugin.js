/**
 * @fileOverview The "token" plugin.
 *
 */

'use strict';

( function() {
	CKEDITOR.plugins.add( 'token', {
		requires: 'widget,dialog',
		lang: 'af,ar,bg,ca,cs,cy,da,de,el,en,en-gb,eo,es,et,eu,fa,fi,fr,fr-ca,gl,he,hr,hu,id,it,ja,km,ko,ku,lv,nb,nl,no,pl,pt,pt-br,ru,si,sk,sl,sq,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		icons: 'token', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%

		onLoad: function() {
			// Register styles for token widget frame.
			CKEDITOR.addCss( '.cke_token{background-color:#ff0}' );
		},

		init: function( editor ) {

			var lang = editor.lang.token;

			// Register dialog.
			CKEDITOR.dialog.add( 'token', this.path + 'dialogs/token.js' );

			// Put ur init code here.
			editor.widgets.add( 'token', {
				// Widget code.
				dialog: 'token',
				pathName: lang.pathName,
				// We need to have wrapping element, otherwise there are issues in
				// add dialog.
				template: '<span class="cke_token">${}</span>',

				downcast: function() {
					return new CKEDITOR.htmlParser.text( '${' + this.data.name + '}' );
				},

				init: function() {
					// Note that token markup characters are stripped for the name.
					this.setData( 'name', this.element.getText().slice( 2, -1 ) );
				},

				data: function() {
					this.element.setText( '${' + this.data.name + '}' );
				}
			} );

			editor.ui.addButton && editor.ui.addButton( 'CreateToken', {
				label: lang.toolbar,
				command: 'token',
				toolbar: 'insert,5',
				icon: 'token'
			} );
		},

		afterInit: function( editor ) {
			var tokenReplaceRegex = /\$\{([^\$\{\}])+\}/g;

			editor.dataProcessor.dataFilter.addRules( {
				text: function( text, node ) {
					var dtd = node.parent && CKEDITOR.dtd[ node.parent.name ];

					// Skip the case when token is in elements like <title> or <textarea>
					// but upcast token in custom elements (no DTD).
					if ( dtd && !dtd.span )
						return;

					return text.replace( tokenReplaceRegex, function( match ) {
						// Creating widget code.
						var widgetWrapper = null,
							innerElement = new CKEDITOR.htmlParser.element( 'span', {
								'class': 'cke_token'
							} );

						// Adds token identifier as innertext.
						innerElement.add( new CKEDITOR.htmlParser.text( match ) );
						widgetWrapper = editor.widgets.wrapElement( innerElement, 'token' );

						// Return outerhtml of widget wrapper so it will be placed
						// as replacement.
						return widgetWrapper.getOuterHtml();
					} );
				}
			} );
		}
	} );

} )();
