var clmenu = function(opts) {
  if (opts === undefined ) opts = {button:true}
  
  var button = '<a class="CL_MENU_TOGGLE" style="margin:0;padding:0 7px 0 7px;position:fixed;top:5px;right:15px;z-index:1000000;background-color:#333;color:#c9d2d4;" href=""><i class="fa fa-navicon"></i></a>';
  
  var menu = '<div id="CL_MENU" class="container" style="display:none;width:100%;height:100%;margin:0;padding:5px;position:fixed;top:0;left:1200;z-index:1000000;background-color:#333;"> \
    <div style="background-color:#555;width:100%;height:100%;padding:5px;"> \
      <div class="row"> \
        <div class="col-md-12"> \
          <p style="text-align:right;"><a class="CL_MENU_TOGGLE" href="" style="color:#333;margin-right:12px;margin-top:-2px;"><i class="glyphicon glyphicon-remove"></i></a></p> \
        </div> \
      </div> \
      <div class="row"> \
        <div class="col-md-12" id="CL_MENU_SELECT"> \
          <h1 style="text-align:center;"><a href="http://cottagelabs.com" style="color:#333;">COTTAGE LABS</a></h1> \
          <h3 style="text-align:center;"><a href="http://accounts.cottagelabs.com" style="color:#c9d2d4;">CL Accounts</a></h3> \
          <h3 style="text-align:center;"><a href="http://api.cottagelabs.com" style="color:#c9d2d4;">CL API</a></h3> \
          <h3 style="text-align:center;"><a href="http://harvest.cottagelabs.com" style="color:#c9d2d4;">CL Harvest</a></h3> \
          <h3 style="text-align:center;"><a href="http://lantern.cottagelabs.com" style="color:#c9d2d4;">CL Lantern</a></h3> \
          <h3 style="text-align:center;"><a href="http://openaccessbutton.org" style="color:#c9d2d4;">Open Access Button</a></h3> \
          <h3 style="text-align:center;"><a href="http://contentmine.co" style="color:#c9d2d4;">Content Mine</a></h3> \
          <h3 style="text-align:center;"><a href="http://doaj.org" style="color:#c9d2d4;">DOAJ</a></h3> \
        </div> \
      </div> \
    </div> \
  </div>';

  if (opts.button) $('body').append(button);
  $('body').append(menu);
  
  var menu_select = function(no) {
    var loc = $('#CL_MENU_SELECT').find('a').eq(no).attr('href');
    window.location = loc;
  }
  var cl_menu = function(event) {
    event ? event.preventDefault() : false;
    $('#CL_MENU').toggle();
  }
  $('.CL_MENU_TOGGLE').bind('click',cl_menu);
  Mousetrap.bind(['c l', 'right right'],cl_menu);
  Mousetrap.bind('a p i',function() { window.location = 'http://api.cottagelabs.com'; });
  // add to the api route with a way to filter the available routes?
  
  // add say to say messages. and @ to ping people or email them if they are offline?

  Mousetrap.bind('c+0',function() {menu_select(0);});
  Mousetrap.bind('c+1',function() {menu_select(1);});
  Mousetrap.bind('c+2',function() {menu_select(2);});
  Mousetrap.bind('c+3',function() {menu_select(3);});
  Mousetrap.bind('c+4',function() {menu_select(4);});
  Mousetrap.bind('c+5',function() {menu_select(5);});
  Mousetrap.bind('c+6',function() {menu_select(6);});
  Mousetrap.bind('c+7',function() {menu_select(7);});
  Mousetrap.bind('c+8',function() {menu_select(8);});
  Mousetrap.bind('c+9',function() {menu_select(9);});
  // can continue onto higher numbers if necessary via alphabet. c+a etc

}