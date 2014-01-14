
(function($) {

	function dynfieldsVisibility(){
		//console.log("IV", $("#id_included_form:visible").length);
		txt = $( "#id_included_form option:selected" ).text();
		if($("#id_included_form:visible").length){
			if (txt == "---------" || txt == ""){
				$("#dynformfields-group").hide();
			} else {
				$("#dynformfields-group").show();
			}

		} else {
			$("#dynformfields-group").hide();
		}
	}

	$(document).ready(function() {
		$( "#id_included_form" ).change(function() {
			dynfieldsVisibility();
		});
		$(".included-form-holder").click(function(){
			dynfieldsVisibility();
		});
		dynfieldsVisibility();
	});
})(grp.jQuery);

