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
                $('.edit_page').parent().before('<li><a class="jtedit_deleteit" style="color:red;" href="">delete this page</a></li>')
                $('.edit_page').parent().remove()
                editpage()
            }
            $('.edit_page').bind('click',singleedit)
            
            $('#facetview').facetview(options.facetview)
            if ( options.data && !options.data['editable'] ) {
                viewpage()
            } else if ( options.editable ) {
                if ( !options.data && options.loggedin ) {
                    var nothere = '<div class="alert alert-info"> \
                        <button class="close" data-dismiss="alert">x</button> \
                        <p><strong>There is no page here yet - create one.</strong></p> \
                        <p><strong>NOTE</strong>: creating a page does not list it in the site navigation. However, once created, you can add it using the <strong>list</strong> option above.</p> \
                        <p><strong>PLUS</strong>: a page is editable by default, which means it is displayed to anyone that can access it as editable (although only logged in users have access to the page setting buttons). Use the <strong>edit</strong> option if you want to change this to appearing as only viewable to non-logged in users whilst remaining as editable to those that are logged in, or select viewable to default to viewable for anyone (in this case, logged in users can still access the edit version from the <strong>options</strong> menu).</p> \
                        <p><strong>ALSO</strong>: pages are public by default, whether editable or not; even though they may not be listed on the navigation, anyone with the URL can access them. Once you have created your page, you can change the page to <strong>private</strong> if necessary, in which case only logged in users will be able to view it.</p>'
                    options.collaborative ? nothere += '<p>You can also share this page with others to collaboratively edit online.</p></div>' : nothere += '</div>'
                    $('.alert-messages').prepend(nothere)
                    var tid = window.location.pathname.replace(/\//g,'___')
                    tid == '___' ? tid += 'index' : ""
                    options.data = {
                        'id': tid,
                        'url': window.location.pathname,
                        'title': window.location.pathname,
                        'content': '',
                        'comments': false,
                        'embed': '',
                        'visible': false,
                        'accessible': true,
                        'editable': true,
                        'image': '',
                        'excerpt': '',
                        'tags': [],
                        'search': {
                            'format':'panels',  // panels, list
                            'hidden': true,
                            'position':'top',   // top, bottom, left, right
                            'options': {}       // like facetview options
                        }
                    }
                    $('.edit_page').parent().next().remove()
                    $('.edit_page').parent().remove()
                    editpage()
                } else if ( options.data && options.data['editable'] && options.loggedin ) {
                    $('.edit_page').parent().before('<li><a class="jtedit_deleteit" style="color:red;" href="">delete this page</a></li>')
                    $('.edit_page').parent().remove()
                    editpage()
                }
            } else {
                $('.edit_page').hide()
                $('.edit_page').parent().next().hide()
            }
            
            if (options.loggedin)
            {
                editoptions()
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
            
            if ( record["search"]["position"] == "right" ) {
                var moved = '<div class="span9">' + $('#article').html() + '</div>'
                $('#article').html(moved)
                $('#facetview').appendTo('#article')
                $('#facetview').removeClass('row-fluid').addClass('span3').addClass('onright')
            } else if ( record["search"]["position"] == "left" ) {
                var moved = '<div class="span9">' + $('#article').html() + '</div>'
                $('#article').html(moved)
                $('#facetview').prependTo('#article')
                $('#facetview').removeClass('row-fluid').addClass('span3').addClass('onleft')
            } else if ( record["search"]["position"] == "bottom" ) {
                $('#facetview').insertAfter('#article')
                $('#facetview').addClass('onbottom')
            }
            record['search']['hidden'] && $.fn.facetview.options.q.length == 0 ? $('#facetview').hide() : ""
            
            // show disqus
            if ( record["comments"] && options.comments ) {
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

            // update with any values already present in record
            // if collaborative edit is on, get the content from etherpad
            if ( options.collaborative ) {
                $('#form_content').unbind()
                $('#form_content').pad({
                  'padId'             : record.id.substring(0,50),
                  'host'              : 'http://pads.cottagelabs.com',
                  'baseUrl'           : '/p/',
                  'showControls'      : true,
                  'showChat'          : true,
                  'showLineNumbers'   : true,
                  'userName'          : 'unnamed',
                  'useMonospaceFont'  : false,
                  'noColors'          : false,
                  'hideQRCode'        : false,
                  'height'            : 400,
                  'border'            : 0,
                  'borderStyle'       : 'solid'
                })
                $('.content').css({'padding':0})
                $('#article').css({'margin-bottom':'-20px'})
                $('.alert').css({'margin-bottom':0})
            } else {
                $('#form_content').val(record['content'])
            }

            if ( options.loggedin ) {
                $('#mainnavlist').append('<li><a class="pagemedia" href="">media</a></li>')
                var showmedia = function(event) {
                    event.preventDefault()
                    !$('#absolute_media_gallery').length ? $('body').media_gallery() : ""
                }
                $('.pagemedia').bind('click',showmedia)
            } else {
                $('.content').jtedit({'data':options.data, 'makeform': false, 'actionbuttons': false, 'jsonbutton': false, 'delmsg':"", 'savemsg':"", "saveonupdate":true, "reloadonsave":""})
            }
        }


        // EDIT OPTION BUTTON FUNCTIONS
        var editoptions = function() {
            // for convenience
            var record = options.data
            
            // create page settings options panel
            var metaopts = '\
                <div id="metaopts" class="row-fluid" style="background:#eee; padding: 5px; -webkit-border-radius: 6px; -moz-border-radius: 6px; border-radius: 6px"> \
                    <div class="row-fluid"> \
                        <div class="span8"><h2>page settings</h2></div> \
                        <div class="span4"><button class="pagesettings close">x</button></div> \
                    </div> \
                    <div class="row-fluid"> \
                        <div class="span6" id="page_info"> \
                            <h3>page info</h3> \
                            <div class="row-fluid"><div class="span3"><strong>navigation title:</strong></div><div class="span9"><input type="text" class="span12 jtedit_value jtedit_title" /></div></div> \
                            <div class="row-fluid"><div class="span3"><strong>primary author:</strong></div><div class="span9"><input type="text" class="span12 jtedit_value jtedit_author" /></div></div> \
                            <div class="row-fluid"><div class="span3"><strong>brief summary:</strong></div><div class="span9"><textarea class="span12 jtedit_value jtedit_excerpt"></textarea></div></div> \
                            <div class="row-fluid"><div class="span3"><strong>featured image:</strong></div><div class="span9"><input type="text" class="span12 jtedit_value jtedit_image" /></div></div> \
                            <div class="row-fluid"><div class="span3"><strong>tags:</strong></div><div class="span9"><textarea class="span12 page_options page_tags"></textarea></div></div> \
                        </div> \
                        <div class="span6" id="access_settings"> \
                            <h3>access settings</h3> \
                            <input type="checkbox" class="page_options access_page" /> <strong>anyone can access</strong> this page without login <br> \
                            <input type="checkbox" class="page_options mode_page" /> <strong>editable by default</strong>, to anyone that can view it <br> \
                            <input type="checkbox" class="page_options nav_page" /> <strong>list this page</strong> in public nav menu and search results <br> \
                            <input type="checkbox" class="page_options page_comments" /> <strong>page comments</strong> enabled on this page<br> \
                            <br>\
                            <h3>embed content</h3> \
                            <div class="row-fluid"><div class="span2"><strong>file url:</strong></div><div class="span10"><input type="text" class="span12 page_options jtedit_value jtedit_embed" /></div></div> \
                        </div> \
                    </div> \
                    <div class="row-fluid"> \
                        <div class="row-fluid"><h3>embedded search settings</h3></div> \
                        <div class="row-fluid"> \
                            <div class="span6"> \
                                <div class="row-fluid"><div class="span3"><strong>query string:</strong></div><div class="span9"><textarea class="span12 page_options search_default"></textarea></div></div> \
                                <div class="row-fluid"><div class="span3"><strong>sort by:</strong></div><div class="span9"> \
                                    <select class="span6 page_options search_sort"> \
                                        <option value="">relevance</option> \
                                        <option value="created_desc">descending created date</option> \
                                        <option value="created_asc">ascending created date</option> \
                                    </select></div></div> \
                                <div class="row-fluid"><div class="span3"><strong>results per page:</strong></div><div class="span9"><input type="text" class="span2 page_options search_howmany" value="9" /></div></div> \
                            </div> \
                            <div class="span6"> \
                                <div class="row-fluid"><div class="span6"><strong>page location for results:</strong></div><div class="span6"> \
                                    <select class="span4 page_options search_position"> \
                                        <option value="top">top</option> \
                                        <option value="bottom">bottom</option> \
                                        <option value="left">left</option> \
                                        <option value="right">right</option> \
                                    </select></div></div> \
                                <div class="row-fluid"><div class="span6"><strong>result display format:</strong></div><div class="span6"> \
                                    <select class="span4 page_options list_search jtedit_search_format"> \
                                        <option value="panels">panels</option> \
                                        <option value="list">list</option> \
                                    </select></div></div> \
                                <div class="row-fluid"><div class="span6"><strong>Only show titles (list view):</strong></div><div class="span6"><input type="checkbox" class="page_options list_search_titles" /></div></div> \
                                <div class="row-fluid"><div class="span6"><strong>Hide results until search bar is used</strong></div><div class="span6"><input type="checkbox" class="page_options hide_search" /></div></div> \
                            </div> \
                        </div> \
                    </div> \
                    <div class="row-fluid"> \
                        <h3>advanced: raw json metadata</h3> \
                        <p>Edit the raw metadata record of this page, then save changes to it if required.</p> \
                        <div id="jtedit_space"></div> \
                    </div> \
                </div>'
            
            $('#article').before(metaopts)
            $('#metaopts').hide()
            
            var showopts = function(event) {
                event.preventDefault()
                $('#metaopts').toggle()
            }
            
            $('.pagesettings').bind('click',showopts)
            
            // set pre-existing values into page settings
            options.data['editable'] ? $('.mode_page').attr('checked',true) : ""
            options.data['accessible'] ? $('.access_page').attr('checked',true) : ""
            options.data['visible'] ? $('.nav_page').attr('checked',true) : ""
            options.data['comments'] ? $('.page_comments').attr('checked',true) : ""
            options.data['search']['hidden'] ? $('.hide_search').attr('checked',true) : ""
            options.data['search']['format'] == 'list' ? $('.list_search').attr('checked',true) : ""
            options.data['search']['onlytitles'] ? $('.list_search_titles').attr('checked',true) : ""
            if (options.data['search']['options']['paging']) {
                options.data['search']['options']['paging']['size'] ? $('.search_howmany').val(options.data['search']['options']['paging']['size']) : ""
            }
            if (options.data['search']['options']['sort']) {            
                if ( options.data['search']['options']['sort']['created_date.exact']['order'] == 'desc' ) {
                    $('.search_sort').val('created_desc')
                } else {
                    $('.search_sort').val('created_asc')
                }
            }
            options.data['search']['options']['q'] ? $('.search_default').val(options.data['search']['options']['q']) : ""
            options.data['search']['position'] ? $('.search_position').val(options.data['search']['position']) : ""
            options.data['tags'] ? $('.page_tags').val(options.data['tags']) : ""

            // handle changes to page settings
            var edits = function(event) {
                var record = $.parseJSON($('#jtedit_json').val())
                if ( $(this).hasClass('mode_page') ) {
                    $(this).attr('checked') == 'checked' ? record['editable'] = true : record['editable'] = false
                } else if ( $(this).hasClass('page_comments') ) {
                    $(this).attr('checked') == 'checked' ? record['comments'] = true : record['comments'] = false
                } else if ( $(this).hasClass('access_page') ) {
                    $(this).attr('checked') == 'checked' ? record['accessible'] = true : record['accessible'] = false
                    update_sitemap(record)
                } else if ( $(this).hasClass('nav_page') ) {
                    $(this).attr('checked') == 'checked' ? record['visible'] = true : record['visible'] = false
                    update_sitemap(record)
                } else if ( $(this).hasClass('hide_search') ) {
                    $(this).attr('checked') == 'checked' ? record['search']['hidden'] = true : record['search']['hidden'] = false
                //} else if ( $(this).hasClass('list_search') ) {
                //    $(this).attr('checked') ? record['search']['format'] = 'list' : record['search']['format'] = 'panels'
                } else if ( $(this).hasClass('list_search_titles') ) {
                    $(this).attr('checked') ? record['search']['onlytitles'] = true : record['search']['onlytitles'] = false
                } else if ( $(this).hasClass('search_position') ) {
                    record['search']['position'] = $(this).val()
                } else if ( $(this).hasClass('search_howmany') ) {
                    record['search']['options']['paging'] = {'from':0,'size':$(this).val() }
                } else if ( $(this).hasClass('search_default') ) {
                    record['search']['options']['q'] = $(this).val()
                } else if ( $(this).hasClass('page_tags') ) {
                    var tags = $(this).val().split(',')
                    record['tags'] = []
                    for ( var item in tags ) {
                        record['tags'].push($.trim(tags[item]))
                    }
                } else if ( $(this).hasClass('search_sort') ) {
                    if ( $(this).val() == "created_desc" ) {
                        record['search']['options']['sort'] = {'created_date.exact': {'order': 'desc'}}
                    } else if ( $(this).val() == "created_asc" ) {
                        record['search']['options']['sort'] = {'created_date.exact': {'order': 'asc'}}
                    } else if ( 'sort' in record['search']['options'] ) {
                         delete record['search']['options']['sort']
                    }
                }
                $('#jtedit_json').val(JSON.stringify(record,"","    "))
                $.fn.jtedit.saveit()
            }
            $('.page_options').bind('change',edits)
            
            $('#jtedit_space').jtedit({'data':options.data, 
                                        'makeform': false, 
                                        /*'actionbuttons': false, 'jsonbutton': false,*/ 
                                        'delmsg':"", 
                                        'savemsg':"", 
                                        "saveonupdate":true, 
                                        "reloadonsave":""})
        }
        
        var update_sitemap = function(record) {
            var info = {
                'visible': record['visible'],
                'accessible': record['accessible'],
                'title': record['title'],
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
        /*var showtags = function(data) {
            var tags = []
            for (var term in data.facets.tagterm.terms) {
                var val = data.facets.tagterm.terms[term]["term"]
                tags.push({'label':val,'value':'tags:'+val})
            }
            $('.facetview_searchbox').autocomplete({source:tags, minLength:0})
        }*/
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
                auto_join_text_default: "",
                auto_join_text_ed: "",
                auto_join_text_ing: "",
                auto_join_text_reply: "",
                auto_join_text_url: "",
                loading_text: "loading tweets..."
            })
        }

        // scroll to anchors with offset
        var scroller = function(event) {
            if ( $(this).attr('href').length > 1 && $(this).attr('href').substring(0,1) == '#' ) {
                event.preventDefault()
                $('html,body').animate({scrollTop: $('a[name=' + $(this).attr('href').replace('#','') +  ']').offset().top - 50}, 10)
            }
        }

        // display search area whenever required, if not already available
        var searchvis = function() {
            if ( !$('#facetview').is(':visible') || $('#facetview').hasClass('onbottom') || ( $('#facetview').hasClass('onright') && $(window).width() <= 767 ) ) {
                $('#close_facetview').remove()
                $('#facetview').prepend('<button id="close_facetview" class="close">close search results</button>')
                $('#close_facetview').css({'margin':'5px'})
                $('#close_facetview').unbind()
                var closefv = function(event) {
                    event.preventDefault()
                    $('#facetview').hide()
                }
                $('#close_facetview').bind('click',closefv)
                $('#facetview').insertBefore('#article')
                $('#facetview').removeClass('span3').removeClass('onbottom').removeClass('onright').addClass('row-fluid')                
                $('#facetview').show()
                $('#navsearch').trigger('keyup')
            }
        }

        var contactus = function(event) {
            event.preventDefault()
            
            var try_again = function(event) {
                event.preventDefault()
                
                var form = $(this).parent().siblings("form")
                $(this).parent().detach()
                form.show()
            }
            
            var form = $(this).parent()
            var message = form.children('[name="message"]').val()
            var email = form.children('[name="email"]').val()
            var action = form.attr("action")
            $.post(action, {"message" : message, "email" : email})
                .success(function() {
                    form.hide()
                    form.parent().prepend('<div class="alert alert-success" style="text-align:left;">thanks for your message! we\'ll get back to you as soon as we can</div>')
                })
                .error(function() {
                    form.hide()
                    form.parent().prepend('<div class="alert alert-error" style="text-align:left;">oops! something went wrong sending your message; please <a href="/contact" id="contact_try_again">try again</a></div>') 
                    $('#contact_try_again').bind('click', try_again)
                })
        }

        // prep showdown for displays
        var converter = false
        options['jspagecontent'] ? converter = new Showdown.converter() : ""


        return this.each(function() {
                        
            // make the topnav sticky on scroll
            var fromtop = $('#topnav').offset().top
            $(window).scroll(function() {
		        if ( $(window).scrollTop() > fromtop && $('#topnav').hasClass('navbar-in-page') ) {
                    $('#topstrap').css({height:options.bannerheight})
                    $('#tagcloud').css({height:'0px'})
                    $('#topnav').removeClass('navbar-in-page')
                    $('#topnav').addClass('navbar-fixed-top')
                    $('#mainnavlist').parent().addClass('navbar-top-pad')
                    $('body').css({'padding-top':'40px'})
                }
                if ( $(window).scrollTop() < fromtop && $('#topnav').hasClass('navbar-fixed-top') ) {
                    $('#topnav').removeClass('navbar-fixed-top')
                    $('#mainnavlist').parent().removeClass('navbar-top-pad')
                    $('#topnav').addClass('navbar-in-page')
                    $('body').css({'padding-top':'0px'})
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
            $('.facetview_searchbox').bind('focus',searchvis)

            // bind anchor scroller offset fix
            $('a').bind('click',scroller)

            // setup the tag cloud functionality
            options.tagkey ? buildtagcloud() : false

            // bind the twitter display if twitter account provided
            options.twitter ? tweets() : false
            
            // add the contact us form handler
            $('#submit_contact').bind('click', contactus)
            
            // get going. for now it is assumed that the record is provided in the options. but could pull from a source, similar to jtedit
            makepage()

        })

    }

    // options are declared as a function so that they can be retrieved
    // externally (which allows for saving them remotely etc)
    $.fn.jsite.options = {}

})(jQuery)

