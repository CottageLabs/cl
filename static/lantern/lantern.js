jQuery(document).ready(function() {
	$('#footer').hide();
	
  var file;
	var filename = '';
  var results = [];
	var dois = 0;
	var pmcids = 0;
	var pmids = 0;
	var titles = 0;
  var review = function() {
		//console.log(results);
    console.log(results.length);
    console.log(dois);
    console.log(pmcids);
    console.log(pmids);
    console.log(titles);
		if ( $('#review').length ) {
			$('#count').html(results.length);
			var numbers = '';
			if (dois > 0) numbers += dois + ' DOIs<br>';
			if (pmcids > 0) numbers += pmcids + ' PMC IDs<br>';
			if (pmids > 0) numbers += pmids + ' PubMed IDs<br>';
			if (titles > 0) numbers += titles + ' titles<br>';
			$('#idnumbers').html(numbers);
			//$('#review').append(JSON.stringify(results));
			$('#review').show();
		}
  }
  var transform = function(split,wrap) {
		results = [];
		dois = 0;
		pmcids = 0;
		pmids = 0;
		titles = 0;
		if (split === undefined) split = ',';
		if (wrap === undefined) wrap = '"';
		var wrapreplace = new RegExp(wrap,"g");
		// could try to look for split and wrap chars in file somehow - looking at first char is no good because systems/people sometimes only use the wraps 
		// when they must, like when surrounding content with a comma, but do not bother at other times
		
    file = file.replace(/\r\n/g,'\n'); // switch MS line breaks to unix
    file = file.replace(/\n{2,}/g,'\n'); // get rid of any blank lines
    file = file.replace(/\n*$/g,''); // remove newlines at end of file
		
		var lines = [];
		var fls = file.split('\n');
		console.log(fls.length);
		var il = '';
		for ( var f in fls ) {
			il += fls[f];
			if ( il.split(wrap).length % 2 !== 0 ) {
				lines.push(il);
				il = '';
			}
		}
		console.log(lines.length);
		var headers = [];
		var hline = lines.shift();
		var hlines = hline.split(split);
		var hl = '';
		for ( var h in hlines ) {
			if (hl.length > 0) hl += ',';
			hl += hlines[h];
			if ( hl.split(wrap).length % 2 !== 0 ) {
				hl = hl.replace(wrapreplace,'').replace(/(^\s*)|(\s*$)/g,''); // strip whitespace leading and ending header names
				//hl = hl.toLowerCase().replace(/ /g,'_').replace(/[^a-z0-9_]/g,'');; // could do additional header cleaning here
				headers.push(hl);
				hl = '';
			}
		}
		console.log(headers);
		
    for (var i = 0; i < lines.length; i++) {
			var obj = {};
			var currentline = lines[i].split(split);
			var cl = '';
			var counter = 0;
			var lengths = 0;
			for ( var col in currentline ) {
				if (cl.length > 0) cl += ',';
				cl += currentline[col];
				if ( cl.split(wrap).length % 2 !== 0 ) {
					cl = cl.replace(wrapreplace,'');
					obj[headers[counter]] = cl;
					if (lengths === 0) lengths = cl.length;
					cl = '';
					counter += 1;
				}
			}
			if (obj.doi || obj.DOI) dois += 1;
			if (obj.pmcid || obj.PMCID) pmcids += 1;
			if (obj.pmid || obj.PMID) pmids += 1;
			if (obj.title || obj['Article title']) titles += 1;
			if (lengths) results.push(obj);
		}
    review();
  }
  var prep = function(e) {
		var f = e.target.files[0];
		filename = f.name;
		var reader = new FileReader();
		reader.onload = (function(theFile) {
			return function(e) {
				file = e.target.result;
				transform();
			};
		})(f);
		reader.readAsText(f);
  }
  $('input[type=file]').on('change', prep);

	var error = function(data) {
		$('#lanternmulti').show();
		$('#submitting').hide();
		$('#errormsg').html('<p>Sorry, there has been an error with your submission. Please try again.</p><p>If you continue go receive an error, please contact us@cottagelabs.com with the following error information:</p><p>' + JSON.stringify(data) + '</p>').show();
    console.log(data);
  }

	var done = false;
	var poll, hash;
	var polling = function(data) {
		console.log('poll returned');
		console.log(data);
		$('.uploader').hide();
		$('#poller').show();
		if ( !data.data ) data.data = 0;
		var status = '<p>Your job is ' + data.data + '% complete.</p>';
		status += '<p><a href="//dev.api.cottagelabs.com/service/lantern/' + hash + '/results?format=csv" class="btn btn-default btn-block">Download your results</a></p>';
		status += '<p style="text-align:center;padding-top:10px;"><a href="//dev.api.cottagelabs.com/service/lantern/' + hash + '/original" style="font-weight:normal;">or download your original spreadsheet</a></p>';
		if (data.data !== 100) setTimeout(poll,10000);
		$('#pollinfo').html(status);
	}
	poll = function(hash) {
		if (hash === undefined) {
			hash = window.location.hash.replace('#','');
		}
		if ( hash ) {
			$.ajax({
				url: '//dev.api.cottagelabs.com/service/lantern/' + hash + '/progress',
				method: 'GET',
				success: polling,
				error: error
			});		
		}
	}
	
	if (window.location.hash) {
		$('.uploader').hide();
		hash = window.location.hash.replace('#','');
		console.log(hash);
		poll(hash);
	}
	
  var success = function(data) {
		$('#lanternmulti').show();
		$('#submitting').hide();
    console.log(data);
		try {
			window.history.pushState("", "poll", '#' + data.data.job);
		} catch (err) {}
		hash = data.data.job;
		poll(data.data.job);
  }
  var submit = function(e) {
		$('#errormsg').html("").hide();
		e.preventDefault();
		var email;
		try {
			var logged = LoginState.get("clogins");
			email = logged.email;
		} catch(err) {}
		if (!email) email = $('#email').val();
		if (!email) {
			$('#errormsg').html('You must provide an email address in order to submit a job. Please do so, and try again.').show();
		} else {
			$('#lanternmulti').hide();
			$('#submitting').show();
			if ( $('#ident').val() && $('#ident').val().length > 0 ) {
				var vl = $('#ident').val();
				var pl = {};
				if ( vl.indexOf('/') !== -1 ) {
					pl.doi = vl;
				} else if (vl.toLowerCase().indexOf('pmc') !== -1) {
					pl.pmcid = vl;
				} else {
					pl.pmid = vl;
				}
				results = [pl];
			}
			var payload = {list:results,name:filename,email:email};
			$.ajax({
				url: '//dev.api.cottagelabs.com/service/lantern',
				method: 'POST',
				data: JSON.stringify(payload),
				dataType: 'JSON',
				contentType: "application/json; charset=utf-8",
				success: success,
				error: error
			});
		}
  }
  $('#lanternmulti').bind('click',submit);
  
});