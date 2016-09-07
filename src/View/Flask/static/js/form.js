function submit_form_input(input) {
    $.getJSON($SCRIPT_ROOT + '/_ajax', {
        full_name: input.attr("id"),
        value: (input.attr("type") == "checkbox") ? (input.is(":checked") ? "yes" : "no") : (input.val())
    }, function (data) {
        // $('#result').text(data.result);
    });
    return false;
}
function submit_form_select(select) {
    $.getJSON($SCRIPT_ROOT + '/_ajax', {
        full_name: select.attr("id"),
        value: select.val()
    }, function (data) {
        // $('#result').text(data.result);
    });
    return false;
}

function multiple_new(input) {
    $.getJSON($SCRIPT_ROOT + '/_multiple_new', {
        full_name: input.attr("full_name")
    }).done(reload(input));
    return false;
}

function multiple_delete(input) {
    $.getJSON($SCRIPT_ROOT + '/_multiple_delete', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    }).done(reload(input));
    return false;
}

function multiple_up(input) {
    $.getJSON($SCRIPT_ROOT + '/_multiple_up', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    }).done(reload(input));
    return false;
}

function multiple_down(input) {
    $.getJSON($SCRIPT_ROOT + '/_multiple_down', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    }).done(reload(input));
    return false;
}


function load_modal(input) {
    if ($(input.attr("data-target")).length) {
        $(input.attr("data-target")).modal('show');
        // loaded()
    }
    else {
        $.get($SCRIPT_ROOT + '/_multiple_modal', {
            full_name: input.attr("full_name")
        }, function (data) {
            $('#Modals').append(data);
            $(input.attr("data-target")).modal('show');
            loaded();
        });
    }

}

function load_collapse(input) {
    if ($(input.attr("data-target")).length) {
        $(input.attr("data-target")).collapse('toggle');
    }
    else {
        $.get($SCRIPT_ROOT + '/_multiple_collapse', {
            full_name: input.attr("full_name")
        }, function (data) {
            input.after(data);
            $(input.attr("data-target")).collapse('show');
            loaded();
        });
    }
    input.toggleClass("btn-primary btn-info");
    input.find("span.glyphicon").toggleClass("glyphicon-menu-down glyphicon-menu-up");

}

function reload_element(elem) {
    $.get($SCRIPT_ROOT + '/_reload_element', {
        full_name: elem.attr("full_name")
    }, function (data) {
        elem.replaceWith(data)
        loaded()
    });
}

function reload(elem) {
    var entry = elem.closest(".entry")
    reload_element(entry)
}

function loaded(input) {
    $('.modal_button').off().on('click', function () {
        load_modal($(this))
    });
    $('.collapse_button').off().on('click', function () {
        load_collapse($(this))
    });

    $('.multiple_new').off().on('click', function () {
        multiple_new($(this))
    });
    $('.multiple_delete').off().on('click', function () {
        multiple_delete($(this))
    });
    $('.multiple_up').off().on('click', function () {
        multiple_up($(this))
    });
    $('.multiple_down').off().on('click', function () {
        multiple_down($(this))
    });

    $('input').off().on('change', function () {
        submit_form_input($(this))
    });
    $('select').off().on('change', function () {
        submit_form_select($(this))
    });

    $('input[type="checkbox"]').bootstrapSwitch();

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

}

$(function () {
    loaded();
    //     $(document).on('show.bs.modal', '.modal', function () {
    //     var zIndex = 1050 + (10 * $('.modal:visible').length);
    //     $(this).css('z-index', zIndex);
    //     setTimeout(function() {
    //         $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    //     }, 0);
    // });
    $(document).on('hidden.bs.modal', '.modal', function () {
        console.log(this);
        if ($('.modal-backdrop').length) {
            $('body').addClass('modal-open');
        }
        else {
            //location.reload()
        }
    });
    $(document).on('hidden.bs.collapse', '.collapse', function () {
        reload($(this));

    });

    // $(document).on('hidden.bs.collapse', '.collapse', function () {
    //         // location.reload()
    // });
});

