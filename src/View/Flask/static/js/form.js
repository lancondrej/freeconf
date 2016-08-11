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

function multiple_up(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_up', {
      full_name: input.attr("full_name"),
      value: input.attr("value"),
  }, location.reload());
  return false;
};

function multiple_down(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_down', {
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
    $('.multiple_up').on('click', function() {multiple_up($(this) )});
    $('.multiple_down').on('click', function() {multiple_down($(this) )});


    $('.modal-content').resizable({
    //alsoResize: ".modal-dialog",
    minHeight: 300,
    minWidth: 300
    });
    $('.modal-dialog').draggable();

    // $('.modal').on('show.bs.modal', function () {
    //     $(this).find('.modal-body').css({
    //         'max-height':'100%'
    //     });
    // });

    $(".modal").appendTo("#Modals");

    $(document).on('show.bs.modal', '.modal', function () {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });
    $(document).on('hidden.bs.modal', '.modal', function () {
        if ($('.modal-backdrop').length) {
        $('body').addClass('modal-open');
        }
        else{
            location.reload()
        }
    });
});

