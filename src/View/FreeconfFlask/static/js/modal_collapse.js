function open_modal(input) {
    var modal="[id='Modal_" + input.attr('full_name') + "']";
    var collapse="[id='Collapse_" + input.attr('full_name') + "']";
    $(modal).remove();
    if ($(collapse).length) {
        open_collapse(input.prev())
    }
    $.get($SCRIPT_ROOT + '/_multiple_modal', {
        full_name: input.attr("full_name")
    }, function (data) {
        $('#Modals').append(data);
        $(modal).modal('show');
        load();
    });

}

function open_collapse(input) {
    var collapse="[id='Collapse_" + input.attr('full_name') + "']";
    if ($(collapse).length) {
        $(collapse).collapse('hide').on('hidden.bs.collapse', function () {
            $(collapse).remove();
        });
    }
    else {
        $.get($SCRIPT_ROOT + '/_multiple_collapse', {
            full_name: input.attr("full_name")
        }, function (data) {
            input.parent().after(data);
            $(collapse).collapse('show');
            load();
        });
    }
    input.toggleClass("btn-primary btn-info");
    input.find("span.glyphicon").toggleClass("glyphicon-menu-down glyphicon-menu-up");

}

function load_modal(input) {
    $('.modal_button').off().on('click', function () {
        open_modal($(this))
    });
    $('.collapse_button').off().on('click', function () {
        open_collapse($(this))
    });

    $('.modal-content').resizable({
        //alsoResize: ".modal-dialog",
        minHeight: 300,
        minWidth: 300
    });
    $('.modal-dialog').draggable();


    $(".modal").click(function (event) {
        if (event.currentTarget === event.target) {
            $(this).css('z-index', "1045");
            var elem = document.elementFromPoint(event.clientX, event.clientY);
            var up = this;
            while ($(elem).is(".modal") && elem != up) {
                $(elem).css('z-index', "1045");
                up = elem;
                elem = document.elementFromPoint(event.clientX, event.clientY);
            }
            var par = $(elem).parents(".modal");
            $(this).css('z-index', "1050");
            if (par.length) {
                par.css('z-index', "1051");
            }
            else {
                $(".modal").modal('hide');
            }
        }
    });

    // TODO: tady si ještě trochu pohrát s okny

        //     $(document).on('show.bs.modal', '.modal', function () {
    //     var zIndex = 1050 + (10 * $('.modal:visible').length);
    //     $(this).css('z-index', zIndex);
    //     setTimeout(function() {
    //         $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    //     }, 0);
    // });
    $(document).off().on('hidden.bs.modal', '.modal', function () {
        console.log(this);
        if ($('.modal-backdrop').length) {
            $('body').addClass('modal-open');
        }
     });
    // $(document).off().on('hidden.bs.collapse', '.collapse', function () {
    // });

    // $(document).on('hidden.bs.collapse', '.collapse', function () {
    //         // location.reload()
    // });

}


