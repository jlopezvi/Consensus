$('.cropme_profile').simpleCropper();
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
var hostEmail = '';
var guestEmail = '';
$(document).ready( function() {
  $(document).on('change', ':file', function() {
    var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
  };

  $('.emailValidate').focusout(function(){
    var email = $(this).val();
    var parent = $(this).parent().parent();
    var cond = false;
    if(parent.hasClass('home--login'))
      cond = true;
    if( !isValidEmailAddress( email ) ) {
      $(this).addClass('errorInput');
      if(cond)
        $('.login--button').prop('disabled', true);
      else
        $('.register--button').prop('disabled', true);
    } else {
      $(this).removeClass('errorInput');
      if(cond)
        $('.login--button').prop('disabled', false);
      else
        $('.register--button').prop('disabled', false);
    }
  });

  $('#fullname_r').keypress(function(e){
    var r = /^[a-zA-ZäöüÄÖÜáéíóúÁÉÚÍÓÑñ\b ]+$/;
    var verified = r.test(String.fromCharCode(e.which));
    if (!verified)
      e.preventDefault();
  });

  $('#position_r').keypress(function(e){
    var r = /^[a-zA-ZäöüÄÖÜáéíóúÁÉÚÍÓÑñ\b ]+$/;
    var verified = r.test(String.fromCharCode(e.which));
    if (!verified)
      e.preventDefault();
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
          url: url[0] + "//" + url[2] + '/login',
          type: 'POST',
          data: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          },
          dataType: 'json',
          success: function (json) {
            if(json.result == 'Wrong: Bad password'){
              $('.login--message').empty().append('Email or Password wrong!').show();
            } else if(json.result == 'Wrong: Bad e-mail'){
              $('.login--message').empty().append('e-mail not found / not verified').show();
            } else if(json.result == 'OK'){
              //GETTING ALL IDEAS FOR NEWSFEED TO VALIDATE THE REDIRECT
              
              $.ajax({
                url: url[0] + "//" + url[2] + '/if_ideas_for_newsfeed',
                type: 'GET',
                success: function (json){
                  if(json.result)
                    window.location = '/newsfeed';
                  else
                    window.location = '/home';
                } 
              });
              
            }
          },
          error: function(response){
            //console.log(response);
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
      'group': $('#group_r option:selected').val(),
      'password': $('#password_r').val(),
      'image_url': '', //$('#password').val(),
      'ifpublicprofile': $('#public_r').val(),
      'host_email': null,
      'ifemailverified': false
    };
    
    if(data.email == '' || data.password == '' || $('#password2_r').val() == '' || data.fullname == '' || data.username == '' || data.position == '' || data.group == '' || data.group == 0){
        $('.register--message').removeClass('alert-success').addClass('alert-danger');
        $('.register--message').empty().append('All fields must be fills!').show();
    } else {
        if($('#password_r').val() == $('#password2_r').val()){
            $.ajax({
              url: url[0] + "//" + url[2] + '/if_participant_exists_by_email/'+data.email,
              type: 'GET',
              headers: {
                'Content-Type': 'application/json'
              },
              dataType: 'json',
              success: function (json) {
                if(json.result){
                  $('.register--message').removeClass('alert-success').addClass('alert-danger');
                  $('.register--message').empty().append('Email already taken').show();
                } else {
                  $('#modal_sign').modal('show');
                }
              },
              error: function(response){
                //console.log('error');
              }
            });

        } else {
            $('.register--message').removeClass('alert-success').addClass('alert-danger');
            $('.register--message').empty().append('Passwords must be the same!').show();
        }
    }
  });

  $(document).on('click', '.register--modal', function(){
    $('.register--button').prop('disabled', 'true');
    if ($('#public_r').is(":checked"))
        opt = true;
    else
        opt = false;
    
    var newData = {
      'fullname': $('#fullname_r').val(),
      'email': $('#email_r').val(),
      'username': $('#username_r').val(),
      'position': $('#position_r').val(),
      'group': $('#group_r').val(),
      'password': $('#password_r').val(),
      'ifpublicprofile': opt,
      'ifregistrationfromemail': false,
      'host_email': 'none'
    };

    hostEmail = $('#hostEmail').val();
    if(hostEmail != null){
      newData['host_email'] = hostEmail;
      newData['ifemailverified'] = true;
      newData['ifregistrationfromemail'] = true;
    }
    
    newData['profilepic'] = null;
    if($('.cropme_profile img').length){
      newData['profilepic'] = $('.cropme_profile img').attr('src');
    }
    
    var host_ideas_lenght = 0;
        
    $.ajax({
      url: url[0] + "//" + url[2] + '/registration',
      type: 'POST',
      data: JSON.stringify(newData),
      headers: {
          'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function (json) {
        if(json.result != 'OK'){
          $('.register--message').removeClass('alert-danger').addClass('alert-success');
          $('.register--message').empty().append('Participant registered previously, resend email verification.').show();
          $('.register--button').prop('disabled', 'false');
        } else {
          if((json.ifhost) && (json.ifemailverified)){
            
              $.ajax({
                url: url[0] + "//" + url[2] + '/if_ideas_for_newsfeed',
                type: 'GET',
                success: function (json){
                  if(json.result)
                    window.location = '/newsfeed';
                  else
                    window.location = '/home';
                } 
              });
            
          }
          else{
            $('.register--message').removeClass('alert-danger').addClass('alert-success');
            $('.register--message').empty().append('E-mail verification sent.<br>Close this window and check your e-mail within the next few minutes.').show();
            $('.register--button').prop('disabled', 'false');
          }
        }
      },
      error: function(response){
        //console.log(response);
      }
    });
    
  });

  function archive(evt) {
	var files = evt.target.files;
	for (var i = 0, f; f = files[i]; i++) {
	if (!f.type.match('image.*')) {
	  continue;
	}
	var reader = new FileReader();
	reader.onload = (function(theFile) {
	return function(e) {
	  //$('.user--icon--login').css('background-image', 'url("'+e.target.result+'")');
	  $('.user--icon--login').attr('src', e.target.result);
	};
	})(f);
      reader.readAsDataURL(f);
    }
  }
  //document.getElementById('profile_photo').addEventListener('change', archive, false);
  
  /**************************** CROPPIE FUNCTIONS ****************************/
  
  

});

var url = window.location.href;
url = url.split("/");

$( window ).load(function(){
  /*********** READY WHEN INVITATION **************/
  hostEmail = $('#hostEmail').val();
  guestEmail = $('#guestEmail').val();
  emailVerificated = $('#emailVerificated').val();
  if(emailVerificated != null){
    $('#email').val(emailVerificated);
  }
  if(hostEmail != null){
    $('#email_r').val(guestEmail).prop('disabled', true);
    $.ajax({
      url: url[0] + "//" + url[2] + '/get_fullname_for_participant_unrestricted/'+hostEmail,
      type: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function (json) {
        ////console.log(json);
        $('.home--content--left h1').html(json.fullname + '<br>Welcomes You!');
        if(json.fullname.length > 18)
          $('.home--content--left h1').css('font-size', '65px');
        if(json.fullname.length > 24)
          $('.home--content--left h1').css('font-size', '55px');
        if(json.fullname.length > 30)
          $('.home--content--left h1').css('font-size', '45px');
          
      },
      error: function(response){
        ////console.log(response.responseText);
        //$('.login--message2').append('You have been invited by <strong>'+ response.responseText +'</strong>');
      }
    });
  }
});

