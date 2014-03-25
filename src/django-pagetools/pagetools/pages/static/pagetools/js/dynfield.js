(function($) {
	
	function dynfieldsVisibility(){
		txt = $( "#id_included_form option:selected" ).text();
		if (txt == "---------"){
			$("#dynformfields-group").hide();
		} else {
			$("#dynformfields-group").show();
		}
	}
	
	$(document).ready(function() {
		$( "#id_included_form" ).change(function() {
			dynfieldsVisibility();
		});
		dynfieldsVisibility();
	});
		//
})(grp.jQuery);

