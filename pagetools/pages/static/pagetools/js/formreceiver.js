(function($){
  function setMailReceiversVisibility(){
    var $formField = $("select#id_included_form");
    var action = $formField.val() ? "show" : "hide";
    $("div.email_receivers")[action]();
  }
  $(document).ready(function(){
    setMailReceiversVisibility();
    $("select#id_included_form").change(function(){
      setMailReceiversVisibility();
    });

  })
}(grp.jQuery));
