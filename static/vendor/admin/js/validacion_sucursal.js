let campo_nombre = $('#id_nombre');
let campo_direccion = $('#id_direccion');
let campo_telefono = $('#id_telefono');

let contador_error = 0;

var regex = /^([-a-zA-ZÀ., ]){3,20}$/i;
var regex_direccion = /^([-%&+# \w]){5,50}$/i;
var regex_telefono = /^([0-9]){7,11}$/;

function validarSucursales(){
    var nombre = campo_nombre.val();
    var direccion = campo_direccion.val();
    var telefono = campo_telefono.val();

    $('.error').remove();

    if (!regex.test(nombre)){
        contador_error += 1;
        campo_nombre.parent().removeClass('has-success has-error');
        campo_nombre.parent().addClass('has-error');
        campo_nombre.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Nombre debe ser mayor a 5 caracteres y a-z</label>')
    }

    if (!regex_direccion.test(direccion)){
        contador_error += 1;
        campo_direccion.parent().removeClass('has-success has-error');
        campo_direccion.parent().addClass('has-error');
        campo_direccion.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Dirección debe ser mayor a 6 caracteres y a-z</label>')
    }

    if(!regex_telefono.test(telefono)){
        contador_error += 1;
        campo_telefono.parent().removeClass('has-success has-error');
        campo_telefono.parent().addClass('has-error');
        campo_telefono.parent().append('<label class="control-label error" for="inputError"><i class="fa fa-times-circle-o"></i> Teléfono deber ser entre 7 y 11 números</label>')
    }

}

function validacion_sucursal() {
    validarSucursales();
    if (!contador_error){
        contador_error = 0;
        return true;
    }else{
        contador_error  = 0;
        return false;
    }
}


