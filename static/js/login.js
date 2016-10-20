function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
  }
  return "";
 var name = cname + "=";
 var ca = document.cookie.split(';');
 for(var i=0; i<ca.length; i++) {
   var c = ca[i];
   while (c.charAt(0)==' ') c = c.substring(1);
   if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
 }
 return "";
};

$(document).ready( function() {
	$(document).on('change', ':file', function() {
    var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  $(document).ready( function() {
    $(':file').on('fileselect', function(event, numFiles, label) {
      var input = $(this).parents('.input-group').find(':text'),
        log = numFiles > 1 ? numFiles + ' files selected' : label;

      if( input.length ) {
        input.val(log);
      } else {
        if( log ) alert(log);
      }
    });
  });

  $(document).on('click', '.login--button', function(){
    $('.login--message').hide();
    var data = {
      'email': $('#email').val(),
      'password': $('#password').val()
    };
    if(data.email == '' || data.password == ''){
      $('.login--message').empty().append('All fields must be fills!').show();
    } else {
        $.ajax({
          url: 'login',
          type: 'POST',
          data: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          },
          dataType: 'json',
          success: function (json) {
            console.log();
            if(json.result == 'Bad password'){
              $('.login--message').empty().append('Email or Password wrong!').show();
            } else if(json.result == 'Bad e-mail'){
              $('.login--message').empty().append('e-mail not found / not verified').show();
            } else if(json.result == 'Login validated'){
              window.location = '/newsfeed';
            }
          },
          error: function(response){
            console.log('error');
            console.log(response);
          }
        });
    }
  });

  $(document).on('click', '.register--button', function(e){
    $('.register--message').hide();
    var data = {
      'fullname': $('#fullname_r').val(),
      'email': $('#email_r').val(),
      'username': $('#username_r').val(),
      'position': $('#position_r').val(),
      'group': 'IT', //$('#group_r').val(),
      'password': $('#password_r').val(),
      'image_url': '', //$('#password').val(),
      'ifpublicprofile': $('#public_r').val(),
      'host_email': null,
      'ifemailverified': false
    };
    if(data.email == '' || data.password == '' || $('#password2_r').val() == '' || data.fullname == '' || data.username == '' || data.position == '' || data.group == ''){
        $('.register--message').removeClass('alert-success').addClass('alert-danger');
        $('.register--message').empty().append('All fields must be fills!').show();
    } else {
        if($('#password_r').val() == $('#password2_r').val()){
            $('#modal_sign').modal('show');
        } else {
            $('.register--message').removeClass('alert-success').addClass('alert-danger');
            $('.register--message').empty().append('Passwords must be the same!').show();
        }
    }
  });

  $(document).on('click', '.register--modal', function(){
    if ($('#public_r').is(":checked"))
        opt = true;
    else
        opt = false;
    console.log(opt);
    var data = {
      'fullname': $('#fullname_r').val(),
      'email': $('#email_r').val(),
      'username': $('#username_r').val(),
      'position': $('#position_r').val(),
      'group': 'IT', //$('#group_r').val(),
      'password': $('#password_r').val(),
      'image_url': '', //$('#password').val(),
      'ifpublicprofile': opt
      'host_email': null,
      'ifemailverified': true
    };
    $.ajax({
      url: 'registration',
      type: 'POST',
      data: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function (json) {
        if(json.result == 'registration pending of email verification'){
            $('.register--message').removeClass('alert-danger').addClass('alert-success');
            $('.register--message').empty().append('Registration completed. <br> Check your email and validate your account!').show();
        }
      },
      error: function(response){
        console.log(response);
      }
    });
  });
});