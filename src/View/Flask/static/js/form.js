function submit_form(input) {
  $.getJSON($SCRIPT_ROOT + '/_ajax', {
      full_name: input.attr("id"),
      value: (input.attr("type")=="checkbox") ? (input.is(":checked") ? "yes" : "no") : (input.val())
  }, function(data) {
    // $('#result').text(data.result);
  });
  return false;
};

function multiple_new(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_new', {
      full_name: input.attr("full_name"),
  }, location.reload());
  return false;
};

function multiple_delete(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_delete', {
      full_name: input.attr("full_name"),
      value: input.attr("value"),
  }, location.reload());
  return false;
};

$(function() {

    $('input[type="checkbox"]').bootstrapSwitch();

    $('input').on('change', function() {submit_form($(this) )});
    $('select').on('change', function() {submit_form($(this) )});

    $('.multiple_new').on('click', function() {multiple_new($(this) )});
    $('.multiple_delete').on('click', function() {multiple_delete($(this) )});

    $('input[type=number]').focus();
});