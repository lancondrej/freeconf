function load() {
    load_form();
    load_modal();
}



function tabs_on() {
    $('#tabs').find('button').on('click', function () {
        socket.emit('tab', {
            name: $(this).attr('value')
        });
        $('#tabs').find('button').removeClass('active');
        $(this).addClass( 'active' );
        $(".tab_shader").css("display", "block");
        $("#loader").css("display", "block");
    });
}

$(document).ready(function() {

    
    socket.on('log', function(data) {
        $('#log').prepend('<li>'+data.log_time +': ' + data.log_record + '</li>');
    });

    socket.on('flash', function(data) {
        $('#flash').prepend(data.flash);
        setTimeout(function() {$('#flash').find('div:first-child' ).remove()}, 5000);
    });

    socket.on('reload_entry', function(data) {
        $("[id='entry_"+data.full_name+"']").replaceWith(data.rendered_entry);
        load()

    });

    socket.on('reload_tabs', function(data) {
        $("#tabs").replaceWith(data.rendered_tabs);
        tabs_on();
    });

    socket.on('reload_tab', function(data) {
        $(".tab_shader").css("display", "none");
        $("#tab").replaceWith(data.rendered_tab);
        load();
        $("#loader").css("display", "none");
    });

    socket.on('reload_section', function(data) {
        $("[id='section_"+data.full_name+"']").replaceWith(data.rendered_section);
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

    tabs_on();
    load();
    

});
