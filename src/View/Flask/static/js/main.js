function load() {
    load_form();
    load_modal();

}




$(document).ready(function() {

    
    socket.on('log', function(data) {
        $('#log').prepend('<li>'+data.log_time +': ' + data.log_record + '</li>');
    });

    socket.on('flash', function(data) {
        $('#flash').prepend(data.flash);
        setTimeout(function() {$('#flash').find('div:first-child' ).remove()}, 5000);
    });

    socket.on('reload', function(data) {
        $("[id='entry_"+data.full_name+"']").replaceWith(data.rendered_entry);
        console.log(data);
        load()

    });


    $('#undo').on('click', function () {
    socket.emit('undo');
    });

    $('#redo').on('click', function () {
    socket.emit('redo');
    });

    $('#save_config').on('click', function () {
    socket.emit('save_config');
    });
    
    $('#save_native').on('click', function () {
    socket.emit('save_native');
    });

    load();

});
