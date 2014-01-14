$(document).ready(function() {
	var menu_entries_changed = false;
	var $nest = $('.sortable').nestedSortable({
          handle: 'div',
          items: 'li',
          toleranceElement: '> div',
          //containment: "parent",
          update: function(event, ui) {
            console.log("EVENT UI")
        	  menu_entries_changed = true;
          }
    });
	$('input[type="submit"]').click(function(){
		$("[name='entry-order']").val($nest.sortable("serialize"));
	});
});

