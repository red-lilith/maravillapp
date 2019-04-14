let campo_nombre = $('#id_nombre');

let contador_error = 0;

var regex = /^([a-z]){4,20}$/i;

function validarGeneros(){
    var nombre = campo_nombre.val();

    $('.error').remove();

    if (!regex.test(nombre)){
        contador_error += 1;
        campo_nombre.parent().removeClass('has-success has-error');
        campo_nombre.parent().addClass('has-error');
        campo_nombre.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Género debe ser mayor a 4 caracteres y a-z</label>')
    }

}

function validacion_genero() {
    validarGeneros();
    if (!contador_error){
        contador_error = 0;
        return true;
    }else{
        contador_error  = 0;
        return false;
    }
}


