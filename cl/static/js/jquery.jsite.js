/*
 * jquery.jsite.js
 *
 * a tool for controlling edit functionality on the CL website
 * almost abstracted enough to be used as a lib on other sites
 *
 * DOES NOT WORK WITHOUT jquery.jtedit.js and jquery.facetview.js
 * 
 * created by Mark MacGillivray - mark@cottagelabs.com
 *
 * copyheart 2012. http://copyheart.org
 *
 */

(function($){
    $.fn.jsite = function(options) {


//------------------------------------------------------------------------------
        // READY THE DEFAULTS

        // specify the defaults - currently pushed from Flask settings
        var defaults = {}

        // and add in any overrides from the call
        $.fn.jsite.options = $.extend(defaults,options)
        var options = $.fn.jsite.options
        

//------------------------------------------------------------------------------
        // BUILD THE PAGE CONTENT SECTION
        var makepage = function() {
            var singleedit = function(event) {
                event.preventDefault()
                if ( options.data['mode'] == 'viewable' ) {
                    var onlyyou = '<div class="alert alert-info"> \
                        <button class="close" data-dismiss="alert">x</button> \
                        <p>You are editing this page, but the page edit mode is still set to <strong>viewable</strong>. \
                        If you want this page to be displayed as <strong>editable</strong> by default, change the edit option above. \
                        If you want it to appear editable to logged in users but remain only viewable to non-logged in users, change \
                        the edit option to <strong>login to edit</strong></p></div>'
                    $('.alert-messages').prepend(onlyyou)
                } else if ( options.data['mode'] == 'logineditable' ) {
                    var onlyyou = '<div class="alert alert-info"> \
                        <button class="close" data-dismiss="alert">x</button> \
                        <p>You are editing this page, but the page mode is still set to <strong>edit with login</strong>. \
                        Any logged in user will see the page as editable by default, but an unlogged user will not. \
                        If you want this page to be displayed as <strong>editable</strong> for anyone by default, change the edit option above to <strong>editable</strong>. \
                        (and make sure the access level is set to public).</p></div>'
                    $('.alert-messages').prepend(onlyyou)
                }
                editpage()
            }
            $('.edit_page').bind('click',singleedit)
            $('#facetview').facetview(options.facetview)
            if ( options.data && options.data['mode'] != 'editable' && options.data['mode'] != 'logineditable') {
                viewpage()
            } else if ( options.editable ) {
                if ( !options.data && options.loggedin ) {
                    var nothere = '<div class="alert alert-info"> \
                        <button class="close" data-dismiss="alert">x</button> \
                        <p><strong>There is no page here yet - create one.</strong></p> \
                        <p><strong>NOTE</strong>: creating a page does not list it in the site navigation. However, once created, you can add it using the <strong>list</strong> option above.</p> \
                        <p><strong>PLUS</strong>: a page is editable by default, which means it is displayed to anyone that can access it as editable (although only logged in users have access to the page setting buttons). Use the <strong>edit</strong> option if you want to change this to appearing as only viewable to non-logged in users whilst remaining as editable to those that are logged in, or select viewable to default to viewable for anyone (in this case, logged in users can still access the edit version from the <strong>options</strong> menu).</p> \
                        <p><strong>ALSO</strong>: pages are public by default, whether editable or not; even though they may not be listed on the navigation, anyone with the URL can access them. Once you have created your page, you can change the page to <strong>private</strong> if necessary, in which case only logged in users will be able to view it.</div>'
                    options.collaborative ? nothere += '<p>You can also share this page with others to collaboratively edit online.</p>' : ''
                    $('.alert-messages').prepend(nothere)
                    var tid = window.location.pathname.replace(/\//g,'___')
                    tid == '___' ? tid += 'index' : ""
                    options.data = {
                        'id': tid,
                        'url': window.location.pathname,
                        'comments': false,
                        'embed': false,
                        'content': '',
                        'listed': false, // false, true
                        'access': 'public', // public, private
                        'mode': 'editable', // editable, logineditable, viewable
                        'tags': [],
                        'search': {
                            'format':'panels',  // panels, list
                            'hidden': true,     // true, false
                            'position':'top',   // top, right
                            'options': {}       // like facetview options
                        },
                        'media': {
                            'hidden': true,
                            'position': 'top',  // top, right
                            'content': []       // list of media file urls
                        }
                    }
                    $('.edit_page').parent().next().remove()
                    $('.edit_page').parent().remove()
                    editpage()
                } else if ( options.data && ( options.data['mode'] == 'editable' || ( options.data['mode'] == 'logineditable' ) && options.loggedin ) ) {
                    $('.edit_page').parent().before('<li><a class="jtedit_deleteit" style="color:red;" href="">delete this page</a></li>')
                    $('.edit_page').parent().remove()
                    editpage()
                }
            } else {
                $('.edit_page').hide()
                $('.edit_page').parent().next().hide()
            }
        }
        
        
        // VIEW A PAGE AS NORMAL
        var viewpage = function() {
            var record = options.data

            // if page content to be built by js (alt. can be built by backend first)
            if ( options.jspagecontent ) {
                $('#article').html("")    // empty the article block
                // display any embedded content
                if ( record["embed"] && record["embed"] != "undefined" ) {
                    var embed = '<div class="span12">'
                    if ( ( record["embed"].indexOf("/pub?") != -1 ) && ( record["embed"].indexOf("docs.google.com") != -1 ) ) {
                        embed += '<iframe id="embedded" src="' + record["embed"] +
                            '&amp;embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
                    } else {
                        $('.content').css({"overflow":"hidden","padding":0})
                        embed += '<iframe id="embedded" src="http://docs.google.com/viewer?url=' + record["embed"] +
                            '&embedded=true" width="100%" height="1000" style="border:none;"></iframe>'
                    }
                    embed += '</div>'
                    $('#article').prepend(embed)
                }

                // display the page content
                var content = '<div class="span12">' + converter.makeHtml(record["content"]) + '</div>'
                $('#article').prepend(content)
            }
            
            if ( record["search"] == "list" ) {
                // move search to the right, and alter style
                $('#facetview').appendTo('#article')
                $('#facetview').removeClass('row-fluid').addClass('span4')
                $('#article > .span12').addClass('span8').removeClass('span12')
            }
            record['search']['hidden'] ? $('#facetview').hide() : ""
            
            // show disqus
            if ( record["comments"] == "on" && options.comments ) {
                var disqus = '<div id="comments" class="container"><div class="comments"><div class="row-fluid" id="disqus_thread"></div></div></div> \
                    <script type="text/javascript"> \
                    var disqus_shortname = "' + options.comments + '"; \
                    (function() { \
                        var dsq = document.createElement("script"); dsq.type = "text/javascript"; dsq.async = true; \
                        dsq.src = "http://" + disqus_shortname + ".disqus.com/embed.js"; \
                        (document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0]).appendChild(dsq); \
                    })(); \
                </script>'
                $('#main').after(disqus)
            }
        }

        
        // SHOW EDITABLE VERSION OF PAGE
        var editpage = function(event) {
            event ? event.preventDefault() : ""
            var record = options.data
        
            $('#facetview').hide()
            $('#article').html("")
                                    
            if ( record['embed'] ) {
                // show embed options
            } else {
                var editor = '<div class="row-fluid" style="margin-bottom:20px;"><div class="span12"><textarea class="tinymce jtedit_value jtedit_content" id="form_content" name="content" style="width:99%;min-height:300px;" placeholder="content. text, markdown or html will work."></textarea></div></div>'
                $('#article').append(editor)

                if ( options.richtextedit ) {
		            $('textarea.tinymce').tinymce({
			            script_url : '/static/vendor/tinymce/jscripts/tiny_mce/tiny_mce.js',
			            theme : "advanced",
			            plugins : "autolink,lists,style,layer,table,advimage,advlink,inlinepopups,media,searchreplace,contextmenu,paste,fullscreen,noneditable,nonbreaking,xhtmlxtras,advlist",
			            theme_advanced_buttons1 : "bold,italic,underline,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,|,forecolor,backcolor,|,bullist,numlist,|,outdent,indent,blockquote,|,sub,sup,|,styleprops",
			            theme_advanced_buttons2 : "undo,redo,|,cut,copy,paste,|,search,replace,|,hr,link,unlink,anchor,image,charmap,media,table,|,insertlayer,moveforward,movebackward,absolute,|,cleanup,code,help,visualaid,fullscreen",
			            theme_advanced_toolbar_location : "top",
			            theme_advanced_toolbar_align : "left",
			            theme_advanced_statusbar_location : "bottom",
			            theme_advanced_resizing : true,

		            })
		        }
		    }

            if ( options.loggedin ) {
                // provide embedded gallery options
                var galleryopts = '<div id="galleryopts" class="row-fluid"><div class="hero-unit">'
                galleryopts += 'gallery options here - embed gallery on page, choose which to show, add from link or upload</div></div>'
                for (var item in record['media']['content'] ) {
                    var thing = '<img class="img thumbnail" src="' + item + '" />'
                    $('#gallery > .hero-unit').append(thing)
                }
                $('#article').after(galleryopts)
                record['media']['hidden'] ? $('#galleryopts').hide() : ""

                // provide the search panel options
                var searchopts = '<div id="searchopts" class="row-fluid"><div class="hero-unit">search options here - top,bottom,left,right,hidden,style,filters,resultsize</div></div>'
                $('#article').after(searchopts)
                record['search']['hidden'] ? $('#searchopts').hide() : ""

            }
                        
            // update with any values already present in record
            // if collaborative edit is on, get the content from the sharejs socket rather than the record
            if ( options.collaborative ) {
                // get page content from sharejs socket server
                // add a check for difference between share data and es data...
                var elem = document.getElementById("form_content")
                sharejs.open('hello', 'text', options.collaborative, function(error, doc) {
	                if (error) {
		                console.log(error)
	                } else {
		                elem.disabled = false
		                doc.attach_textarea(elem)
	                }
                })
            } else {
                $('#form_content').val(record['content'])
            }
            options.loggedin ? editoptions() : ""
            $('.content').jtedit({'data':options.data, 'makeform': false, /*'actionbuttons': false, 'jsonbutton': false,*/ 'delmsg':"", 'savemsg':"", "saveonupdate":true, "reloadonsave":""})
        }


        // EDIT OPTION BUTTON FUNCTIONS
        var editoptions = function() {
            $('#editoptions').show()
            var editopts = '<div class="btn-group" style="float:left;"><button class="btn btn-small mode_page">editable</button><button class="btn btn-small mode_page">login to edit</button><button class="btn btn-small mode_page">viewable</button></div>'

            if ( window.location.pathname != '/' ) {
                editopts += '<div class="btn-group" style="float:left;"><button class="btn btn-small access_page">public</button><button class="btn btn-small access_page">private</button></div>'
                editopts += '<div class="btn-group" style="float:left;"><button class="btn btn-small nav_page">unlisted</button><button class="btn btn-small nav_page">listed</button></div>'
            }
            editopts += '<div class="btn-group" style="float:left;"><button class="btn btn-small init_search">show search</button><button class="btn btn-small init_search">hide search</button></div>'
            editopts += '<div class="btn-group" style="float:left;"><button class="btn btn-small page_comments">comments off</button><button class="btn btn-small page_comments">comments on</button></div>'
            editopts += '<button class="btn btn-small page_media" style="margin-left:5px;">media <span class="caret"></span></button>'
            editopts += '<button class="btn btn-small page_meta" style="margin-left:5px;">meta <span class="caret"></span></button>'

            $('#editoptions').append(editopts)
            if ( options.data['mode'] == 'editable' ) {
                $('.mode_page').eq(0).addClass('btn-info').addClass('active')
            } else if ( options.data['mode'] == 'logineditable' ) {
                $('.mode_page').eq(1).addClass('btn-info').addClass('active')
            } else {
                $('.mode_page').eq(2).addClass('btn-info').addClass('active')
            }
            options.data['access'] == 'public' ? $('.access_page').eq(0).addClass('btn-info').addClass('active') : $('.access_page').eq(1).addClass('btn-info').addClass('active')
            !options.data['comments'] ? $('.page_comments').eq(0).addClass('btn-info').addClass('active') : $('.page_comments').eq(1).addClass('btn-info').addClass('active')
            !options.data['search']['hidden'] ? $('.init_search').eq(0).addClass('btn-info').addClass('active') : $('.init_search').eq(1).addClass('btn-info').addClass('active')
            options.data['listed'] ? $('.nav_page').eq(1).addClass('btn-info').addClass('active') : $('.nav_page').eq(0).addClass('btn-info').addClass('active')

            options.collaborative ? $('#form_content').unbind() : ""
            $('#editoptions').append('<div style="clear:both;height:0;"></div>')
            
            var edits = function(event) {
                event.preventDefault()
                $('.alert').remove()
                var record = $.parseJSON($('#jtedit_json').val())
                var refresh = false
                if ( $(this).hasClass('mode_page') ) {
                    if ($(this).html() == 'editable') {
                        record['mode'] = 'editable'
                        $('.mode_page').removeClass('btn-info').removeClass('active')
                        $('.mode_page').eq(0).addClass('btn-info').addClass('active')
                    } else if ( $(this).html() == 'login to edit' ) {
                        record['mode'] = 'logineditable'
                        $('.mode_page').removeClass('btn-info').removeClass('active')
                        $('.mode_page').eq(1).addClass('btn-info').addClass('active')
                    } else {
                        record['mode'] = 'viewable'
                        $('.mode_page').removeClass('btn-info').removeClass('active')
                        $('.mode_page').eq(2).addClass('btn-info').addClass('active')
                        refresh = true
                    }
                }
                if ( $(this).hasClass('page_comments') ) {
                    if ($(this).html() == 'comments off') {
                        record['comments'] = false
                        $('.page_comments').eq(0).addClass('btn-info').addClass('active')
                        $('.page_comments').eq(1).removeClass('btn-info').removeClass('active')
                    } else {
                        record['comments'] = true
                        $('.page_comments').eq(0).removeClass('btn-info').removeClass('active')
                        $('.page_comments').eq(1).addClass('btn-info').addClass('active')
                    }
                }
                if ( $(this).hasClass('init_search') ) {
                    if ($(this).html() == 'show search') {
                        record['search']['hidden'] = false
                        $('.init_search').eq(0).addClass('btn-info').addClass('active')
                        $('.init_search').eq(1).removeClass('btn-info').removeClass('active')
                        $('#searchopts').show()
                    } else {
                        record['search']['hidden'] = true
                        $('.init_search').eq(0).removeClass('btn-info').removeClass('active')
                        $('.init_search').eq(1).addClass('btn-info').addClass('active')
                        $('#searchopts').hide()
                        var searchy = '<div class="alert alert-info"> \
                            <button class="close" data-dismiss="alert">x</button> \
                            <p>Search set to <strong>hidden</strong>. \
                            When this page is loaded, search results will not be visible; however when the search bar is used, the search results will come into view.</p> \
                            <p>Other search options are available, set to visible to view the search pane and edit the options there if desired. Those options \
                            will take effect whenever the search results panel becomes visible.</p></div>'
                        $('.alert-messages').prepend(searchy)
                    }
                }
                if ( $(this).hasClass('access_page') ) {
                    if ($(this).html() == 'public') {
                        record['access'] = 'public'
                        $('.access_page').eq(0).addClass('btn-info').addClass('active')
                        $('.access_page').eq(1).removeClass('btn-info').removeClass('active')
                    } else {
                        record['access'] = 'private'
                        $('.access_page').eq(0).removeClass('btn-info').removeClass('active')
                        $('.access_page').eq(1).addClass('btn-info').addClass('active')
                        var onlyyou = '<div class="alert alert-info"> \
                            <button class="close" data-dismiss="alert">x</button> \
                            <p>Page mode changed to <strong>private</strong>. \
                            Only logged in users will be able to acces it, regardless of edit mode.</p></div>'
                        $('.alert-messages').prepend(onlyyou)
                    }
                    update_sitemap(record)
                }
                if ( $(this).hasClass('nav_page') ) {
                    if ($(this).html() == 'unlisted') {
                        record['listed'] = false
                        $('.nav_page').eq(0).addClass('btn-info').addClass('active')
                        $('.nav_page').eq(1).removeClass('btn-info').removeClass('active')
                    } else {
                        record['listed'] = true
                        $('.nav_page').eq(0).removeClass('btn-info').removeClass('active')
                        $('.nav_page').eq(1).addClass('btn-info').addClass('active')
                    }
                    update_sitemap(record)
                }
                $('#jtedit_json').val(JSON.stringify(record,"","    "))
                $.fn.jtedit.saveit(refresh)
            }
            $('.mode_page').bind('click',edits)
            $('.access_page').bind('click',edits)
            $('.page_comments').bind('click',edits)
            $('.init_search').bind('click',edits)
            $('.nav_page').bind('click',edits)
            
            var showmedia = function(event) {
                event.preventDefault()
                $('#galleryopts').show()
                $('body').media_gallery()
            }
            var pagemeta = function(event) {
                event.preventDefault()
                alert('for now just shows jtedit box. should perhaps be customised via jtedit instead')
                $('#jtedit_json').toggle()
            }
            $('.page_media').bind('click',showmedia)
            $('.page_meta').bind('click',pagemeta)
        }
        
        var update_sitemap = function(record) {
            var info = {
                'listed': record['listed'],
                'access': record['access'],
                'url': window.location.pathname
            }
            var url = '/sitemap' + window.location.pathname
            $.ajax({ 
                type: 'POST', 
                url: url, 
                data: JSON.stringify(info),
                contentType: "application/json; charset=utf-8"
            })
        }


//------------------------------------------------------------------------------
        // TAG CLOUD
        var tagcloud = function(event) {
            $('.alert').remove()
            if ( $('.navbar-in-page').length ) {
                $('#topstrap').animate({height:'60px'},{duration:500})
                $('#tagcloud').animate({height:'185px'},{duration:500})
            } else {
                $('html,body').scrollTop($('#facetview').offset().top - 20)
            }
            $('#navsearch').animate({width:'400px'},{duration:500})
        }

        var detagcloud = function(event) {
            if ( $('.navbar-in-page').length ) {
                jQuery('#topstrap').animate({height:options.bannerheight},{duration:500})
                jQuery('#tagcloud').animate({height:'0px'},{duration:500})
            }
            jQuery('#navsearch').animate({width:'200px'},{duration:500})
        }

        var dotagsearch = function(event) {
            event.preventDefault()
            var tag = $(this).html()
            $('#navsearch').val(options.tagkey+':'+tag)
            $('#navsearch').trigger('keyup')
        }
        var showtags = function(data) {
            for (var term in data.facets.tagterm.terms) {
                var val = data.facets.tagterm.terms[term]["term"]
                var termlink = '<a class="tagsearch" href="?q=' + val + '">' + val + '</a> '
                $('#tagcloud > p').append(termlink)
            }
            $('.tagsearch').bind('click',dotagsearch)
        }
        var buildtagcloud = function() {
            var query = {
                "query":{
                    "match_all":{}
                },
                "facets":{
                    "tagterm":{
                        "terms":{
                            "field":options.tagkey,
                            "size":100
                        }
                    }
                }
            }
            $.ajax({
                type: "get",
                url: options.searchurl,
                data: {source: JSON.stringify(query) },
                // processData: false,
                dataType: options.datatype,
                success: showtags
            })
            jQuery('#navsearch').bind('focus',tagcloud)
            jQuery('#navsearch').bind('blur',detagcloud)
        }


//------------------------------------------------------------------------------
        // TWEETS
        var tweets = function() {
            $(".tweet").tweet({
                username: options.twitter,
                avatar_size: 48,
                count: 5,
                join_text: "auto",
                auto_join_text_default: "we said,",
                auto_join_text_ed: "we",
                auto_join_text_ing: "we were",
                auto_join_text_reply: "we replied",
                auto_join_text_url: "we read ",
                loading_text: "loading tweets..."
            })
        }


        // attach a selectall to the search bar, and ensure search is visible on search
        var selectall = function(event) {
            event.preventDefault()
            $(this).select()
        }
        var searchvis = function() {
            if ( !$('#facetview').is(':visible') ) {
                $('#facetview').show()
            }
        }

        // prep showdown for displays
        var converter = false
        options['jspagecontent'] ? converter = new Showdown.converter() : ""


        return this.each(function() {
            
            // make the topnav sticky on scroll
            var fromtop = $('#topnav').offset().top + 40
            $(window).scroll(function() {
		        if ( $(window).scrollTop() > fromtop && $('#topnav').hasClass('navbar-in-page') ) {
                    $('#topnav').removeClass('navbar-in-page')
                    $('#topnav').addClass('navbar-fixed-top')
                    $('#mainnavlist').parent().addClass('navbar-top-pad')
                }
                if ( $(window).scrollTop() < fromtop && $('#topnav').hasClass('navbar-fixed-top') ) {
                    $('#topnav').removeClass('navbar-fixed-top')
                    $('#mainnavlist').parent().removeClass('navbar-top-pad')
                    $('#topnav').addClass('navbar-in-page')
                }
            })

            // bind new page creation to new page button
            var newpage = function(event) {
                event.preventDefault()
                var subaddr = window.location.pathname
                subaddr.charAt(subaddr.length-1) != '/' ? subaddr += '/' : ""
                var newaddr = prompt('what / where ?',subaddr)
                newaddr.indexOf('/null') == -1 ? window.location = newaddr : ""
            }
            $('#new_page').bind('click',newpage)

            // bind search display
            $('#navsearch').bind('focus',searchvis)
            $('#navsearch').bind('mouseup',selectall)

            // setup the tag cloud functionality
            options.tagkey ? buildtagcloud() : false

            // bind the twitter display if twitter account provided
            options.twitter ? tweets() : false
            
            // get going. for now it is assumed that the record is provided in the options. but could pull from a source, similar to jtedit
            makepage()

        })

    }

    // options are declared as a function so that they can be retrieved
    // externally (which allows for saving them remotely etc)
    $.fn.jsite.options = {}

})(jQuery)

