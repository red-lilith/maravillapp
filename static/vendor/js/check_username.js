
$('#id_username').keyup(function(e){
  check_username();
});

function check_username(){

  var username = $('#id_username').val();
  var $div_username = $('#id_username').parent();

  if(username.length == 0){
    $div_username.removeClass('has-success has-error');
    $('.username-error').remove();
    $('.username-success').remove();
  }

  $.get(url_api, {"csrfmiddlewaretoken":token,'username': username}, function(data){

    $div_username.removeClass('has-success has-error');
    $('.username-error').remove();
    $('.username-success').remove();

    if (data.response) {
      $div_username.addClass('has-success');
      $div_username.append('<label class="control-label username-success" for="inputSuccess"><i class="fa fa-check"></i> Username disponible</label>');

    }else{
      $div_username.addClass('has-error');
      $div_username.append('<label class="control-label username-error" for="inputError"><i class="fa fa-times-circle-o"></i> Username no disponible</label>')
    }
  });
}
