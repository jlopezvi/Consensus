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
    var data = {
      'email': $('#email').val(),
      'password' : $('#password').val()
    };
    console.log(data);
    $.ajax({
      url: 'login',
      type: 'POST',
      data: {
        'email': $('#email').val(),
        'password' : $('#password').val()
      },
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
      },
      dataType: 'json',
      success: function (json) {
        console.log(json);
      },
      error: function(response){
        console.log(response);
      }
    });
       var data = {
         'email': $('#email').val(),
         'password' : $('#password').val()
       };
       console.log(data);
       $.ajax({
         url: 'login',
         type: 'POST',
         data: {
           'email': $('#email').val(),
           'password' : $('#password').val()
         },
         headers: {
           'X-CSRFToken': getCookie("csrftoken")
         },
         dataType: 'json',
         success: function (json) {
           console.log(json);
         },
         error: function(response){
           console.log(response);
         }
       });
  });
});