function submit_form_input(input) {
    socket.emit('submit', {
        full_name: input.attr("id"),
        value: input.val()
    });
    return false;
}

// function submit_form_checkbox(input) {
//     socket.emit('submit', {
//         full_name: input.attr("id"),
//         value: input.is(":checked") ? "yes" : "no"
//     });
//     return false;
// }

function set_checkbox_state(input) {
    switch (input.val()) {
        case 'no':
            input.prop('indeterminate', false);
            input.prop('checked', false);
            break;
        case 'yes':
            input.prop('indeterminate', false);
            input.prop('checked', true);
            break;
        default:
            input.prop('indeterminate', true);
            input.prop('checked', false);
    }
}

function change_checkbox_state(input) {
    switch (input.val()) {
        case 'no':
            input.val('');
            break;
        case 'yes':
            input.val('no');
            break;
        default:
            input.val('yes');
    }
}


function submit_form_checkbox(input) {
    change_checkbox_state(input);
    set_checkbox_state(input);
    submit_form_input(input);
    return false;
}

function submit_form_select(select) {
    socket.emit('submit', {
        full_name: select.attr("id"),
        value: select.val()
    });
    return false;
}

function multiple_new(input) {
    socket.emit('multiple_new', {
        full_name: input.attr("full_name")
    });
    return false;
}

function multiple_delete(input) {
    socket.emit('multiple_delete', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    });
    return false;
}


function multiple_up(input) {
    socket.emit('multiple_up', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    });
    return false;
}

function multiple_down(input) {
    socket.emit('multiple_down', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    });
    return false;
}


function load_form() {
    $('.modal_button').off().on('click', function () {
        toogle_modal($(this))
    });
    $('.collapse_button').off().on('click', function () {
        toogle_collapse($(this))
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
    }).on('keypress', function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            submit_form_input($(this))
            return false;
        }
    });

    $('input[type="checkbox"]').each(function () {
        set_checkbox_state($(this));
    }).off().on('change', function () {
        submit_form_checkbox($(this));
    });

    // $('input[type="checkbox"]').off().on('switchChange.bootstrapSwitch', function () {
    //     submit_form_checkbox($(this))
    // });
    // $('input[type="checkbox"]').bootstrapSwitch();


    $('select').off().on('change', function () {
        submit_form_select($(this))
    });

    $('[data-toggle="popover"]').popover();

}


