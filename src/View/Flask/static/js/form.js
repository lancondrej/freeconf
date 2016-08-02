    function submit_form(input) {
      $.getJSON($SCRIPT_ROOT + '/_ajax', {
          full_name: input.attr("id"),
          value: (input.attr("type")=="checkbox") ? (input.is(":checked") ? "yes" : "no") : (input.val())
      }, function(data) {
        $('#result').text(data.result);
      });
      return false;
    };


$(function() {

    $('input[type="checkbox"]').bootstrapSwitch();

    $('input').on('change', function() {submit_form($(this) )});
    $('select').on('change', function() {submit_form($(this) )});

    // $('input[type=number]').bind('keydown', function(e) {
    //   if (e.keyCode == 13) {
    //     submit_form(e);
    //   }
    // });


    $('input[type=number]').focus();
});