function submit_form(input) {
  $.getJSON($SCRIPT_ROOT + '/_ajax', {
      full_name: input.attr("id"),
      value: (input.attr("type")=="checkbox") ? (input.is(":checked") ? "yes" : "no") : (input.val())
  }, function(data) {
    // $('#result').text(data.result);
  });
  return false;
}

function multiple_new(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_new', {
      full_name: input.attr("full_name")
  }, location.reload());
  return false;
}

function multiple_delete(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_delete', {
      full_name: input.attr("full_name"),
      value: input.attr("value")
  }, location.reload());
  return false;
}

function multiple_up(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_up', {
      full_name: input.attr("full_name"),
      value: input.attr("value")
  }, location.reload());
  return false;
}

function multiple_down(input) {
  $.getJSON($SCRIPT_ROOT + '/_multiple_down', {
      full_name: input.attr("full_name"),
      value: input.attr("value")
  }, location.reload());
  return false;
}


function load_modal(input) {
    $.get($SCRIPT_ROOT + '/_multiple_modal', {
      full_name: input.attr("full_name")
    }, function( data ) {
        $('#Modals').append( data );
        $(input.attr("data-target")).modal('show');
        loaded()
    });
}


function loaded(input) {
    $('.modal_button').on('click', function() {load_modal($(this) )});

    $('.modal-content').resizable({
    //alsoResize: ".modal-dialog",
    minHeight: 300,
    minWidth: 300
    });
    $('.modal-dialog').draggable();
    $('input[type="checkbox"]').bootstrapSwitch();

    $('input').on('change', function() {submit_form($(this) )});
    $('select').on('change', function() {submit_form($(this) )});

    $('.multiple_new').on('click', function() {multiple_new($(this) )});
    $('.multiple_delete').on('click', function() {multiple_delete($(this) )});
    $('.multiple_up').on('click', function() {multiple_up($(this) )});
    $('.multiple_down').on('click', function() {multiple_down($(this) )});

        $( ".modal" ).click(function( event ) {
      if( event.currentTarget === event.target ){
          $(this).css('z-index',  "1045" );
          var elem = document.elementFromPoint(event.clientX , event.clientY);
          var up=this;
          while($(elem).is( ".modal" ) && elem != up){
                $(elem).css('z-index',  "1045" );
                up = elem;
                elem = document.elementFromPoint(event.clientX , event.clientY);
          }
          var par = $(elem).parents(".modal");
          $(".modal").css('z-index',  "1050" );
          if(par.length){
              par.css('z-index',  "1051" );
          }
          else{
              $(".modal").modal('hide');
          }
      }
    });

    // TODO: tady si ještě trochu pohrát s okny

}

$(function() {
loaded();
    //     $(document).on('show.bs.modal', '.modal', function () {
    //     var zIndex = 1050 + (10 * $('.modal:visible').length);
    //     $(this).css('z-index', zIndex);
    //     setTimeout(function() {
    //         $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    //     }, 0);
    // });
    $(document).on('hidden.bs.modal', '.modal', function () {
        if ($('.modal-backdrop').length) {
        $('body').addClass('modal-open');
        }
        else{
            location.reload()
        }
    });
});

