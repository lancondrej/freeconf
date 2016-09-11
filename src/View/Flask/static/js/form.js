function submit_form_input(input) {
    $.getJSON($SCRIPT_ROOT + '/_submit', {
        full_name: input.attr("id"),
        value: input.val()
    }, function (data) {
        // $('#result').text(data.result);
    });
    return false;
}

function submit_form_checkbox(input) {
    $.getJSON($SCRIPT_ROOT + '/_submit', {
        full_name: input.attr("id"),
        value: input.is(":checked") ? "yes" : "no"
    }, function (data) {
        // $('#result').text(data.result);
    });
    return false;
}
function submit_form_select(select) {
    $.getJSON($SCRIPT_ROOT + '/_submit', {
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
    }, function (data){
        if(data.result){reload(input)}
        else{flash()}
    });
}

function multiple_delete(input) {
    $.getJSON($SCRIPT_ROOT + '/_multiple_delete', {
        full_name: input.attr("full_name"),
        value: input.attr("value")
    }, function (data){
        if(data.result){reload(input)}
        else{flash()}
    });
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








function load_form() {
    $('.modal_button').off().on('click', function () {
        open_modal($(this))
    });
    $('.collapse_button').off().on('click', function () {
        open_collapse($(this))
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
    $('input[type="checkbox"]').off().on('switchChange.bootstrapSwitch', function () {
        submit_form_checkbox($(this))
    });
    $('input[type="checkbox"]').bootstrapSwitch();


    $('select').off().on('change', function () {
        submit_form_select($(this))
    });

}


