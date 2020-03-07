
(function($) {

  function dynfieldsVisibility(){
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


  var dynHelpTexts = {};
  $(document).ready(function() {
    $( "#id_included_form" ).change(function() {
      dynfieldsVisibility();
    });
    $(".included-form-holder").click(function(){
      dynfieldsVisibility();
    });
    dynfieldsVisibility();

    $('#dynformfields-group select').first().children(' option').each(function(){
      if (this.text.startsWith("-")) return;
      var splitted = this.text.split('#');
      if (splitted.length > 1){
        this.text = splitted[0];
        dynHelpTexts[this.value] = splitted[1];
      }
    });
    $('#dynformfields-group select').change(function(){
      $(this).siblings('p').text(dynHelpTexts[$(this).val()]);
    });
  });


})(grp.jQuery);

