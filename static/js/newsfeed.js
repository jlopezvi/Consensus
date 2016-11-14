var url = window.location.href;
url = url.split("/");

$(document).ready(function(){
	$('.home--content').css('background-image','url("")');
	var percent = $('#percent').val();
	var total = Math.floor(percent);
	$('.input--percent').append(total + '%');
	var support_percent = $('#supporters--percent').val();
	$('.newsfeed--bar').css('width',support_percent+'%');

	var volunter_percent = $('#volunters--percent').val();
	$('.newsfeed--bar2').css('width',volunter_percent+'%');

	$.ajax({
      url: url[0] + "//" + url[2] + '/ideas_for_newsfeed',
      type: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function(json) {
        console.log(json);
      },
      error: function(response){
        console.log('error');
        console.log(response);
        /*
        if(response.responseText == "redirect to Home"){
          alert("Redirecting to Home");
          //window.location = '/home';
        } else {

        }
        */
      }
    });
});