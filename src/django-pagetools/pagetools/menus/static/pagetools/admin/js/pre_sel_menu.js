// Read a page's GET URL variables and return them as an associative array.

//  - not my work
function getUrlVars() {
	var vars = [], hash;
	var hashes = window.location.href.slice(
			window.location.href.indexOf('?') + 1).split('&');
	for ( var i = 0; i < hashes.length; i++) {
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	return vars;
}

(function($) {
	$(document).ready(
		function() {
			var uvars = getUrlVars();
			if ('menu' in uvars) {
				$s = $("#id_menus").find("option[value="+ uvars['menu']+"]");
				$s.attr('selected',true);//.select();
			}
		})
})(grp.jQuery);
