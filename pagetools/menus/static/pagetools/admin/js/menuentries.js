/* global grp */
(function($){
  $(document).ready(function() {
    // var menu_entries_changed = false;
    var $nest = $('.sortable').nestedSortable({
            handle: 'div',
            items: 'li',
            toleranceElement: '> div',
            /* update: function(event, ui) {
              menu_entries_changed = true;
            }
            */
      });
    $('input[type="submit"]').click(function(){
      $("[name='entry-order']").val($nest.sortable("serialize"));
    });
  });
})(grp.jQuery); 
