jQuery(document).ready(function() {
	
	var apibaseurl = '//dev.api.cottagelabs.com';
	
  var file;
	var filename = '';
  var results = [];
	var dois = 0;
	var pmcids = 0;
	var pmids = 0;
	var titles = 0;
	
  var review = function() {
		//console.log(results);
    //console.log(results.length);
    //console.log(dois);
    //console.log(pmcids);
    //console.log(pmids);
    //console.log(titles);
		if ( $('#review').length ) {
			var msg = '<p style="color:black;">Thank you. Your file appears to have ';
			msg += results.length;
			msg += ' record rows, containing<br>';
			if (dois > 0) msg += dois + ' DOIs<br>';
			if (pmcids > 0) msg += pmcids + ' PMC IDs<br>';
			if (pmids > 0) msg += pmids + ' PubMed IDs<br>';
			if (titles > 0) msg += titles + ' titles<br>';
			msg += 'Please submit for processing now:</p>';
			$('#review').html(msg).show();
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
		var il = '';
		for ( var f in fls ) {
			il += fls[f];
			if ( il.split(wrap).length % 2 !== 0 ) {
				lines.push(il);
				il = '';
			}
		}
		if (lines.length > 3001) {
			$('#errormsg').html('<p style="color:black;">Sorry, the maximum amount of rows you can submit in one file is 3000. Please reduce the size of your file and try again.</p>').show();
			file = undefined;
			filename = '';
		} else {
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
						if (headers[counter] && headers[counter].length > 0) obj[headers[counter]] = cl;
						if (lengths === 0) lengths = cl.length;
						cl = '';
						counter += 1;
					}
				}
				if (obj.doi || obj.DOI) dois += 1;
				if (obj.pmcid || obj.PMCID) pmcids += 1;
				if (obj.pmid || obj.PMID) pmids += 1;
				if (obj.title || obj['Article title'] || obj['Article Title']) titles += 1;
				if (lengths) results.push(obj);
			}
			review();
		}
  }

	function readBinaryStringFromBlob(blob, callback, ie) {
		var reader = new FileReader();
		if(!ie) {
			reader.addEventListener("loadend", function () {
				file = reader.result;
				transform();
			});
			try {
				reader.readAsBinaryString(blob);
			} catch (err) {
				readBinaryStringFromBlob(blob, callback, true);
			}
		} else {
			reader.addEventListener("loadend", function () {
				var binary = "";
				var bytes = new Uint8Array(reader.result);
				var length = bytes.byteLength;
				for (var i = 0; i < length; i++) {
					binary += String.fromCharCode(bytes[i]);
				}
				file = binary;
				callback();
			});
			reader.readAsArrayBuffer(blob);
		}
	}

  var prep = function(e) {
		var f;
		if( window.FormData === undefined ) {
			f = (e.files || e.dataTransfer.files);
		} else {
			f = e.target.files[0];
		}
		filename = f.name;
		/*var reader = new FileReader();
		reader.onload = (function(theFile) {
			return function(e) {
				file = e.target.result;
				transform();
			};
		})(f);
		reader.readAsBinaryString(f);*/
		readBinaryStringFromBlob(f,transform);
  }

	var error = function(data) {
		$('#lanternmulti').show();
		$('#submitting').hide();
		$('#errormsg').html('<p style="color:black;">Sorry, there has been an error with your submission. Please try again.<br>If you continue go receive an error, please contact us@cottagelabs.com attaching a copy of your file and with the following error information:<br>' + JSON.stringify(data) + '</p>').show();
  }

	var done = false;
	var poll, hash;
	var polling = function(data) {
		//console.log('poll returned');
		$('.uploader').hide();
		$('#poller').show();
		var progress = !data.data || !data.data.progress ? 0 : data.data.progress;
		var pc = (Math.floor(progress * 10))/10;
		var status = '<p>Job ';
		status += data.data && data.data.name ? data.data.name : '#' + data.data._id;
		status += '</p>';
		if (data.data && data.data.new === true) status += '<p>Your job is new, and is still being loaded into the system. For large jobs this may take a couple of minutes.</p>';
		status += '<p>Your job is ' + pc + '% complete.</p>';
		status += '<p><a href="' + apibaseurl + '/service/lantern/' + hash + '/results?format=csv" class="btn btn-default btn-block">Download your results</a></p>';
		status += '<p style="text-align:center;padding-top:10px;"><a href="' + apibaseurl + '/service/lantern/' + hash + '/original" style="font-weight:normal;">or download your original spreadsheet</a></p>';
		if (data.data.progress !== 100) setTimeout(poll,10000);
		$('#pollinfo').html(status);
	}
	
	poll = function(hash) {
		if (hash === undefined) {
			hash = window.location.hash.replace('#','');
		}
		if ( hash ) {
			$.ajax({
				url: apibaseurl + '/service/lantern/' + hash + '/progress?apikey='+clogin.apikey,
				method: 'GET',
				success: polling,
				error: error
			});		
		}
	}
	
  var success = function(data) {
		$('#lanternmulti').show();
		$('#submitting').hide();
    //console.log(data);
		try {
			window.history.pushState("", "poll", '#' + data.data.job);
		} catch (err) {}
		hash = data.data.job;
		poll(data.data.job);
  }
	
  var submit = function(e) {
		$('#errormsg').html("").hide();
		e.preventDefault();
		if ( !(( $('#ident').length && $('#ident').val().length ) || filename) ) {
			$('#errormsg').html('<p style="color:black;">You must provide at least an ID or a file with at least one record in order to submit. Please provide more information and try again.</p>').show();
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
			var payload = {list:results,name:filename};
			try { payload.email = $('#email').val(); } catch(err) {}
			$.ajax({
				url: apibaseurl + '/service/lantern?wellcome=true',
				method: 'POST',
				data: JSON.stringify(payload),
				dataType: 'JSON',
				contentType: "application/json; charset=utf-8",
				success: success,
				error: error
			});
		}
  }

	var startup = function() {
	  $('input[type=file]').on('change', prep);
	  $('#lanternmulti').bind('click',submit);
		document.title = 'Wellcome compliance tool';
		$('#footer').hide();
		if (window.location.hash) {
			setTimeout(function() {$('.uploader').hide();},200);
			$('#poller').show();
			$('#pollinfo').html('<p>One moment please, retrieving job status...</p>');
			hash = window.location.hash.replace('#','');
			console.log(hash);
			poll(hash);
		}
	}
	

});
