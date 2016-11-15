function load() {
    load_form();
    load_modal();
        flash();


}

function reload(elem) {
    var entry = elem.closest(".entry")
    reload_element(entry)
    flash()
}

function reload_element(elem) {
    $.get($SCRIPT_ROOT + '/_reload_element', {
        full_name: elem.attr("full_name")
    }, function (data) {
        elem.replaceWith(data)
        load()
    });
}

function flash() {
    $.get($SCRIPT_ROOT + '/_flash', function (data) {
        $('#flash').empty().append(data)
    })
}


function undo() {
    $.getJSON($SCRIPT_ROOT + '/_undo',function (data) {
       if(data.result){
        reload($("[id*='"+data.full_name+"']"));
        }
    });
}

function redo() {
    $.getJSON($SCRIPT_ROOT + '/_redo',function (data) {
        if(data.result){
        reload($("[id*='"+data.full_name+"']"));
        }
    });
}

$(function () {
    load();

    $('#undo').on('click', function () {
        undo()
    });

    $('#redo').on('click', function () {
        redo()
    });
});
