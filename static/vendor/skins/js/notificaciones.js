$('.notificaciones').on('click', '.modal-notificacion', function() {
    noti($(this));
});

function noti($elemento) {

    let titulo = $elemento.data('titulo');
    let mensaje = $elemento.data('mensaje');
    let icono = $elemento.data('icono');
    let id = $elemento.data('id');

    const modal = $('#modal-noti');
    modal.find('.modal-title').text('');
    modal.find('.modal-title').append('<i class="' + icono + '"></i>  ' + titulo)
    modal.find('.modal-body').text(mensaje);

    //funcion para cambiarle el estado de leido
    $.get(url_api, {
        "csrfmiddlewaretoken": token,
        'id': id
    }, function(data) {

        //Modificar el numero de las notificaciones
        const $span_notis = $('#num_notis');
        let num_notificaciones = $span_notis.html();

        //Variables para modificar el label de las notificaciones
        const $label_notis = $('#label_notificaciones');
        $label_notis.text('');

        var num_notis_actual = num_notificaciones - 1;

        if (num_notis_actual == 0) {
            $span_notis.remove();
            $label_notis.text('Has leído todas las notificaciones');
        } else {
            $span_notis.text(num_notificaciones - 1);
            $label_notis.text('Tienes ' + num_notis_actual + ' notificaciones sin leer');
        }

        //Borrar las notificaciones que se van leyendo
        const $elemento_notificacion = $('#noti_' + id);
        $elemento_notificacion.remove();

    });

}